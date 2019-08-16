import sys
from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtCore import QDateTime
import sys
import telnetlib
import time
import threading
import datetime
import os



def TELNET(tn, id, pw):
  
    user = id
    password = pw
    timeout = 1  # 3sec
  
    tn.read_until(b"login:").decode('ascii')
    tn.write(user.encode("ascii")+ b"\n")
    tn.read_until(b"Password:").decode('ascii')
    tn.write(password.encode("ascii")+b"\n")

    

class Form(QtWidgets.QMainWindow):
    
#.\project\Tools for networks\Window.ui    
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = uic.loadUi('./Window.ui', self) #If the script is not working, please check the file directory, and Python env path
        self.ui.show()
        self.comboBox_2.addItem("Telnet")

        self.lineEdit.text()
        self.lineEdit_2.text()
        self.lineEdit_3.text()
        self.lineEdit_4.text()
        self.lineEdit_5.setText("1")
        self.lineEdit_6.setText("1")
        self.fileName = 'Null'  #This is for "Files" in Memu bar, initial value.
     #  self.threadclass = ThreadClass()  # for multi-threading for Tab1_running(). Because so far my test and i guess, 2 signal can't be procesed in PYQT at the same time.
        self.actionSave_session.triggered.connect(self.saveFileDialog)   # 'Files' in Memubar 
        self.dateTimeEdit
        self.dateTimeEdit_2
        self.current_datatime = QDateTime.currentDateTime()
 



    @QtCore.pyqtSlot()    # This is to establish a connection via Telnet at this version. In the furture, Netconf/SSH module would be added.
    def slot_2st(self):  
        
        self.tn = telnetlib.Telnet(self.lineEdit.text())
        TELNET(self.tn, self.lineEdit_2.text(),self.lineEdit_3.text())   
        self.textBrowser_2.setText(self.tn.read_until(b">").decode('ascii'))
           
  
    def saveFileDialog(self): # File Dialog at memubar
        try:
            options = QtWidgets.QFileDialog.Options()
            options |= QtWidgets.QFileDialog.DontUseNativeDialog
            self.fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self,"QFileDialog.getSaveFileName()","","All Files (*);;Text Files (*.txt)", options=options)
            self.ff = open(self.fileName, 'w')
        except:
            self.fileName = 'Null'
        

    def Tab1_running(self, args):

        self.tn1 = self.tn
        self.args = args
        self.t = threading.currentThread() # This helps to send a Flag to a running Thread to stop or else purpose.
            # while getattr(self.t, "do_run", True): 
            # print ("working on %s" % self.arg)
     
      
            # self.tn1.set_debuglevel(0.5)
            # self.tn1_read = self.tn1.read_all()
            # print (repr(tn1_read))
            # self.tn1.read_until(b"#").decode('ascii')

        date_from = self.dateTimeEdit.text()
        date_to = self.dateTimeEdit_2.text()
        
        temp_for_command = []   # This used to receive a string of commands with ";" such as) run show interface terse;aaaa;run show chassis hardware;
        temp_for_command = self.lineEdit_4.text().split(';')  #split used to save command list as LIST.

  
        if ((date_from or date_to) == '2000-01-01 00:00.00') or (date_from <= QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") and QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") <= date_to) :
               for i in range(int(self.lineEdit_5.text())):

                    if ((date_from or date_to) == '2000-01-01 00:00.00') or (date_from <= QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") and QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss") <= date_to) :
                      #  print(i)
                      #  print(QDateTime.currentDateTime().toString("yyyy-MM-dd hh:mm:ss"))

                        for j in temp_for_command :
                                self.tn1.write(j.encode('ascii') + b'\n')
                                time.sleep(int(self.lineEdit_6.text()))
                                temporal = self.tn1.read_very_eager().decode('ascii')
                                self.textBrowser_2.append(temporal)

                                if getattr(self.t, "do_run", True) : #This receives a Flag from "slot_4st" to stop it.

                                        if self.fileName != 'Null' :
                                            print(self.fileName)
                                            print(temporal)
                                            self.ff.write(temporal)
                                            self.ff.flush()  #This is to write system outputs in Buffer to a file.


                                else :
                                    sys.exit() #Thread stop, as running out of for loop.
                                    
                    else :
                        self.textBrowser_2.append("Your test ended. or please check time expired 4).Running Schedule ")
                        break
    
        else : 
            # self.textBrowser_2.setFontPointSize(20)
            self.textBrowser_2.append("please check the other input values added properly or time expired at 4).Running Schedule")
   

  
    @QtCore.pyqtSlot() # This slot is for  "Running or Enter key" button.
    def slot_3st(self): 
        self.t = threading.Thread(target=self.Tab1_running, args=("task",)) #for multithreading, currently 'args' is for feature usage. Not used yet.
        self.t.start()


    @QtCore.pyqtSlot() # This slot is for  "Stop or Ctrl+c" button.
    def slot_4st(self):  
        self.t.do_run = False # This helps to send a Flag to a running Thread.
        self.t.join()  # Waiting for Thread finishes here
        self.tn1.write(b"\x03")  # After thread stopped, to send "CTRL +C "
        time.sleep(0.1)
        temp1 = self.tn1.read_very_eager()  #reading from a buffer received a response aganist "CTRL +C " from a Server.
        self.textBrowser_2.append(temp1[10:].decode('ascii'))

  
        #   self.tn1.write(b"\x03")  # This is for "CTRL +C" of Telnetlib
        #   time.sleep(0.1)
        #   temp1 = self.tn1.read_very_eager() # This is to remove "recv b'\xf2[abort]\r\n"
        #   self.textBrowser_2.append(temp1[10:].decode('ascii')) # This is to remove "recv b'\xf2[abort]\r\n", which can not convert to Ascii


     
        # Other method to define a Thread
        # class ThreadClass(threading.Thread):
        #    def __init__(self, parent = None):
        #        super(ThreadClass, self).__init__(parent)
        #        self.stopped = False
        #        threading.Thread.__init__(self)
        #
        #    def run(self):
        #        w.Tab1_running()

 
if __name__ == "__main__":
    app =QtWidgets.QApplication(sys.argv)
    w = Form()
    sys.exit(app.exec())

