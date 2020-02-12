"""
Written by 

1. History
   2019. 8
     - "Tools for Networkers_v1"
   2020.1
     - "Tools for Networkers_v2.1"

2. Author
   HyungKwang (s99225078@gmail.com)

"""

import sys
import time
import threading  #This is for multi-threading
import datetime
import io
from contextlib import redirect_stdout #This is to redirect stdout
from multiprocessing import Process #This is for multi-processing
#import multiprocessing
#https://docs.python.org/2/library/multiprocessing.html#multiprocessing.Process.daemon
import os

import telnetlib         # This mainly used for TAB-1 such as telnet feature. 

# Third party lib.  For this, you have to install PYQT5. Please refer to the "release_note_v2.1"
# PYQT5 is for GUI.
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtGui import QTextCursor #This is used for Qtextbrowzer scroll down feature. (self.textBrowser_2.moveCursor(QTextCursor.End))
from PyQt5.QtCore import QDateTime

#Third party lib. For this, you have to install scapy. For details, Please refer to the "release_note_v2.1"
from scapy.all import *  # This mainly used for TAB-2 such as packet building sending/receving.


    


def _sending_packets(cap_name,count,interval):    
    #name = multiprocessing.current_process().name
    #id = multiprocessing.current_process().pid
    #print(name, id)
    #print(os.getpid())

    if interval == 0:
        sendp(cap_name,loop=1)
    else :
        sendp(cap_name,count=count,inter=1./interval)
    #count=count, inter=1./interval,

    # The function "sned()" is for layer-3 packets
    # The function "sendp()" is for layer-2 packets
    # For fast speed testing in case you installed TCPreplay
    #    sendpfast(self.new_modified_packets, pps=1000, loop=10000, parse_results=1)
    
    # please refer to "help(sendpfast)" or "help(sendp)""
    # sending packets, please go through "https://scapy.readthedocs.io/en/latest/api/scapy.sendrecv.html#scapy.sendrecv.sendpfast"
    #Scapy has a sendpfast function that sends packets using tcpreplay. However, this function first creates a temporary pcap file and then calls tcpreplay on that.
    #  This adds too much delay. Is there anyway to bypass it and directly send data to tcpreplay. 
    # I know that tcpreplay can read data from STDIN



class Form(QtWidgets.QMainWindow):
       
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self,parent)
        root = os.path.dirname(os.path.realpath(__file__))
        self.ui = uic.loadUi(os.path.join(root, 'Window.ui'), self)#If the script is not working, please check the file directory, and Python env path such as)"\project\Tools for networks\Window.ui"
        self.ui.show()
        self.fileName = 'Null'  #This is for "Files" in Memu bar, initial value.
        self.actionSave_session.triggered.connect(self._savefiledialog)   # 'Files' in Memubar 
        
     #Initialization for TAB-1
        self.comboBox_2.addItem("Telnet") # In TAB-1 "How to access"
        self.lineEdit.text() # In TAB-1, "Put an ip address"
        self.lineEdit_2.text()# In TAB-1, "ID"
        self.lineEdit_3.text()# In TAB-1, "PW"
        self.lineEdit_4.text() #In TAB-1, "1). What commands to execute"
        self.lineEdit_5.setText("1") #In TAB-1, "3). How many times runnning"
        self.lineEdit_6.setText("1")#In TAB-1, "2). Time sleep (sec) Interleaving between commands (default 1sec)"
        self.dateTimeEdit # In TAB-1, "> Beginning"
        self.dateTimeEdit_2# In TAB-1, "> End"
        self._thread_1 = None #Initialization to the un-defined thread value Used for 'Repetitive Tasks'
        self._tl_1 = None     #Initialization to the un-defined Telnet object value Used for 'Repetitive Tasks'

     #Initialization for TAB-2
        self.lineEdit_7.setText("1") # In TAB-2, "3). The number of packets to send"
        self.lineEdit_8.setText("1") # In TAB-2, "4). PPS"
        self.current_datatime = QDateTime.currentDateTime()
        self.p_list = [] # This is for multiprocess to take in the processes running as to list. Later This list used to process join()/terminate() 
             

    def _savefiledialog(self): # _savefiledialog at memu bar
        try:
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
            self._file_write = open(self.fileName, 'w')
        except:
            self.fileName = 'Null'
            pass
    

    def _openfiledialog(self): # OpenFile Dialog 
        try:
            options = QtWidgets.QFileDialog.Options()
            self._fileName_open, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","All Files (*);;PCAP Files (*.pcap)", options=options)
            print(self._fileName_open)
        except:
            self._fileName_open = 'Null'
            pass


