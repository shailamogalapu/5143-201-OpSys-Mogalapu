import os
import sys
import stat
import time
import shutil

"""
@Name: historyManager
@Description:
    Maintains a history of shell commands to be used within a shell environment.
@Methods:
    push_command - add command to history
    get_commands - get all commands from history
    number_commands - get number of commands in history
"""


class historyManager(object):
    def __init__(self):
        self.command_history = []
    """
    @Name: push_command
    @Description:
        Add command to history
    @Params:
        cmd (string) - Command added to history
    @Returns: None
    """

    def push_command(self,cmd):
        self.command_history.append(cmd)
    """
    @Name: get_commands
    @Description:
        get all commands from history
    @Params: None
    @Returns: None
    """    
 
    def get_commands(self):
        return self.command_history
    

    """
    @Name: number_commands
    @Description:
        get number of commands in history
    @Params: None
    @Returns: 
        (int) - number of commands
    """ 

    def number_commands(self):
        return len(self.command_history)


"""
@Name: parserManager
@Description:
    Handles parsing of commands into command , arguments, flags.
@Methods:
    parse - does actual parsing of command
"""

class parserManager(object):
    def __init__(self):
        self.parts = []
    """
    @Name: parse
    @Description:
        Parses command into a list (right now). 
    @Params: 
        cmd (string) - The command to be parsed
    @Returns: 
        (int) - number of commands
    """
    def parse(self,cmd):
        self.parts = cmd.split(" ")
        return self.parts
        
"""
@Name: commandManager
@Description:
    Maintains a history of shell commands to be used within a shell environment.
@Methods:
    run_command - Runs a parsed command
    ls - Directory_listing
    cat - File dump
"""
class commandManager(parserManager):
    def __init__(self):
        self.command = None

    """
    @Name: run_command
    @Description:
        Runs a parsed command
    @Params: 
        cmd (string) - The command
    @Returns: 
        (list) - With the command parts (It shouldn't return the list, it should RUN the appropriate command from this method.
    """
    def run_command(self,cmd):
        self.command = cmd
        self.command = self.parse(self.command)
        return self.command

    """
    @Name: ls
    @Description:
        Does a directory listing
    @Params: 
        dir (string) - The directory to be listed
    @Returns: None
    """
    def ls(self):
        for dirname, dirnames, filenames in os.walk('.'):
            for subdirname in dirnames:
                print(os.path.join(dirname,subdirname))
        for filename in filenames:
            print(os.path.join(dirname, filename))
    
    
    """
    @Name: lsfun
    @Description:
        Does a directory listing
    @Params:
        flag (string) - type of flag
    @Returns: None
    """
    def lsfun(self,flag):
        files_list=[]
        for filename in os.listdir('.'):
            file_stats=os.stat(filename)
            file_list = [
            filename,
            file_stats [stat.ST_SIZE],
            oct(stat.S_IMODE(file_stats.st_mode)),
            time.strftime("%b:%d:%Y %H:%M:%S", time.gmtime(os.path.getmtime(filename))),
            time.strftime("%b:%d:%Y %H:%M:%S", time.gmtime(os.path.getatime(filename))),
            time.strftime("%b:%d:%Y %H:%M:%S", time.gmtime(os.path.getctime(filename)))
            ]
            files_list.append(file_list)
        
        #flag is -l 
        if(flag=='-l'):
          print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("FileName","Size","Permission","ModifyTime","AccessTime","CreationTime")
          print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("---------","---------","--------","--------","--------","--------")
          for file in files_list:
              print '{0:20} {1:5} {2:10} {3:15} {4:5} {5:25}'.format(file[0],file[1],file[2],file[3],file[4],file[5])
        #flag is -s
        elif(flag=='-s'):
            files_list.sort(key=lambda x:int(x[1]))
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("FileName","Size","Permission","ModifyTime","AccessTime","CreationTime")
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("---------","---------","--------","--------","--------","--------")
            for file in files_list:
                print '{0:20} {1:5} {2:10} {3:15} {4:5} {5:25}'.format(file[0],file[1],file[2],file[3],file[4],file[5])
        #flag is -m
        elif(flag=='-m'):
            files_list.sort(key=lambda x:time.strftime(x[3]))
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("FileName","Size","Permission","ModifyTime","AccessTime","CreationTime")
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("---------","---------","--------","--------","--------","--------")
            for file in files_list:
                print '{0:20} {1:5} {2:10} {3:15} {4:5} {5:25}'.format(file[0],file[1],file[2],file[3],file[4],file[5])
        #flag is -a
        elif(flag=='-a'):
            files_list.sort(key=lambda x:time.strftime(x[4]))
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("FileName","Size","Permission","ModifyTime","AccessTime","CreationTime")
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("---------","---------","--------","--------","--------","--------")
            for file in files_list:
                print '{0:20} {1:5} {2:10} {3:15} {4:5} {5:25}'.format(file[0],file[1],file[2],file[3],file[4],file[5])
        #flag is -c
        elif(flag=='-c'):
            files_list.sort(key=lambda x:time.strftime(x[5]))
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("FileName","Size","Permission","ModifyTime","AccessTime","CreationTime")
            print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("---------","---------","--------","--------","--------","--------")
            for file in files_list:
                print '{0:20} {1:5} {2:10} {3:15} {4:5} {5:25}'.format(file[0],file[1],file[2],file[3],file[4],file[5])
        
        else:
            print("flag is not recognised")

    """
    method : copy
    desc: copies to new file
    """

    def cp(self,inputfile,outputfile):
            shutil.copy(inputfile,outputfile)
            print("successfully copied to new file!!")
    """
    method :chmod
    desc : change file permission
    """
    def chmod(self,inputfile,mode):
        os.chmod(inputfile,mode);
        print("file mode has changed!!")
               

    """
    method : cd
    desc : change directory
    """

        
    def cd(self,directory):
        if directory=='..':
            os.chdir('..')
            new=os.getcwd()
            print(new)
        elif directory=='~':
            home=os.path.expanduser('~')
            os.chdir(home)
            new=os.getcwd()
            print(new)
        else:
            if os.path.isdir(directory):
                os.chdir(directory)
                new=os.getcwd()
                print(new)
            else:
                print("directory  does not exist")

    """
    method : wc
    desc : word count
    """
    def wc(self,flag,file):
        if(os.path.isfile(file)):
            num_lines = 0
            num_words = 0
            num_chars = 0
            with open(file, 'r') as f:
                for line in f:
                    words = line.split()
                    num_lines += 1
                    num_words += len(words)
                    num_chars += len(line)
            if flag=="0":
                print(num_lines)
                print(num_words)
                print(num_chars)
            elif(flag=="-l"):
                print(num_lines)
            else:
                print("flag does not exist")
        else:
            print("file does not exist")

    """
    method : history
    desc : shows the history of commands
    """
    def history(self):
        his=historyManager.get_commands(self)
        return his
    
    """
    method : remove
    desc : removes file
    """
    def rm(self,file):
        if(os.path.isfile(file)):
            os.remove(file)
            print("file removed succesfully")
        else:
            print("file does not exist")

    """
    method : mv
    desc : rename file name
    """
    def mv(self,source,destination):
        if(os.path.isfile(source)):
            shutil.move(source,destination)
            print("file renamed succesfully")
        else:
            print("file does not exist")
            

    """
    method : cat
    desc : open a file in view mode
    """
    def cat(self,file):
        f = open(file,'r')
        print(f.read())
        
