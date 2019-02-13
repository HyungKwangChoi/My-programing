#Reference in korean
#https://cds0915.blog.me/221251448909
#Reference in English
#https://www.michaelcho.me/article/using-pythons-watchdog-to-monitor-changes-to-a-directory
# python watchdog package 
#https://pypi.org/project/watchdog/
#
#Python Watchdog API reference
#https://pythonhosted.org/watchdog/



import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import threading
import ftplib
import os


def my_upload(ftp, filename):
  
    ext = os.path.splitext(filename)[1] #This is to separate download mode as Text/Binary. https://iamhoh.blog.me/221396426230
     # perform upload progress bar


    if ext in (".txt", ".htm", ".html"):
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb') #type must be 'rb'. If you set 'r', it returns an error.
            ftp.storlines("STOR " + filename ,fd))
            fd.close() # close file open or fd.quit()

        except:
             print ("Error occureddddddddddddddddddddddddd")

    else:
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb')
            ftp.storbinary("STOR " + filename ,fd, 1024)
            fd.close()

        except:
             print ("Error else")
  

class Watcher:
    DIRECTORY_TO_WATCH = "C:\\Python35\\studyrootm"

    def __init__(self):
        self.observer = Observer()
    
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        #print("**Monitoring Started**")
        try:
            print("**Monitoring Started**")
            while True:
                time.sleep(5)
                print("test\n")
        except KeyboardInterrupt:
            self.observer.stop()
            print("Keyboard interrupted")
        except:
            self.observer.stop()
            print("Something wrong")
        
        self.observer.join()

class Handler(FileSystemEventHandler):

    @staticmethod

    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            print("recevied a created event - %s." %event.src_path)

            filename = event.src_path.split('\\')[-1]
            dirname = event.src_path.split('\\')[-2]
            print(filename)
            print(dirname)

            myftp = ftplib.FTP("X.X.X.X") # put FTP server ip addr = ftplib.FTP('ip', 'id', 'pw')
            myftp.login("XX", "XXXXX")    # put ID and PW

          

            t = threading.Thread(target=my_upload(myftp, filename))
            t.start()
            
         

        elif event.event_type == 'deleted':
            print("recevied a delete event - %s." %event.src_path)

            filename = event.src_path.split('\\')[-1]
            dirname = event.src_path.split('\\')[-2]
            print(filename)
            print(dirname)
            
            myftp = ftplib.FTP("X.X.X.X") # put FTP server ip addr = ftplib.FTP('ip', 'id', 'pw')
            myftp.login("XX", "XXXXX")    # put ID and PW
            
            try:
                myftp.delete(filename)
                print("File successfully deleted.")
            except:
                print("please check if file exists or not")

            #t = threading.Thread(target=myftp.delete(filename))
            #t.start()

         
        # modified doesn't work..i don't know why
        #elif event.event_type == 'modified':
        #    print("recevied a modified event - %s." %event.src_path)

        #    filename = event.src_path.split('\\')[-1]
        #    dirname = event.src_path.split('\\')[-2]
        #    print(filename)
        #    print(dirname)

            #t = threading.Thread(target=my_upload(myftp, filename))
            #t.start()
            

        else:
            return None

if __name__ == '__main__':
    w = Watcher()
    w.run()