#Used for 'Repetitive Tasks'
    def _tab1_running(self, args):
        self._tl_1 = self._tl
        self.args = args
        self._thread_1 = threading.currentThread() # This helps to send a Flag to a running Thread to stop or else purpose.
            #ex below) while getattr(self._thread_1, "do_run", True): 
            # How to debug telnetlib.
            # self._tl_1.set_debuglevel(0.5)
            # self._tl_1_read = self._tl_1.read_all()
            # print (repr(_tl_read))
            # self._tl_1.read_until(b"#").decode('ascii')
        date_from = self.dateTimeEdit.text()
        date_to = self.dateTimeEdit_2.text()        
        temp_for_command = []   # This used to receive a string of multiple commands with ";" such as) show interface terse;show version; show chassis hardware;
                                # For details on how to run, please refer to the Manaual.
        temp_for_command = self.lineEdit_4.text().split(';')  #split used to save command list as LIST.  
        if ((date_from or date_to) == '2000-01-01 00:00.00') or (date_from <= QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") and QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") <= date_to) :
               for i in range(int(self.lineEdit_5.text())):
                    if ((date_from or date_to) == '2000-01-01 00:00.00') or (date_from <= QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") and QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") <= date_to) :
                        for j in temp_for_command :
                                self._tl_1.write(j.encode('ascii') + b'\n')
                                time.sleep(int(self.lineEdit_6.text()))
                                temporal = self._tl_1.read_very_eager().decode('ascii')
                                self.textBrowser_2.append(temporal)
                                self.textBrowser_2.moveCursor(QTextCursor.End) #This is to scroll down, inherited from "from PyQt5.QtGui import QTextCursor"
                                if getattr(self._thread_1, "do_run", True) : #This receives a Flag from "slot_4st('Stop or Ctrl+c' button)" to stop it.
                                    if self.fileName != 'Null' :
                                       self._file_write.write(temporal)
                                       self._file_write.flush()  #This is to write system outputs in Buffer to a file.

                                else :
                                    sys.exit() #Exit Thread, to run out of for loop you need to substitute sys.exit() with 'break'
                              
                    else :
                        self.textBrowser_2.append("Your test ended. or please check time expired 4).Running Schedule ")
                        break
        else : 
            # self.textBrowser_2.setFontPointSize(20)
            self.textBrowser_2.append("please check the other input values added properly or time expired at 4).Running Schedule")


#Used for 'Repetitive Tasks'
    @QtCore.pyqtSlot()    
    def slot_2st(self):  # In TAB-1 "Connect" button.
                         # This is to establish a connection via Telnet at this version. In the furture, Netconf/SSH module would be added.
        try :
            self._tl = telnetlib.Telnet(self.lineEdit.text(), timeout=3) # Establish Telnet connection
            if b"login:" in self._tl.read_until(b"login:",timeout=3):   
                self._tl.write(self.lineEdit_2.text().encode("ascii")+ b"\n")     # In TAB-1, writing "ID"

                if b"Password:" in self._tl.read_until(b"Password:",timeout=3):
                    self._tl.write(self.lineEdit_3.text().encode("ascii")+ b"\n") # In TAB-1, writing "PW"
                    self.textBrowser_2.append(self._tl.read_until(b">", timeout=3).decode('ascii'))
        except:
            self.textBrowser_2.setText("Error occured during connection. please check if you set IP, ip, pw or socket number properly ")
            self.textBrowser_2.append("\n")
            self.textBrowser_2.append("\n")
            self.textBrowser_2.append("In my source-code, login/Password prompt are \"login:\", \"Password:\" are coded ")
            self.textBrowser_2.append("\n")
            self.textBrowser_2.append("\n")
            self.textBrowser_2.append("So your Device prompts do not match thoese, please modify my source-code above properly. It's easy..!!")
            pass
            
            # How to debug telnetlib.
            # self._tl_1.set_debuglevel(0.5)
            # self._tl_1_read = self._tl_1.read_all()
            # print (repr(_tl_read))
            # self._tl_1.read_until(b"#").decode('ascii')


#Used for 'Repetitive Tasks'
    @QtCore.pyqtSlot() 
    def slot_3st(self): # This slot is for  "Running or Enter key" button in TAB-1
        
        try : 
            self._thread_1 = threading.Thread(target=self._tab1_running, args=("task",)) #for multithreading, currently 'args' is for feature usage. Not used yet.
            self._thread_1.start()
        except:
            self.textBrowser_2.setText("You got a problem when you are running. please follow the running sequence (please refer to Manual)") 
            pass

#Used for 'Repetitive Tasks'
    @QtCore.pyqtSlot() # This slot is for  "Stop or Ctrl+c" button in TAB-1
    def slot_4st(self): 
        try : 
            if self._thread_1:  # When stop button clicked, this is to check thread is running or not.
                self._thread_1.do_run = False # This helps to send a Flag to a running Thread.
                self._thread_1.join()  # Waiting for Thread finishes here
            if self._tl_1:      # When stop button clicked, this is to check telnet value has an object or not. (telnet is running or not)
                self._tl_1.write(b"\x03")  # After thread stopped, to send "CTRL +C "
                time.sleep(0.1)
                temp1 = self._tl_1.read_eager()  #reading from a buffer received a response aganist "CTRL +C " from a Server.
                self.textBrowser_2.append(temp1[10:].decode('ascii'))


        except:
            self.textBrowser_2.setText("Exception occurred. please report me s99225078@gmail.com") 
            pass

