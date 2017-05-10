#!/usr/bin/python3 
import sys, os
sys.path.append(os.path.dirname(os.path.realpath(__file__))+'/components')
import random
import time

from sim_components import *


"""
This is a starter pack for a cpu scheduling project. The code / classes provided are to give you a
head start in creating the scheduling simulation. Obviously this is a simulation, so the majority
of the concepts are "simulated". For example, process "burst times" and "IO times" are known
a-priori (not so in real world). Things like memory are abstracted from addressable locations and
page tables to total "blocks" needed.
"""


###################################################################################################

# === Class: MLFQ===

class MLFQ(object):
    """Multi-Level Feedback Queue

    - Some general requirements for a MLFQ:
        - Each queue needs its own scheduling algorithm (typically Fcfs).
        - The method used to determine when to upgrade a process to a higher-priority queue.
        - The method used to determine when to demote a process to a lower-priority queue.
        - The method used to determine which queue a process will enter when that process needs
        service.

    - Rule 1: If Priority(A) > Priority(B), A runs (B doesn't).
    - Rule 2: If Priority(A) = Priority(B), A & B run in RR.
    - Rule 3: When a job enters the system, it is placed at the highest priority (the topmost
              queue).
    - Rule 4: Once a job uses up its time allotment at a given level (regardless of how many times
              it has given up the CPU), its priority is reduced (i.e., it moves down one queue).
    - Rule 5: After some time period S, move all the jobs in the system to the topmost queue.

    - **Attributes**:
        - self.num_levels
        - self.queues
    """
    def __init__(self, num_levels=2):
        self.num_levels = num_levels
        self.queues = []

        for i in range(self.num_levels):
            self.queues.append(Fifo())

    def new(self, process):
        """This method admits a new process into the system.

        - **Args:**
            - None
        - **Returns:**
            - None
        """
        self.queues[process.priority].add(process)

    def nextProcess(self):
        if not self.queues[1].empty():  # there is at least one process with high priority
            p = self.queues[1].remove() # get the process from the queue
        elif not self.queues[0].empty():  # there is at least one process with low priority
            p = self.queues[0].remove()
        else:
            p = None
        return p

    def __str__(self):
        """Visual dump of class state.

        - **Args:**
            - None
        - **Returns:**
            - None
        """
        return MyStr(self)

###################################################################################################

# === Class: Scheduler===

