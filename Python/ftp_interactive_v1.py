#http://code.activestate.com/recipes/521925-python-ftp-client/


import sys
import ftplib
import os
 
myftp = ftplib.FTP("172.27.122.173") # or session = ftplib.FTP('ip', 'id', 'pw')
myftp.login("jun", "jun2per")

#############
#ftp = ftplib.FTP()
#ftp.connect('192.168.1.102',2233) You can separate port number like with method.
#
######################################################################
myftp.dir() # reading directory file list. or myFtp.dir("/var")
            # Another way to list up.
            #        data = []
            # 
            # myftp.dir(data.append)
            # 
            # myftp.quit()
            # 
            # for line in data:
            #     print "-", line
            #

def my_ownload(ftp, filename):
    ext = os.path.splitext(filename)[1] #This is to separate download mode as Text/Binary. https://iamhoh.blog.me/221396426230
    if ext in (".txt", ".htm", ".html"):
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'w')
            ftp.retrlines("RETR " + filename ,fd.write)
            fd.close()
                                                     # myftp.retrlines : for the Ascii file. 
            #myftp.retrbinary("RETR "+filename, fd.write)# myftp.retrlbinary : for binary, writing files to above open(), 주의핡것 "RETR " RETR에서 한간 안띄우면, permission 500에러뜸.

            #fd = open("C:\\Python35\\studyrootm\\" + filename, 'wb') #open() used for where/with what's name file will be saved in your PC/Mobile.
                                                                  #For the directory set, you have to use double "\\""
        except:
             print ("Error occureddddddddddddddddddddddddd")

    else:
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'wb')
            ftp.retrbinary("RETR " + filename ,fd.write)
            fd.close()

        except:
             print ("Error else")


def my_upload(ftp, filename):
    ext = os.path.splitext(filename)[1] #This is to separate download mode as Text/Binary. https://iamhoh.blog.me/221396426230
    if ext in (".txt", ".htm", ".html"):
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb') #type must be 'rb'. If you set 'r', it returns an error.
            ftp.storlines("STOR " + filename ,fd)
            fd.close()

        except:
             print ("Error occureddddddddddddddddddddddddd")

    else:
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb')
            ftp.storbinary("STOR " + filename ,fd, 1024)
            fd.close()

        except:
             print ("Error else")

#download = "ldp-trace.pcap"
#upload = "logging.txt"

#ROOT= '/var/home/jun'
#myftp.cwd(ROOT) : Chaning directory

while True:
    command = input("FTP>")
    if "get " in command:
        rf = command.replace("get ","")
        rf = rf.replace("\n","")
        my_ownload(myftp,rf)
        continue
    elif "put " in command:
        lf = command.replace("put ","")
        lf = lf.replace("\n","")
        my_upload(myftp,lf)
        #myftp.close()
        #myftp = FTP(host_name)
        #myftp.login(user,pwd)
        continue
    elif "mkdir " in command:
        mkdirname = command.replace("mkdir ","")
        mkdirname = mkdirname.replace("\n","")
        try: myftp.mkd(mkdirname)
        except:
            print ("Incorrect usage.")
            continue
        else:
            print("Directory created.")
            continue
    elif "rmdir " in command:
        rmdirname = command.replace("rmdir ","")
        rmdirname = rmdirname.replace("\n","")
        current = myftp.pwd()
        myftp.cwd(rmdirname)
        allfiles = myftp.nlst()
        for file in allfiles:
            try:
                myftp.delete(file)  
            except Exception:
                pass
            else:
                pass
        myftp.cwd(current)
        try:
            myftp.rmd(rmdirname)
        except Exception:
            print("All files within the directory have been deleted, but there is still another directory inside.  As deleting this directory automatically goes against true FTP protocol, you must manually delete it, before you can delete the entire directory.")
        else:
            print("Directory deleted.")
        continue
    elif command == "dir":
        myftp.dir()
        continue
    elif command == "ls" or command == "pwd":
        print(myftp.pwd())
        continue