#Used for 'Packet Builder'
    @QtCore.pyqtSlot() # This slot is to Browze pcap file in TAB-2
    def slot_5st(self): 
        self._openfiledialog()
        ext = os.path.splitext(self._fileName_open)[1] #This is to separate download mode as Text/Binary. https://iamhoh.blog.me/221396426230
        if ext in (".pcap", ".pcapng"):
            try:
                self._packets = rdpcap(self._fileName_open)
                for packet in self._packets:
                    
                    f = io.StringIO()  #The structure is to redirect stdout as to a value "a" to apped to textBrowser_2/textBrowser_3
                    with redirect_stdout(f):
                         print(packet.command())
                    a = f.getvalue()       
                    self.textBrowser_3.append(a)
                    self.textBrowser_2.append(packet.show(dump=True)) #self.textBrowser_2.setText(packet.show(dump=True))#output of the packet.show() is stdout, so to dump as to valuable or text, you have to add "dump=True"             
                    if self.fileName != 'Null' : # This is to save output to a file once def _savefiledialog() enabled.
                        self._file_write.write(packet.show(dump=True))
                        self._file_write.flush()  #This is to write system outputs in Buffer to a file.
            
            except:
                    self.textBrowser_2.setText("You got a problem when opening or loading a PACP") 
                    pass
        else:
            self.textBrowser_2.setText("please open a PCAP only, We don't support other's")
    

#Used for 'Packet Builder'
    @QtCore.pyqtSlot() # This slot is "Running CheckSum"  in TAB-2
    def slot_6st(self):
        changed_text = self.textBrowser_3.toPlainText() # QTextEdit does not have any text() method, if you want to get the text you must use toPlainText(), if you want to clean the text it is better to use clear() since it makes it more readable.       
        self.new_modified_packets = [] #finally, all packets modified and CheckSum calcuation done, will be written in this list.
        reading_changed_text = []      #This is just temporal list to take in the packets displayed in 'self.textBrowser_3.toPlainText()'        
        reading_changed_text = changed_text.split('\n\n')  # To remove "/n" in the list to finally convert to packets(self.new_modified_packets)
        self.textBrowser_2.setText("") # to initialize the text displayed on the "textBrowser_2"
        try :
            for i in reading_changed_text :    
                i = eval(i) # to Convert list 'string' to scapy format..if you do not use eval(), value "i" is simply string, not understable in scapy.
                  
                temp = "" 
                temp = i.summary()
                if "IP" in temp:
                    del i[IP].len
                    del i[IP].chksum
                
                if "TCP" in temp:
                    del i[TCP].chksum
                
                if "ICMP" in temp:
                    del i[ICMP].chksum 

               # i.build()   # for the checksum. The func build() is from SCAPY, which rebuilds the packet. So new Checksum calcuation occurs. 
                self.textBrowser_2.append(i.show2(dump=True)) 
                self.new_modified_packets.append(i)  # The new built packets         
                if self.fileName != 'Null' : # This is to save output to a file once def _savefiledialog() enabled.
                   self._file_write.write(i.show(dump=True))
                   self._file_write.flush()  #This is to write system outputs in Buffer to a file.
        except:
            self.textBrowser_2.setText("Error occured running CheckSum error, you might add/put/modified wrong value type/name, please check what you touched")
            pass


#Used for 'Packet Builder'
    @QtCore.pyqtSlot() # This slot is "Saving modified packets as to PCAP" in TAB-2
    def slot_7st(self):
        self._savefiledialog()
        try:
            for i in self.new_modified_packets:
                wrpcap(self.fileName, i, append=True) # This is to build pacp files, the func "wrpcap()" is from SCAPY
        except:
            self.textBrowser_2.setText("No packet to save. please check if you miss the sequence, such as 'running checksum or else' or not proper filename ")
            pass



#Used for 'Packet Builder'
    @QtCore.pyqtSlot() # This slot is for 'Running' in TAB-2
    def slot_8st(self): 
        try:
          
            p = Process(target=_sending_packets, name= "process name", args=(self.new_modified_packets, int(self.lineEdit_7.text()), int(self.lineEdit_8.text()))) # multiprocessing, and passing the arguments.
            p.start()  
         #   print(p.pid)
            self.p_list.append(p)        
        except:
            self.textBrowser_2.setText("No packet to send. please check if you miss the sequence, such as 'running checksum or else' or not proper filename, else ")
            pass


#Used for 'Packet Builder'
    @QtCore.pyqtSlot() # This slot is for 'Stopping' in TAB-2
    def slot_9st(self):        
        if self.p_list != None:
            for p in self.p_list: # This is to terminate/join all multi-processes
              #  print(p.pid)
                p.terminate()  
            for p in self.p_list: # This is to terminate/join all multi-processes
              #  print(p.pid)
                p.join()  
            self.p_list = [] # This is to inistialize the list
            



if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())

    