"""
@Name: driver
@Description:
    Drives the entire shell environment
@Methods:
    run_shell - Loop that drives the shel environment
"""
class driver(object):
    def __init__(self):
        self.history = historyManager()
        self.commands = commandManager()
        self.number_commands = 0
    """
    @Name: runShell
    @Description:
        Loop that drives the shel environment
    @Params: None
    @Returns: None
    """      
 
    def runShell(self):
        number_commands = 0
        while True:
            self.input = raw_input("parser-$" )         # get command
            self.history.push_command(self.input)   # put in history
            parts = self.commands.run_command(self.input)
            if parts[0]=='cat':
               if(len(parts)==1):
                 print("need a file name to view")
               elif len(parts)==2:
                    self.commands.cat(parts[1])
               else:
                    print("invalid cat command")
            elif parts[0]=='ls':
                if(len(parts)==1):
                    self.commands.ls()
                elif (len(parts)==2):
                    self.commands.lsfun(parts[1])
                else:
                    print("invalid ls command")
            elif parts[0]=='cp':
                if (len(parts)==1) |(len(parts)==2):
                    print("invalid or missing command arguments")
                elif(len(parts)==3):
                    self.commands.cp(parts[1],parts[2])
                else:
                    print("excess arguments passed for  cp command")
            elif parts[0]=='chmod':
                if len(parts)==1:
                   print("arguments need to be pass")
                elif(len(parts)==3):
                    self.commands.chmod(parts[2],int(parts[1]))
                else:
                    print("more arguments for c command")
            elif parts[0]=='cd':
                if (len(parts)==1) | (len(parts)>2):
                   print("invalid cd command")
                elif(len(parts)==2):
                    self.commands.cd(parts[1])
            elif parts[0]=='wc':
                if(len(parts)==1) | (len(parts)>3):
                  print("invalid wc command")
                elif(len(parts)==2):
                    self.commands.wc("0",parts[1])
                elif(len(parts)==3):
                    self.commands.wc(parts[2],parts[1])
            elif parts[0]=='rm':
                if(len(parts)==1) | (len(parts)>2):
                  print("invalid rm command")
                elif(len(parts)==2):
                    self.commands.rm(parts[1])
            elif parts[0]=='mv':
                if(len(parts)==1) | (len(parts)==2) | (len(parts)>3):
                  print("invalid move command")
                elif(len(parts)==3):
                    self.commands.mv(parts[1],parts[2])
            elif parts[0]=='history':
                his=self.history.get_commands()
                if(len(parts)>1):
                  print("invalid history command")
                elif(len(parts)==1):
                    for hiscmd in his:
                        print(hiscmd)
            elif parts[0]=='exit()':
			print "******************"
			print "Exits parser"
			raise SystemExit    
            else:
                print("ERROR: Command not found")
                


if __name__=="__main__":
    d = driver()    
    d.runShell()
