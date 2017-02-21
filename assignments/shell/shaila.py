import threading
import os
import sys
import stat
import time
import shutil

def who():
	print(os.popen('who').read())
def ls():
        for dirname, dirnames, filenames in os.walk('.'):
            for subdirname in dirnames:
                print(os.path.join(dirname,subdirname))
        for filename in filenames:
            print(os.path.join(dirname, filename))
class historyManager:
	command_history=[]
	def push_command(cmd):
       	 command_history.append(cmd) 
	def get_commands():
         return command_history
	def number_commands():
       	 return len(command_history)

def history():
        his=historyManager.get_commands()
        return his
def cat(filename):
		if os.path.exists(filename):
			f = open(filename, "r")
			text = f.read()
			print text
			f.close()
		else:
			print("File doesn't exist")
def chmod(_flag1,_flag2):
                sum=[0,0,0]
                for i in range(len(_flag1)):
                        if int(_flag1[i])<=7 and int(_flag1[i])>=0:
                                sum[i]=3
                        else:
                                print "Syntax Error"
                                return None
				print sum
				print len(_flag1)
                if os.path.exists(_flag2) and (sum[i]<=3 for w in sum):
                        os.chmod(_flag2,int(_flag1,8))
                        print "Permissions changed successfully"
                else:
                        print "Check the syntax or Filename"	
def mv(filename1,filename2):
                cp(filename1,filename2)
                rm(filename1)
                print "Moved the file"
def cp(filename1,filename2):
                path=os.getcwd()
                conc=path+'\%s'%filename1
                if os.path.exists(filename1):
                        fread=open(filename1,'r')
                        content=fread.read()
                        fread1=open(filename2,'w')
                        fread1.write(content)
                        fread.close()
                        fread1.close() 
def lsfun(flag):
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
	if(flag=='-l'):
          print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("FileName","Size","Permission","ModifyTime","AccessTime","CreationTime")
          print '{0:20} {1:8} {2:10} {3:35} {4:10} {5:25}'.format("---------","---------","--------","--------","--------","--------")
          for file in files_list:
              print '{0:20} {1:5} {2:10} {3:15} {4:5} {5:25}'.format(file[0],file[1],file[2],file[3],file[4],file[5])
	elif(flag=='-a'):
            files_list.sort(key=lambda x:time.strftime(x[4]))
            for file in files_list:
                print (file[0])
	else:
            print("flag is not recognised")
def sort(file):
	with open(file) as f:
	 for line in sorted(f):
        	print (line)
def head(file):
	with open(file) as f:
		lines=f.readlines()[0:3]
        print (lines)
    			
def rm(file):
        if(os.path.isfile(file)):
            os.remove(file)
            print("file removed succesfully")
        else:
            print("file does not exist")
def cd(directory):
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
def mkdir(directory):
	if not os.path.exists(directory):
		os.makedirs(directory)
		print("directory has been created")
	else:
	        print("directory already exists")
def rmdir(directory):
		shutil.rmtree(directory)
		print(" directory has been removed")
def wc(file):
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
                print(num_lines)
                print(num_words)
                print(num_chars)
		print(file)
        else:
            print("file does not exist")

def pwd():
		print(os.getcwd())
		return

if __name__=="__main__":
	number_commands = 0
#	history1=historyManager()
	while True:
          parts = []
	  cmd = raw_input("parser-$" )
#	  history1.push_command(cmd) 
	  parts=cmd.split(" ")
	 # history1.push_command(parts[0])
	  if parts[0]=='rm':
                if(len(parts)==1) | (len(parts)>2):
                  print("invalid rm command")
                elif(len(parts)==2):
                   files=parts[1]
		   c=threading.Thread(target=rm,args=(files,))
		   c.start()
		   c.join()
	  if parts[0] == 'pwd':
			c = threading.Thread(target=pwd)
			c.start()
			c.join()
	  elif parts[0] == 'mv':
			file1 = parts[1]
			file2 = parts[2]
			c = threading.Thread(target=mv, args=(file1, file2,))
			c.start()
			c.join()
	  elif parts[0]=='ls':
                if(len(parts)==1):
                    c=threading.Thread(target=ls)
		    c.start()
		    c.join()
                elif (len(parts)==2):
		    files=parts[1]
                    c=threading.Thread(target=lsfun,args=(files,))
		    c.start()
		    c.join()
                else:
                    print("invalid ls command")
	  elif parts[0] == 'who':
		c = threading.Thread(target=who)
		c.start()
		c.join()
	  elif parts[0]=='cd':
                if (len(parts)==1) | (len(parts)>2):
                   print("invalid cd command")
                elif(len(parts)==2):
                    files=parts[1]
		    c=threading.Thread(target=cd,args=(files,))
		    c.start()
		    c.join()
	  elif parts[0] == 'cat':
			file = parts[1]
			c = threading.Thread(target=cat, args=(file,))
			c.start()
			c.join()
          elif parts[0] == 'chmod':
			flag1 = parts[1]
			flag2 = parts[2]
			c = threading.Thread(target=chmod, args=(flag1, flag2,))
			c.start()
			c.join()			
	  elif parts[0] == 'cp':
			file1 =parts[1]
			file2 = parts[2]
			c = threading.Thread(target=cp, args=(file1,file2,))
			c.start()
			c.join()
	  elif parts[0]=='wc':
                if(len(parts)==1) | (len(parts)>2):
                  print("invalid wc command")
                elif(len(parts)==2):
		    files=parts[1]
		    c=threading.Thread(target=wc,args=(files,))
                    c.start()
		    c.join()
	  elif parts[0]=='sort':
		files=parts[1]
		c=threading.Thread(target=sort,args=(files,))
		c.start()
		c.join()
	  elif parts[0]=='head':
		files=parts[1]
		c=threading.Thread(target=head,args=(files,))
		c.start()
		c.join()
	  elif parts[0] == 'mkdir':
			files = parts[1]
			c = threading.Thread(target=mkdir,args=(files,))
			c.start()
			c.join()
	  elif parts[0]=='rmdir':
		files=parts[1]
		c=threading.Thread(target=rmdir,args=(files,))
		c.start()
		c.join()
	  elif parts[0]=='history':
                his=history1.get_commands()
                if(len(parts)>1):
                  print("invalid history command")
                elif(len(parts)==1):
                    for hiscmd in his:
                        print(hiscmd)
	  elif parts[0]=='exit()':
			print "******************"
			print "Exiting shell"
			raise SystemExit    
          else:
                print("ERROR: Command not found")
