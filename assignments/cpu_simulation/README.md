>Group Members
>
| Name    | Email   | Github Username |
|----------|---------|-----------------|
|  Keerthi Reddy Gangidi  | kittu.tintu07@gmail.com | gangidikeerthireddy  |
|  Lavanya Mengaraboina  | lavanyamengaraboina@gmail.com | LavanyaMengaraboina  |
|  Shaila Mogalapu | sweety.shailamogalapu@gmail.com | shailamogalapu |
### Structure of files:    
In a directory called cpu_simulation, we placed the files in this format.    
### Components(directory)    
	   __init__.py    
	  accounting.py    
	  clock.py    
	  cpu.py     
	  fifo.py    
	  memory.py    
	  process.py    
	  run_all.py    
	  semaphore.py    
	  sim_components.py    
### input_data(directory)      
	  jobs_in_c.txt     
### simulation.py(main driver file)     
All the code is added only to simulation.py file.    
Run as python simulation.py    
### Structure of simulation.py    
### simulation.py    
### class MLFQ:    
	  __init__    
	  new     
	  nextProcess      
	  __str__     
### class Scheduler:     
  	__init__    
	  new_process     
	  job_scheduling     
	  process_scheduling     
	  newEvent     
	  perform_io     
	  sem_acquire     
	  sem_release     
	  terminate      
	  expire     
	  ioComplete      
### class Simulator:      
  	__init__     
	  display_job     
	  display_process_table     
	  display_semaphore    
	  display_status     
	  __str__     
### run_tests     
### main  
     
     
### Addition of print statements:     
The addition of print statements is done by concatenation and formatting      
The following are the sources looked at for this formatting:     
https://www.google.com/search?tbm=bks&hl=en&q=python+print#hl=en&q=print+statements+in+python+concatenate     
https://dzone.com/articles/python-formating    
http://www.python-course.eu/python3_formatted_output.php     
http://stackoverflow.com/questions/12169839/which-is-the-preferred-way-to-concatenate-a-string-in-python     
https://waymoot.org/home/python_string/     
   