class Scheduler(object):
    """
    New:        In this status, the Process is just made or created.
    Running:    In the Running status, the Process is being executed.
    Waiting:    The process waits for an event to happen for example an input from the keyboard.
    Ready:      In this status the Process is waiting for execution in the CPU.
    Terminated: In this status the Process has finished its job and is ended.
    """
    def __init__(self, *args, **kwargs):
        self.clock = Clock()
        self.memory = Memory()                  
        self.cpu = Cpu()
        self.accounting = SystemAccounting()
        self.semaphore = []
        for i in range(5):
            self.semaphore.append(Semaphore(1))
        self.job_scheduling_queue = Fifo()

        self.events = kwargs['jobs']
        self.ready = MLFQ()  # list of ready process
        self.finished = []   # list of finished p  rocess
        self.cpu_time = [300, 100]

        self.io_queue = {}  # actually not a queue but a dictionary

    def new_process(self,job_info):
        """New process entering system gets placed on the 'job_scheduling_queue'.
        - **Args**:
            - job_info (dict): Contains new job information.
        - **Returns**:
            - None
        """

        if int(job_info['mem_required']) > 512:  # reject the job, it doesn't fit in the memory
            return "This job exceeds the system's main memory capacity."

        self.job_scheduling_queue.add(Process(**job_info))
        self.job_scheduling()

        return True

    def job_scheduling(self):
        t = self.clock.current_time()
        process = self.job_scheduling_queue.first()

        while process and self.memory.fits(process['mem_required']):
            self.memory.allocate(process)
            process.inScheduleTime = self.clock.current_time()
            self.job_scheduling_queue.remove()
            process.priority = 1
            self.ready.new(process)
            process = self.job_scheduling_queue.first()

        # no process in the cpu, try to schedule
        if not self.cpu.busy():
            self.process_scheduling()

    def process_scheduling(self):

        if self.cpu.busy():
            p0 = self.cpu.running_process.priority  # running process priority
            if p0 == 0 and not self.ready.queues[1].empty():   # there is a process in the first queue which needs to be run
                currentProcess = self.cpu.running_process      # queue the current process
                self.ready.new(currentProcess)
                self.cpu.remove_process()

                for event in currentProcess.events:
                    if event['time'] in self.events:
                        del self.events[event['time']]


            else:
                return

        process = self.ready.nextProcess()

        if process == None:  # idle processor
            return
        if process.startTime == None:  # new process...
            process.startTime = self.clock.clock   # set the start time
        terminate_time = self.clock.clock + int(process.burst_time)

        process.cpu_time = self.cpu_time[process.priority]

        self.newEvent(process, self.clock.clock + process.burstLeft, 'T')
        self.newEvent(process, self.clock.clock + process.cpu_time, 'E')

        self.cpu.run_process(process)

    def newEvent(self, process, time, event):

        # first check if the event is a E event are there is already a T event, ignore it:
        if event == 'E':
            if str(time) in self.events:
                for e in self.events[str(time)]:
                    if e['event']=='T':          # ignore this event, we cannot have a T and E in the same moment
                        return
        ev = {'time':str(time), 'event': event}
        process.events.append(ev)

        if ev['time'] not in self.events:
            self.events[ev['time']] = []
        self.events[ev['time']].append(ev)

    def perform_io(self,info):
        """Current process on cpu performs io
        """
        # send current process to the
        currentProcess = self.cpu.running_process

        completeTime = self.clock.clock + int(info['ioBurstTime'])

        if currentProcess == None:
            pass

        currentProcess.iostart = self.clock.clock
        currentProcess.ioburst =  int(info['ioBurstTime'])
        self.cpu.remove_process()

        # remove all remaining event for this process
        for event in currentProcess.events:
            if event['time'] in self.events:
                del self.events[event['time']]
            else:
                pass

        currentProcess.events = []  # clear current process events

        self.newEvent(currentProcess, completeTime, 'C')
 
        if str(completeTime) not in self.io_queue:
            self.io_queue[str(completeTime)] = []
        self.io_queue[str(completeTime)].append(currentProcess)
        # info = self.cpu.remove_process()
        self.process_scheduling()

        return True

    def sem_acquire(self,info):
        """Acquire one of the semaphores
        """
        runningProcess = self.cpu.running_process
        if  not self.semaphore[int(info['semaphore'])].wait(runningProcess): # we need to wait

            pid = runningProcess.process_id

            # remove all events from the running process
            for event in runningProcess.events:
                if event['time'] in self.events:
                    del self.events[event['time']]

            # remove the process from cpu
            self.cpu.remove_process()
            self.process_scheduling()

        return True

    def sem_release(self,info):
        """Release one of the semaphores
        """
        currentProcess = self.cpu.running_process
        process = self.semaphore[int(info['semaphore'])].signal()

        if process != None:  # wake up the process
            process.priority = 1
            self.ready.new(process)  # insert in ready queue
            self.process_scheduling()

        return True

    def terminate(self, info):
        """Terminates current running process
        """
        self.memory.deallocate(self.cpu.running_process.process_id)
        self.cpu.running_process.com_time = self.cpu.system_clock.current_time()
        self.finished.append(self.cpu.running_process)
        # remove all remaining event for this process
        for event in self.cpu.running_process.events:
            if event['time'] in self.events:
                del self.events[event['time']]
            else:
                pass
        self.cpu.remove_process()
        self.job_scheduling()

        return True

    def expire(self, info):
        runningProcess = self.cpu.running_process
        runningProcess.priority = 0   # get priority down
        runningProcess.cpu_time = 300

        for event in runningProcess.events:
            if event['time'] in self.events:
                del self.events[event['time']]

        self.cpu.remove_process()
        self.ready.new(runningProcess)  # insert in ready queue

        self.process_scheduling()

        return True

    def ioComplete(self, info):
        # get list of processes completed at this time
        completeProcess = self.io_queue[info['time']]
        for process in completeProcess:
            process.priority = 1
            self.ready.new(process)

            # now put this process into the ready list

            #if self.cpu.busy():
            #    removed = self.cpu.remove_process()['pid']
            #else:
            #    removed = None

            #self.cpu.run_process(process)


            #if removed != None:
            #    self.ready.new(removed)

        self.process_scheduling()
        return True

###################################################################################################

# === Class: Simulator===

