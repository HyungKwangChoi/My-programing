"""
Written by 

1. History
   2019. 8
     - "Tools for Networkers_v1"
   2020.1
     - "Tools for Networkers_v2.1"
   2020.3
     - "Tools for Networkers_v3.2"

2. Author
   HyungKwang (s99225078@gmail.com)
   Rengaramalingam A (rengahcl@gmail.com) : contributed to the feature of "Easy Lab Replication", which originated from his shell script "scriptit.sh"

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
import struct
from telnetlib import DO, DONT, IAC, WILL, WONT, NAWS, SB, SE
MAX_WINDOW_WIDTH = 65000  # Max Value: 65535
MAX_WINDOW_HEIGHT = 5000


import telnetlib         # This mainly used for TAB-1 such as telnet feature. 

# Third party lib.  For this, you have to install PYQT5. Please refer to the "release_note_v2.1"
# PYQT5 is for GUI.
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import QTextCursor #This is used for Qtextbrowzer scroll down feature. (self.textBrowser_2.moveCursor(QTextCursor.End))

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
        self.ui = uic.loadUi(os.path.join(root, 'Window.ui'), self) #If the script is not working, please check the file directory, and Python env path such as)"\project\Tools for networks\Window.ui"
        self.ui.show()
        self.fileName = 'None'  #This is for "Files" in Memu bar, initial value.
        self.actionSave_session.triggered.connect(self._savefiledialog)   # 'Files -> Start logging' in Memubar 
        self.actionStop_logging.triggered.connect(self._stopfiledialog)   # 'Files -> Stop logging' in Memubar 

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
        self._tl = None       #Initialization to the un-defined Telnet object value Used for 'Repetitive Tasks'
     #Initialization for TAB-2
        self.lineEdit_7.setText("1") # In TAB-2, "3). The number of packets to send"
        self.lineEdit_8.setText("1") # In TAB-2, "4). PPS"
        self.current_datatime = QDateTime.currentDateTime()
        self.p_list = [] # This is for multiprocess to take in the processes running as to list. Later This list used to process join()/terminate()   

     #Initialization for TAB-3   
        
        self.temp_list = [] # To take in template strings(txt_string).
        """self.lineEdit_9.setEnabled(False) # In TAB-3, it sets to uneditable displaying 'gray' color 
        self.lineEdit_10.setEnabled(False)
        self.lineEdit_11.setEnabled(False)  
        self.lineEdit_12.setEnabled(False)
        self.lineEdit_13.setEnabled(False)
        self.lineEdit_14.setEnabled(False)
        self.lineEdit_15.setEnabled(False)
        self.lineEdit_16.setEnabled(False)"""

        self._TAB3_template_dic = {0:['',''],
                 1: ['IGP-OSPF # MPLS RSVP LSP # NO PE-CE Protocol','template-1.txt','1'], 
                 2: ['IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol OSPF # NO RR','template-2.txt','1'],
                 3: ['IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol BGP  # NO RR','template-3.txt','1'], 
                 4: ['IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol OSPF # SINGLE RR','template-4.txt','1'],
                 5: ['IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol BGP  # SINGLE RR','template-5.txt','1'], 
                 6: ['IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol OSPF # DUAL RR','template-6.txt','1'], 
                 7: ['IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol BGP  # DUAL RR','template-7.txt','1'],
                 8: ['IGP-OSPF # MPLS LDP # NO PE-CE Protocol','template-8.txt','1'],
                 9: ['IGP-OSPF # MPLS LDP # PE-CE Protocol OSPF # NO RR','template-9.txt','1'],
                10: ['IGP-OSPF # MPLS LDP # PE-CE Protocol BGP  # NO RR','template-10.txt','1'],
                11: ['IGP-OSPF # MPLS LDP # PE-CE Protocol OSPF # SINGLE RR','template-11.txt','1'], 
                12: ['IGP-OSPF # MPLS LDP # PE-CE Protocol BGP  # SINGLE RR ','template-12.txt','1'],
                13: ['IGP-OSPF # MPLS LDP # PE-CE Protocol OSPF # DUAL RR','template-13.txt','1'], 
                14: ['IGP-OSPF # MPLS LDP # PE-CE Protocol BGP  # DUAL RR','template-14.txt','1'],
                15: ['6PE - IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol BGP  # SINGLE RR','template-15.txt','1'],
                16: ['6VPE - IGP-OSPF # MPLS RSVP LSP # PE-CE Protocol BGP  # SINGLE RR','template-16.txt','1'],
                17: ['VPLS [3 CE] - IGP OSPF # MPLS RSVP LSP # SINGLE RR [4 loops Required]','template-17.txt','4'],
                18: ['VPLS [3 CE] - IGP OSPF # MPLS LDP # SINGLE RR [4 loops Required]','template-18.txt','4'],
                19: ['MPLS L2VPN - IGP-OSPF # MPLS RSVP LSP # SINGLE RR [3 loops Required]','template-19.txt','3'],
                20: ['MPLS L2VPN - IGP-OSPF # MPLS LDP # SINGLE RR [3 loops Required]','template-20.txt','3'],
                21: ['INTER-AS L3VPN OPTION-A    IGP-OSPF # MPLS LDP # PE-CE Protocol EBGP','template-21.txt','1'],
                22: ['INTER-AS L3VPN OPTION-B    IGP-OSPF # MPLS LDP # PE-CE Protocol EBGP','template-22.txt','1'],
                23: ['INTER-AS L3VPN OPTION-C    IGP-OSPF # MPLS LDP # PE-CE Protocol EBGP','template-23.txt','1'],
                24: ['PLAIN MULTICAST # PIM - SPARSE MODE # STATIC RP CONFIGURED # ASM','template-24.txt','1'],
                25: ['PLAIN MULTICAST # PIM - DENCE MODE','template-25.txt','1'],
                26: ['PLAIN MULTICAST # PIM - SPARSE MODE # NO RP CONFIGURED # SSM','template-26.txt','1'],
                27: ['NG-MVPN # MBGP Multicast VPN with PIM SSM as PE-CE Protocol','template-27.txt','1'],
                28: ['NG-MVPN # MBGP Multicast VPN with PIM ASM as PE-CE Protocol # RPT-SPT','template-28.txt','1'],
                94: ['Template - MPLS VPLS SETUP [3 CE] - IGP OSPF # MPLS RSVP LSP # SINGLE RR ','template-94.txt','4'],
                95: ['NG-MVPN # MBGP Multicast VPN with PIM ASM as PE-CE Protocol # RPT-SPT','template-95.txt','1'],       
                98: ['IGP-OSPF -- MULTI-AREA - STUB - NSSA -TSA  -ALL P2MP LINKS [1 loop]','template-98.txt','1'],
                99: ['IGP-OSPF -- MULTI-AREA - STUB - NSSA -TSA  -ALL P2P LINKS  [1 loop]','template-99.txt','1']}
        # In Dictionary, for string, you have to use ', not ""
        self.comboBox_3.currentTextChanged.connect(self._TAB3_commbobox3_changed) #To take Combobox3 event, passing value to def _TAB3_commbobox3_changed()
        self.comboBox_4.currentIndexChanged.connect( self._TAB3_commbobox4_changed) #To take Combobox4 event, passing value to def __TAB3_commbobox4_changed()
        #lambda가 있는 이유는 combobox click event를 구현하기 위함...click 이벤트는 없기 때문에, index change를 통해서.
         


    def _new_window_pop_up(self,template):
     
        self.pop_up_window = QtWidgets.QMainWindow()                                    
        self.pop_up_window.setWindowTitle('Lab Topology')

        self.pop_up_window.move(self.geometry().x() + self.geometry().width() + 30,         
                 self.geometry().y() - 30)
        
        text_display = QtWidgets.QTextBrowser(self.pop_up_window)      
        text_display.setStyleSheet('font: 10pt "Fixedsys"; background-color: rgb(0, 0, 0); color: rgb(0, 255, 72);')  

        self.pop_up_window.setGeometry(600,150,1200,600)
        text_display.setGeometry(10,10,1200,600)    
        text_display.setText(template)

        self.pop_up_window.show()
        
    def _TAB3_commbobox4_changed(self,value):        

        if value != 0 and value !=-1:  # index값이, clear()는 -1, add는 무조건 여러개를 하더라도 '0', 실제 클릭은 1,2,3,4 로 index값을 받음
            for k, v in self._TAB3_template_dic.items() : #list loop구문
                if self.comboBox_4.currentText() in v:
                    break
                 
            f = open("Lab Topology/{0}".format(self._TAB3_template_dic[k][1]), 'r')
            txt_string = f.read()
            f.close

            self._new_window_pop_up(txt_string.split('after adding interface number.')[0])

       # print(self._TAB3_template_dic[k][2])
            if self._TAB3_template_dic[k][2] == "1":
                self.lineEdit_9.setEnabled(True) # In TAB-3, it sets to uneditable displaying 'gray' color 
                self.lineEdit_10.setEnabled(True)
                self.lineEdit_11.setEnabled(False)  
                self.lineEdit_12.setEnabled(False)
                self.lineEdit_13.setEnabled(False)
                self.lineEdit_14.setEnabled(False)
                self.lineEdit_15.setEnabled(False)
                self.lineEdit_16.setEnabled(False)

            elif self._TAB3_template_dic[k][2] == "3":
                self.lineEdit_9.setEnabled(True)  
                self.lineEdit_10.setEnabled(True)
                self.lineEdit_11.setEnabled(True)  
                self.lineEdit_12.setEnabled(True)
                self.lineEdit_13.setEnabled(True)  
                self.lineEdit_14.setEnabled(True)
                self.lineEdit_15.setEnabled(False)
                self.lineEdit_16.setEnabled(False)

        # elif self._TAB3_template_dic[k][2] == "4":
            else :
                self.lineEdit_9.setEnabled(True)  
                self.lineEdit_10.setEnabled(True)
                self.lineEdit_11.setEnabled(True)  
                self.lineEdit_12.setEnabled(True)
                self.lineEdit_13.setEnabled(True)  
                self.lineEdit_14.setEnabled(True)
                self.lineEdit_15.setEnabled(True)  
                self.lineEdit_16.setEnabled(True)


    def _TAB3_commbobox3_changed(self, value):
        if value == "MPLS L3VPN" :
            self.textBrowser_4.setText("MPLS L3VPN")
            self.comboBox_4.clear()
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[1][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[2][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[3][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[4][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[5][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[6][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[7][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[8][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[9][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[10][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[11][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[12][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[13][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[14][0])


        elif value == "MPLS L2VPN" :
            self.textBrowser_4.setText("MPLS L2VPN")
            self.comboBox_4.clear()
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[19][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[20][0])

        elif value == "MPLS VPLS" :
            self.textBrowser_4.setText("MPLS VPLS ")
            self.comboBox_4.clear()
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[17][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[18][0])

        elif value == "Multicast" :
            self.textBrowser_4.setText("Multicast")
            self.comboBox_4.clear()
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])          
            self.comboBox_4.addItem(self._TAB3_template_dic[24][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[25][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[26][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[27][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[28][0])
         
        elif value == "6PE" :
            self.textBrowser_4.setText("6PE")
            self.comboBox_4.clear()
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[15][0])

        elif value == "6VPE" :
            self.textBrowser_4.setText("6VPE")
            self.comboBox_4.clear()
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[16][0])

        elif value == "INTER-AS VPN" :
            self.textBrowser_4.setText("INTER-AS VPN ") 
            self.comboBox_4.clear()     
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[21][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[22][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[23][0])

        elif value == "Various scenario" :
            self.textBrowser_4.setText("Various scenario")
            self.comboBox_4.clear()
            self.comboBox_4.addItem(self._TAB3_template_dic[0][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[98][0])
            self.comboBox_4.addItem(self._TAB3_template_dic[99][0])

    def _savefiledialog(self): # 'Files -> Start logging' in Memubar 
        try:
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
            self._file_write = open(self.fileName, 'w')
        except:
            self.fileName = 'None'
            pass
    
    def _stopfiledialog(self): # 'Files -> Stop logging' in Memubar 
            self.fileName = 'None'

    def _openfiledialog(self): # OpenFile Dialog 
        try:
            options = QtWidgets.QFileDialog.Options()
            self._fileName_open, _ = QtWidgets.QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()","","All Files (*);;PCAP Files (*.pcap)", options=options)
            print(self._fileName_open)
        except:
            self._fileName_open = 'None'
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
            # print (repr(self._tl_read))
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
                                    if self.fileName != 'None' :
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

#Used for common usage for Telnet initial access

    def _telnet_access(self,ip,id,pw):

        try :
            self._tl = telnetlib.Telnet(ip, timeout=2) # Establish Telnet connection
            if b"login:" in self._tl.read_until(b"login:",timeout=3):   
                self._tl.write(id.encode("ascii")+ b"\n")     # In TAB-1, writing "ID"

                if b"Password:" in self._tl.read_until(b"Password:",timeout=3):
                    self._tl.write(pw.encode("ascii")+ b"\n") # In TAB-1, writing "PW"
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
            # print (repr(self._tl_read))
            # self._tl_1.read_until(b"#").decode('ascii')


#Used for 'Repetitive Tasks'
    @QtCore.pyqtSlot()    
    def slot_2st(self):  # In TAB-1 "Connect" button.
                         # This is to establish a connection via Telnet at this version. In the furture, Netconf/SSH module would be added.
        self._telnet_access(self.lineEdit.text(),self.lineEdit_2.text(),self.lineEdit_3.text())


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
                    if self.fileName != 'None' : # This is to save output to a file once def _savefiledialog() enabled.
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


                #i.build()   # for the checksum. The func build() is from SCAPY, which rebuilds the packet. So new Checksum calcuation occurs. 
                self.textBrowser_2.append(i.show2(dump=True)) 
                self.new_modified_packets.append(i)  # The new built packets   
               
                if self.fileName != 'None' : # This is to save output to a file once def _savefiledialog() enabled.
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
           #     print(p.pid)
                p.terminate()  
            for p in self.p_list: # This is to terminate/join all multi-processes
            #    print(p.pid)
                p.join()  
            self.p_list = [] # This is to inistialize the list


#Used for 'Easy Lab Replication'
    @QtCore.pyqtSlot() # This slot is for 'Done' in TAB-3
    def slot_10st(self):        
        self.temp_list = [] # To take in template strings(txt_string).

        try:
            for k, v in self._TAB3_template_dic.items() : #list loop구문
                if self.comboBox_4.currentText() in v:
                    break

        
            f = open("Lab Topology/{0}".format(self._TAB3_template_dic[k][1]), 'r')
            txt_string = f.read()
            f.close()


         
            if self._TAB3_template_dic[k][2] == "1":
                i = self.lineEdit_9.text()
                txt_string = txt_string.replace("I1",i)  
                txt_string = txt_string.replace("interface1",i) 

                i = self.lineEdit_10.text()           
                txt_string = txt_string.replace("I2",i)   
                txt_string = txt_string.replace("interface2",i)  

                self.temp_list = txt_string.split('after adding interface number.')
                self.textBrowser_2.setText(self.temp_list[2])
                self.textBrowser_2.append(self.temp_list[3])
                self._new_window_pop_up(self.temp_list[1])


            if self._TAB3_template_dic[k][2] == "3":
                i = self.lineEdit_9.text()
                txt_string = txt_string.replace("I1",i)  
                txt_string = txt_string.replace("interface1",i) 

                i = self.lineEdit_10.text()           
                txt_string = txt_string.replace("I2",i)   
                txt_string = txt_string.replace("interface2",i)  

                i = self.lineEdit_11.text()
                txt_string = txt_string.replace("I3",i)  
                txt_string = txt_string.replace("interface3",i) 

                i = self.lineEdit_12.text()           
                txt_string = txt_string.replace("I4",i)   
                txt_string = txt_string.replace("interface4",i)  

                i = self.lineEdit_13.text()
                txt_string = txt_string.replace("I5",i)  
                txt_string = txt_string.replace("interface5",i) 

                i = self.lineEdit_14.text()           
                txt_string = txt_string.replace("I6",i)   
                txt_string = txt_string.replace("interface6",i)  

                self.temp_list = txt_string.split('after adding interface number.')
                self.textBrowser_2.setText(self.temp_list[2])
                self.textBrowser_2.append(self.temp_list[3])
                self._new_window_pop_up(self.temp_list[1])




            if self._TAB3_template_dic[k][2] == "4":
                i = self.lineEdit_9.text()
                txt_string = txt_string.replace("I1",i)  
                txt_string = txt_string.replace("interface1",i) 

                i = self.lineEdit_10.text()           
                txt_string = txt_string.replace("I2",i)   
                txt_string = txt_string.replace("interface2",i)  

                i = self.lineEdit_11.text()
                txt_string = txt_string.replace("I3",i)  
                txt_string = txt_string.replace("interface3",i) 

                i = self.lineEdit_12.text()           
                txt_string = txt_string.replace("I4",i)   
                txt_string = txt_string.replace("interface4",i)  

                i = self.lineEdit_13.text()
                txt_string = txt_string.replace("I5",i)  
                txt_string = txt_string.replace("interface5",i) 

                i = self.lineEdit_14.text()           
                txt_string = txt_string.replace("I6",i)   
                txt_string = txt_string.replace("interface6",i)  

                i = self.lineEdit_15.text()
                txt_string = txt_string.replace("I7",i)  
                txt_string = txt_string.replace("interface7",i) 

                i = self.lineEdit_16.text()           
                txt_string = txt_string.replace("I8",i)   
                txt_string = txt_string.replace("interface8",i)  

                self.temp_list = txt_string.split('after adding interface number.')
                self.textBrowser_2.setText(self.temp_list[2])
                self.textBrowser_2.append(self.temp_list[3])
                self._new_window_pop_up(self.temp_list[1])



        except:
            self.textBrowser_2.setText("pleae write down interface names all in activated boxes")    
            pass 
                

#Used for 'Easy Lab Replication'
    @QtCore.pyqtSlot() # This slot is for 'Download Topology & Congifuration' in TAB-3
    def slot_11st(self):
        if not self.temp_list :
            self.textBrowser_2.setText("pleae write down interface names all in activated boxes and click Done")

        else :
            self._savefiledialog()
            try:
              self._file_write.write(self.temp_list[1])
              self._file_write.write(self.temp_list[2])
              self._file_write.write(self.temp_list[3])
              self._file_write.flush()  #This is to write system outputs in Buffer to a file.
              self._file_write.close()
            except:
                pass


#Used for 'Easy Lab Replication'
    @QtCore.pyqtSlot() # This slot is for 'Done' in TAB-3
    def slot_12st(self):   

        try:     
            
            self._telnet_access(self.lineEdit_17.text(),self.lineEdit_18.text(),self.lineEdit_19.text())
            self._tl_2 = self._tl


            #self._tl_2.set_debuglevel(0.5)

            
            self._tl_2.write("configure".encode("ascii")+ b"\n")
            self.textBrowser_2.append(self._tl_2.read_until(b"#", timeout=7).decode('ascii'))
            self.textBrowser_2.moveCursor(QTextCursor.End) #This is to scroll down, inherited from "from PyQt5.QtGui import QTextCursor"

            time.sleep(1)
    
            self._tl_2.write(self.temp_list[3].encode("ascii")+ b"\n")
            self.textBrowser_2.moveCursor(QTextCursor.End) #This is to scroll down, inherited from "from PyQt5.QtGui import QTextCursor"
            self.textBrowser_2.append("Waiting..Uploading configuration to.....")

 

            self._tl_2.write(b"\n")
            self._tl_2.write("commit".encode("ascii")+ b"\n")

            self._tl_2.write("exit".encode("ascii")+ b"\n")
            self._tl_2.write("exit".encode("ascii")+ b"\n")

   
        
            while True:             # read until we stop
                hi = self._tl_2.read_eager().decode("ascii")

                time.sleep(1)                
                if "exit" in hi:  # check if there was no data to read
                    self.textBrowser_2.append("Commit Done successfully.")
                    break           # now we stop
                
                if "err" or "fai" in hi:  # check if there was no data to read
                    print(hi)
                    self.textBrowser_2.append("Commit failure...please check the Router configuration.")
                    break           # now we stop

        #except EOFError:            # If connection was closed
        except :            # If connection was closed    
                print('connection failure')
                pass



if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())

    