#	elif "chdir " in command:
#		dirpath = command.replace("chdir ","")
#		dirpath = dirpath.replace("\n","")
#		myftp.cwd(dirpath)
#		print "Directory changed to " + dirpath
#		continue
    elif "cd" in command:
     #   ch = myftp.pwd()
      #  print(ch)
      
        index = len(command)
        #print(myftp.cwd(ch[0:9]))
        temp = command
        if "../" in command:
            print(command)
            try:
                for i in range(index,0,-3):
                     if temp[i-3:i] == "../":
                          print(temp[i-3:i])
                          myftp.cwd("../")
                          print(myftp.pwd())
                          continue
                     if i == 3:
                          print("you reached the last")
                          break 
                     else:
                          print("you put wrong character")
                          break
           #     print(myftp.pwd())
            #    print("One directory back.")
                continue
            except:
                print("wrong input, please add correctly.")
#			if(operator.contains(charset,dir[i])):
#				temp = temp[:-1]
#				if temp=="/":
#					myftp.cwd(temp)
#					print "One directory back."
        else:
                chdir = command.replace("cd ","")
                chdir = chdir.replace("\n","")
                try:
                    myftp.cwd(chdir)
                    print(myftp.pwd())
                except:
                    print("you put wrong character")
                continue
#	elif command == "rename":
#		fromname = raw_input("Current file name: ")
#		toname = raw_input("To be changed to: ")
#		myftp.rename(fromname,toname)
#		print "Successfully renamed."
#		continue
    elif "delete " in command:
        delfile = command.replace("delete ","")
        delfile = delfile.replace("\n","")
        try:
            myftp.delete(delfile)
            print("File successfully deleted.")
        except:
            print("please check if file exists or not")
        continue

        		
#	elif "size " in command:
#		szfile = command.replace("size ","")
#		szfile = szfile.replace("\n","")
#		print "The file is " + str(myftp.size(szfile)) + " bytes."
#		continue		
    elif command == "debug -b":
        myftp.set_debuglevel(1)
        print ("Debug mode set to base.")
        continue
    elif command == "debug -v":
        myftp.set_debuglevel(2)
        print ("Debug mode set to verbose.")
        continue
    elif command == "debug -o":
        myftp.set_debuglevel(0)
        print ("Debug mode turned off.")
        continue
    elif command == "help" or command == "h":
        print ("debug -o - turns off debug output\n")
        print ("debug -v - turns the debug output to verbose mode\n")
        print ("debug -b - turns the debug output to base\n")
		#print ("size [filename] - returns the size in bytes of the specified file")
        print ("exit or quit - terminate the ftp session\n")
        print ("delete [filename] - delete a file\n")
		#print ("rename - rename a file\n")
        print ("cd directory or path or ../ navigate 1 directory up\n")
		#print ("chdir [path] - change which directory you're in\n")
        print ("pwd - prints the path of the directory you are currently in\n")
        print ("ls or pwd - lists the contents of the directory\n")
        print ("rmdir [directory path] - removes/deletes an entire directory\n")
        print ("mkdir [directory path] - creates a new directory\n")
        print ("put [filename] - stores a local file onto the server (does not work with microsoft office document types)\n")
        print ("get [filename] - download a remote file onto your computer\n\n")
        continue

    elif command == "exit" or command == "quit":
        
        print ("Session closed.")
        sys.exit()

    else:
    	print ("Sorry, invalid command.  Check 'help' for proper usage.")
     

myftp.quit()



##############################################
#http://zetcode.com/python/ftp/
#http://code.activestate.com/recipes/521925-python-ftp-client/
#ftp.dir()  : 목록을 가져옴
#
#ftp.rename('test.tgz','t.tgz')  : 파일 명을 바꿈
#
#ftp.delete('t.tgz') : 파일삭제
#
#ftp.pwd() :현재 디렉토리 출력
#
#ftp.mkd('k1rha') : 디렉토리만들기. 
#
#ftp.cwd('file') : 디렉토리로 들어가기 
#
#
# * Reference : OS
# https://iamhoh.blog.me/221396426230
#################################################