class Simulator(object):
    """
    Not quite sure yet
    """
    def __init__(self, **kwargs):

        # Must have input file to continue
        if 'input_file' in kwargs:
            self.input_file = kwargs['input_file']
        else:
            raise Exception("Input file needed for simulator")
        
        # Can pass a start time in to init the system clock.
        if 'start_clock' in kwargs:
            self.input_file = kwargs['start_clock']
        else:
            self.start_clock = 0

        internalEvents = {}

        outfile = sys.stdout # open(kwargs['output_file'], "w")

        # Read jobs in apriori from input file.
        self.jobs_dict = load_process_file(self.input_file,return_type="Dict")

        # create system clock and do a hard reset it to make sure
        # its a fresh instance. 
        self.system_clock = Clock()
        self.system_clock.hard_reset(self.start_clock)

        # Initialize all the components of the system. 
        self.scheduler = Scheduler(jobs = internalEvents)    
        self.memory = Memory()
        self.cpu = Cpu()
        self.accounting = SystemAccounting()

        # This dictionary holds key->value pairs where the key is the "event" from the input
        # file, and the value = the "function" to be called.
        # A = new process enters system             -> calls scheduler.new_process
        # D = Display status of simulator           -> calls display_status
        # I = Process currently on cpu performs I/O -> calls scheduler.perform_io 
        # S = Semaphore signal (release)            -> calls scheduler.sem_acquire
        # W = Semaphore wait (acquire)              -> calls scheduler.sem_release
        self.event_dispatcher = {
            'A': self.scheduler.new_process,
            'D': self.display_status,
            'I': self.scheduler.perform_io,
            'W': self.scheduler.sem_acquire,
            'S': self.scheduler.sem_release,
            'T': self.scheduler.terminate,
            'E': self.scheduler.expire,
            'C': self.scheduler.ioComplete
        }

        # Start processing jobs:
        
        # While there are still jobs to be processed
        while len(self.jobs_dict) > 0 or len(internalEvents) > 0:
            # Events are stored in dictionary with time as the key
            key = str(self.system_clock.current_time())

            # solve internal events first
            if key in internalEvents:
                if len(internalEvents[key]) > 1:
                    key = key
                for event in internalEvents[key]:
                    event_data = event
                    event_type = event_data['event']

                    outfile.write("Event: %s   Time: %s\n" % (event_data['event'], event_data['time']))
                    # Call appropriate function based on event type
                    result = self.event_dispatcher[event_type](event_data)
                    if result != True:
                        outfile.write("%s\n"%result)

            # If current time is a key in dictionary, run that event.
            if key in self.jobs_dict.keys():
                event_data = self.jobs_dict[key]
                event_type = event_data['event']

                outfile.write("Event: %s   Time: %s\n" % (event_data['event'], event_data['time']))

                # Call appropriate function based on event type
                result = self.event_dispatcher[event_type](event_data)
                if result != True:
                    outfile.write("%s\n"%result)

                # Remove job from dictionary
                del self.jobs_dict[key]

            self.system_clock += 1

            if self.cpu.running_process != None:
                self.cpu.running_process.burstLeft -= 1
                self.cpu.running_process.cpu_time -= 1

        outfile.write("\nThe contents of the FINAL FINISHED LIST\n---------------------------------------\n\nJob #  Arr. Time  Mem. Req.  Run Time  Start Time  Com. Time\n-----  ---------  ---------  --------  ----------  ---------\n\n")
        total_turnaround = 0
        total_wait = 0
        total_schedule = 0
        n_finished = 0
        for finished in self.scheduler.finished:
            outfile.write("%5d  %9d  %9d  %8d  %10d  %9d\n"%(int(finished.process_id), 
                                                         int(finished.time), 
                                                         int(finished.mem_required),
                                                         int(finished.burst_time),
                                                         int(finished.startTime),
                                                         finished.com_time))
            total_turnaround += finished.com_time - int(finished.time)
            total_wait += int(finished.inScheduleTime) - int(finished.time)
            n_finished += 1

        outfile.write("\n\n")

        avg_turnaround = total_turnaround / n_finished 
        avgWait = total_wait / n_finished 
        outfile.write("The Average Turnaround Time for the simulation was %.3f units.\n\n"%avg_turnaround)
        outfile.write("The Average Job Scheduling Wait Time for the simulation was %.3f units.\n\n"%avgWait)
        outfile.write("There are %d blocks of main memory available in the system.\n\n"%(self.memory.available()))

        outfile.close()

    def display_job(self, p):
        return "%5d %10d %10d %9d"%(int(p.process_id), int(p.time), int(p.mem_required), int(p.burst_time))

    def display_process_table(self, table):
        if table.empty():
            return "The Job Scheduling Queue is empty.\n"
        else:
            result = "Job #  Arr. Time  Mem. Req.  Run Time\n-----  ---------  ---------  --------\n\n"
            for row in table:
                result += self.display_job(row)+"\n"
            return result

    def display_semaphore(self, n):
        numbers = ["ZERO", "ONE", "TWO", "THREE", "FOUR"]
        header = "The contents of SEMAPHORE %s"%numbers[n]
        result = header+"\n"+("-"*len(header))+"\n\n"
        result += "The value of semaphore %d is %d.\n\n"%(n, self.scheduler.semaphore[n].value)
        if self.scheduler.semaphore[n].waitqueue.empty():
            result += "The wait queue for semaphore %d is empty.\n\n\n"%n
        else:
            for process in self.scheduler.semaphore[n].waitqueue.Q:
                result += str(process.process_id) + "\n"
            result += "\n\n"
        return result

    def display_status(self,info):
        status = "\n************************************************************\n\n"
        status += "The status of the simulator at time %s.\n\n"%info['time']
        status += "The contents of the JOB SCHEDULING QUEUE\n----------------------------------------\n\n"
        status += self.display_process_table(self.scheduler.job_scheduling_queue)   

        status += "\n\nThe contents of the FIRST LEVEL READY QUEUE\n-------------------------------------------\n\n"
        if self.scheduler.ready.queues[1].empty():
            status += "The First Level Ready Queue is empty.\n\n\n"
        else:
            status += self.display_process_table(self.scheduler.ready.queues[1])
            status += "\n\n"

        status += "The contents of the SECOND LEVEL READY QUEUE\n--------------------------------------------\n\n"
        if self.scheduler.ready.queues[0].empty():
            status += "The Second Level Ready Queue is empty.\n\n\n"
        else:
            status += self.display_process_table(self.scheduler.ready.queues[0])
            status += "\n\n"

        status += "The contents of the I/O WAIT QUEUE\n----------------------------------\n\n"

        jobs = []
        for time in self.scheduler.io_queue:
            if int(time) > self.system_clock.current_time():
                for job in self.scheduler.io_queue[time]:
                    #comp_time = job.
                    pid     = int(job.process_id)
                    arrtime = int(job.time)
                    memreq  = int(job.mem_required)
                    runtime = int(job.burst_time)
                    ioStart = job.iostart
                    ioBurst = job.ioburst
                    ioComp  = ioStart + ioBurst
                    jobs.append([ioComp, pid, arrtime, memreq, runtime, ioStart, ioBurst])

        if len(jobs)==0:
            status += "The I/O Wait Queue is empty.\n\n\n"
        else:
            status += "Job #  Arr. Time  Mem. Req.  Run Time  IO Start Time  IO Burst  Comp. Time\n"
            status += "-----  ---------  ---------  --------  -------------  --------  ----------\n\n"

            jobs.sort()
            for job in jobs:
                status += "%5d  %9d  %9d  %8d  %13d  %8d  %10d\n"%(job[1],
                                                                    job[2],
                                                                    job[3],
                                                                    job[4],
                                                                    job[5],
                                                                    job[6],
                                                                    job[0])
            status += "\n\n"

        for i in range(5):
            status += self.display_semaphore(i)

        currentProcess = self.cpu.running_process
        status += "The CPU  Start Time  CPU burst time left\n-------  ----------  -------------------\n\n"

        if currentProcess == None:
            status += "The CPU is idle.\n"
        else:
            burstLeft = currentProcess.burstLeft
            status += "%7d  %10d  %19d\n"%(int(currentProcess.process_id),int(currentProcess.startTime),burstLeft)

        status += "\n\nThe contents of the FINISHED LIST\n---------------------------------\n\n"
        status += "Job #  Arr. Time  Mem. Req.  Run Time  Start Time  Com. Time\n-----  ---------  ---------  --------  ----------  ---------\n\n"

        for finished in self.scheduler.finished:
            status += "%5d  %9d  %9d  %8d  %10d  %9d\n"%(int(finished.process_id), 
                                                         int(finished.time), 
                                                         int(finished.mem_required),
                                                         int(finished.burst_time),
                                                         int(finished.startTime),
                                                         finished.com_time)

        status += "\n\nThere are %d blocks of main memory available in the system.\n"%(self.memory.available())

        return status

    def __str__(self):
        """
        Visual dump of class state.
        """
        return my_str(self)


###################################################################################################
# Test Functions
###################################################################################################

def run_tests():
    print("############################################################")
    print("Running ALL tests .....\n")

    test_process_class()
    test_class_clock()
    test_cpu_class()
    test_memory_class()
    test_semaphore_class()


if __name__ == '__main__':

    file_name1 = os.path.dirname(os.path.realpath(__file__))+'/input_data/jobs_in_c.txt'

    S = Simulator(input_file=file_name1)
    
