import threading
import os
import sys
import stat
import time
import shutil
import subprocess

command_history = []
command_new=[]


def previoushistory(file):
	x1=[]
	y=[]
	x1=list(file)
	del x1[0]
	files=''.join(x1)
	l=len(command_history)
	for i in range(l):
		if (command_new[i]==files):
			index=i
	cmd1 = command_history[index]
	print cmd1
	y=cmd1.split(" ")
	print y[0]
	length= len(y)
	file1=eval(y[0])

	if length==1:
		print "in if"
	#	file1=getattr(y[0])
		t=threading.Thread(target=file1)
		t.start()
		t.join()
	elif length==2:
		file2=y[1]
		print file2
		t=threading.Thread(target=file1,args=(file2,))
		t.start()
		t.join()
	elif length==3:
		file2=y[1]
		file3=y[2] 
		t=threading.Thread(target=file1,args=(file2,file1,))
                t.start()
                t.join()
	elif length==4:
		file2=y[1]
                file3=y[2]
		file4=y[3]
		t.threading.Thread(target=file1,args=(file2,file3,file4,))
		t.start()
		t.join()
#	c=threading.Thread(target=
	
	#	else:
	#		print "didnot find"
def less(filename):
	if os.path.exists(filename):                                           
		f = open(filename, "r")
		text = f.readline()
		lines=0
		for line in f:
			if lines==20:	
				user = raw_input("type in yes to continue ")
				if user == "yes":
					lines = 0
					continue
				else:	
					break
			else :
				print line
				lines=lines+1
	else:
		print("file doesnt exists")
def grep(filename,searchphrase):
	 if os.path.exists(filename):
	 	searchfile = open(filename)
		for line in searchfile:
   		 if searchphrase in line: 
			print line
		 else:
			print("keyword doesnt exist")
		searchfile.close()
	 else:
		print("file doesnot exist")
def tail(filename):
	 if os.path.exists(filename):
		nlines=-10
		lines=open(filename,'r').readlines()
		tot_lines = len(lines)
      		for i in range(nlines,0):
        		print lines[i]
	 else:
		print("file doesnt exists")
def who():
	print(os.popen('who').read())
def ls():
        for dirname, dirnames, filenames in os.walk('.'):
            for subdirname in dirnames:
                print(os.path.join(dirname,subdirname))
        for filename in filenames:
            print(os.path.join(dirname, filename))

def history():
	print(command_history)

def cat(filename):
	if os.path.exists(filename):
		f = open(filename, "r")
		text = f.read()
		print text
		f.close()
	else:
		print("File doesn't exist")
def cat1(filename1,filename2,filedest):
     if os.path.exists(filename1):
	if os.path.exists(filename2):
		fread=open(filename1,'r')
        	content=fread.read()
        	fread1=open(filename2,'r')
		content1=fread1.read()
		fread2=open(filedest,'w')
      	        fread2.write(content)
         	fread2.write(content1)
                fread.close()
                fread1.close()
        	fread2.close()
        else:
        	print("file doesnt exist")
     else:
		print("file doesnt exist")
def redirect(file):
        original = sys.stdout
        sys.stdout = open(file, 'w')

def chmod(_flag1,_flag2):
	permission=int(_flag1,8)
        print permission
        os.chmod(_flag2,permission)
        print("changed permission of")
        print(_flag2)
def mv(filename1,filename2):
	 if(os.path.isfile(filename1)):
		cp(filename1,filename2)
        	rm(filename1)
       	        print "Moved the file"
	 else:
		print("files doesnt exist")
def cp(filename1,filename2):
        path=os.getcwd()
        conc=path+'\%s'%filename1
        if os.path.exists(filename1):
        	fread=open(filename1,'r')
                content=fread.read()
                fread1=open(filename2,'w')
                fread1.write(content)
		print("succesfully made a copy of the file")
                fread.close()
                fread1.close() 
	else:
		print("file doesnt exist")
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
	 if os.path.exists(file):
		with open(file) as f:
			for line in sorted(f):
        			print (line)
	 else:
		print("file doesnt exist")
def head(filename):
	  if os.path.exists(filename):
                nlines=10
                lines=open(filename,'r').readlines()
                tot_lines = len(lines)
                for i in range(0,nlines):
                        print lines[i]
          else:
                print("file doesnt exists")
"""@
	 if os.path.exists(file):
		with open(file,'r') as f:
			lines=f.readlines()[0:3]
        	print (lines)
    	 else:
		print("file doesnt exist")	
"""	
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
	if not os.path.exists(directory):
		print("directory is not present")
	else:
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
		print("number of line:")
                print(num_lines)
		print("number of words:")
                print(num_words)
		print("number of characters:")
                print(num_chars)
		print("filename:")
		print(file)
        else:
            print("file does not exist")

def pwd():
		print(os.getcwd())
		return

if __name__=="__main__":
	number_commands = 0
	while True:
          parts = []
	  x=[]
	  cmd = raw_input("parser-$" )
	  parts=cmd.split(" ")
	  command_history.append(cmd)
	  command_new.append(parts[0])
	  x=list(parts[0])
	  if parts[0]=='rm':
                if(len(parts)==1) | (len(parts)>2):
                  print("invalid rm command")
                elif(len(parts)==2):
                   files=parts[1]
		   c=threading.Thread(target=rm,args=(files,))
		   c.start()
		   c.join()
	  elif parts[0] == 'pwd':
			c = threading.Thread(target=pwd)
			c.start()
			c.join()
	  elif parts[0] == 'mv':
			file1 = parts[1]
			file2 = parts[2]
			c = threading.Thread(target=mv, args=(file1, file2,))
			c.start()
			c.join()
	  elif parts[0]=='tail':
		     c=threading.Thread(target=tail,args=(parts[1],))
		     c.start()
		     c.join()
	  elif parts[0]=='grep':
		     c=threading.Thread(target=grep,args=(parts[2],parts[1],))
		     c.start()
		     c.join()
	  elif x[0]=='!':
		    # print parts[0]
		     c=threading.Thread(target=previoushistory,args=(parts[0],))
		     c.start()
		     c.join()
	  elif parts[1]=='>':
                    # print parts[0]
		     output=subprocess.check_output(parts[0],parts[2])
		     print output
		     c=threading.Thread(target=parts[0])
                     c.start()
                     c.join()
                     c=threading.Thread(target=redirect,args=(parts[2],))
                     c.start()
                     c.join()

	  elif parts[0]=='less':
                     c=threading.Thread(target=less,args=(parts[1],))
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
		    files=parts[2]
		    c=threading.Thread(target=redirect,args=(files,))
		    c.start()
		    c.join()
                   # print("invalid ls command")
	  elif parts[0]=='history':
           if len(parts)==1:
              c=threading.Thread(target=history)
	      c.start()
	      c.join()
           else:
	      print("Needs only 1 arguments")
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
		if (len(parts)==2):
			file = parts[1]
			c = threading.Thread(target=cat, args=(file,))
			c.start()
			c.join()
		elif (len(parts)==5):
		 file1=parts[1]
		 file2=parts[2]
		 file3=parts[4]
		 c=threading.Thread(target=cat1,args=(file1,file2,file3,))
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
