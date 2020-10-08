from PyQt5.QtWidgets import QWidget, QFileDialog, QTreeWidgetItem, QTreeWidget, QComboBox
 
from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtCore import Qt, pyqtSignal
import os
import sys
from PyQt5.QtGui import  QPixmap  #QTextCursor
import pandas as pd 
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from os.path import basename

from Error_handling import pop_up_error # This is imported from the file 'Error_handling.py' which i created. 
from matplotlib import rc
from datetime import datetime
import time

######### This lib mainly used for Tab-4, real-time plotting" ######## 
# For this, you have to install pyqtgraph lib. Please refer to the "release_note_v4.2.pdf"
import pyqtgraph as pg
 

class TimeAxisItem(pg.AxisItem): 
     def __init__(self, *args, **kwargs): 
         super().__init__(*args, **kwargs) 
         self.setLabel(text='Time (sec)', units=None) 
         self.enableAutoSIPrefix(False) 
 

     def tickStrings(self, values, scale, spacing): 
         #print("--tickStrings valuse ==>", values) 
         return [time.strftime("%H:%M:%S", time.localtime(local_time)) for local_time in values] 
 

class SecondWindow_for_live_plotting(QWidget):
    
    # This is to send Closed signal to an master class object "self._mrtg_second_window.Closed.connect(self.slot_15st)" in "Tools for Networkers_v4.2.py"
    # So closing all.
     
    Closed = pyqtSignal()

    def __init__(self):
 
        QWidget.__init__(self) 
 
        self.object_list = []
        self.setWindowTitle("MRTG from pyqtgraph & Pysnmp")


        """
          # Another method to adjust window size. 
          # To use 'setFixedWidth', 'setFixedHeight', you must initialize both method under "class SecondWindow_for_live_plotting"
          # self._mrtg_second_window.setFixedWidth(self.x_size)
          # self._mrtg_second_window.setFixedHeight(self.y_size)

          #initial_width = 800
          # setting  the fixed width of window 
          #self.setFixedWidth(initial_width) 

          #initial_height = 250
          # setting  the fixed height of window 
          #self.setFixedHeight(initial_height) """


        # If you don't specify exact layout size, it will take whole size of the figure opened.
        self.layout = QtWidgets.QVBoxLayout()

    # This is used to detect when the close drawing 'Live_plotting' window when the button "X" click
    def closeEvent(self, event):  
        self.Closed.emit()       #This is to emit close signal to "Closed = pyqtSignal()"
        super(SecondWindow_for_live_plotting, self).closeEvent(event)  # This is a close event detected.

    def creat_object_add_layout(self, number, _figure_options):
        self.object_list.append(Live_plotting(_figure_options))
        self.layout.addWidget(self.object_list[number].pw)     # This is to add each MRTG graph as to "layout widget"
        self.setLayout(self.layout) 

    def cleanup_graph_and_value(self):
        self.clearLayout() # This is to remove "layout widget"
        self.object_list = [] # This is to remove "object_list"
         
    # This is to remove "layout widget", when closed the live plotting window
    def clearLayout(self):  
        for i in reversed(range(self.layout.count())):
            item = self.layout.itemAt(i)
            if item != None :
                widget = item.widget()
            if widget != None:
                self.layout.removeWidget(widget)
                widget.deleteLater()   



class Live_plotting(QWidget):
           
    """
      ### 3. Live plotting options##
      #self._figure_options list number : list member : object                      : label
      #                                   0           : self.lineEdit_29            : Y axis MAX Value
      #                                   1           : self.lineEdit_30            : Title
      #                                   2           : self.lineEdit_31            : Y axis MIN value
      #                                   3           : self.lineEdit_32            : X axis Label
      #                                   4           : self.lineEdit_33            : Y axis label
      #             Not Used yet, future purpose      : self.lineEdit_34            : X Time Range (sec)
      #                                                 self.lineEdit_35            : Graph Size value
      #                                   5           : self.lineEdit_36            : Legend
      #                                   6           : self.checkBox.isChecked()   : Drawing Plot Graph
      #                                   7           : self.checkBox_2.isChecked() : Drawing Bar Graph"""


    def __init__(self, _figure_options):
        QWidget.__init__(self) 
        self.pw = pg.PlotWidget( 
             title=_figure_options[1], 
             labels={'left': _figure_options[4]},              
             axisItems={'bottom': TimeAxisItem(orientation='bottom')} 
        ) 
        

        legend = pg.LegendItem()    

        """# If you want specify legned position, refer to below.
        # legend = pg.LegendItem((80,60), offset=(40,160))
        # self.pw.addLegend(offset=(10,10))
        # self.pw.addLegend(size=None, offset=(2,180))
        #if you enable Bar graph legnd, you will face error, because 'Bar graph legnd' doesn't work well at this version.  "legend.addItem(self.pl1, 'yyy')"""
        legend.setParentItem(self.pw.graphicsItem())

      # self.x and self.y are for plotting (x, y)
        self.x = []
        self.y = []

        self.drawing_plot = False
        self.drawing_bar = False

        self.x.append(int(time.time()))
        self.y.append(0)

        if _figure_options[6] :
            self.pl = self.pw.plot(pen='r', name = 'Red')
            legend.addItem(self.pl, _figure_options[5])
            self.drawing_plot = True

        if _figure_options[7] :
            self.pl1 = pg.BarGraphItem(x=self.x,x0=None, x1=None,y0=None,y1=None, height=self.y, width=1, pen ='g', brush='g')
            self.pw.addItem(self.pl1)            
            self.drawing_bar = True

        self.pw.showGrid(x=True, y=True)    
        self.pw.setYRange(_figure_options[2], _figure_options[0], padding=0) # Freeprog.tistory.com/368, padding '0' means removing back space.
   
 
  # This is an actual drawing function thread.
    def plot_drawing(self, queue, stop_thread, saving_to_csv):
    
        i = 0 
      
        if saving_to_csv[0] != 'None':                
            saving_to_csv[1].writerow(["Index", "Time", "OID query {0}".format(saving_to_csv[2])])
            saving_to_csv[0].flush()

        while True :
        
           # Exiting loop, so closing the thread.
            if stop_thread():
                break

           # Actullay this is from "qq.put(val)" of "async def async_next_snmp_request()" "Snmp_functions.py"
            yy = int(queue.get()) 
         
            new_time_data = int(time.time()) 
            current_time = datetime.now() 
        

           # Writing OID value return and currentl time, and index number to CSV file.
            if saving_to_csv[0] != 'None':            
                saving_to_csv[1].writerow([i, current_time.replace(microsecond=0), yy])
                i = i + 1
                saving_to_csv[0].flush()
 
            self.x.append(new_time_data)
            self.y.append(yy)

            self.pw.setXRange(new_time_data - 600, new_time_data + 1, padding=0)   


          # drawing plot graph.
            if self.drawing_plot:
                self.pl.setData(self.x, self.y)  

          # drawing bar graph.
            if self.drawing_bar :
                self.pl1.setOpts(x=self.x,x0=None, x1=None,y0=None,y1=None, height=self.y, width=1, brush='g')

          # To limit the size of list to '600', which is timedelta drawing.
            if len(self.x) >= 600 or len(self.y) >= 600 : 
                del(self.x[0])   
                del(self.y[0])   

            #print("testing/{0} {1}".format(self.x, self.y))


class Second_Window_to_recall_MRTG_Graph(QWidget):

    def __init__(self, parent=None):
        super(Second_Window_to_recall_MRTG_Graph, self).__init__()
        
        self.root = os.path.dirname(os.path.realpath(__file__))
        self.ui = uic.loadUi(os.path.join(self.root, 'Loading_MRTG_Graph.ui'), self) 

        self.label_4.setPixmap(QPixmap(os.path.join(self.root, 'plot2.png')).scaled(340,200))
        self.label_5.setPixmap(QPixmap(os.path.join(self.root, 'plot3.png')).scaled(440,200))

        self.df_list = [] #Used to merge all csv files into one DataFrame. Finally df_list[0] has the complete dataframe.
        self.mytree_item_list = []

        """
        ### Options for "Spacing" under "multiple axes" group
        # self.lineEdit_3 : left
        # self.lineEdit_4 : bottom
        # self.lineEdit_5 : right       
        # self.lineEdit_6 : top
        # self.lineEdit_7 : hspace
        # self.lineEdit_8 : wspace"""

        self.comboBox.currentTextChanged.connect(self._changing_lineEdit_status)
        self.lineEdit_3.setEnabled(False) 
        self.lineEdit_4.setEnabled(False) 
        self.lineEdit_5.setEnabled(False) 
        self.lineEdit_6.setEnabled(False) 
        self.lineEdit_7.setEnabled(False) 
        self.lineEdit_8.setEnabled(False) 

    def _changing_lineEdit_status(self):

        if self.comboBox.currentText() == 'Automatic' :
          self.lineEdit_3.setEnabled(False) 
          self.lineEdit_4.setEnabled(False) 
          self.lineEdit_5.setEnabled(False) 
          self.lineEdit_6.setEnabled(False) 
          self.lineEdit_7.setEnabled(False) 
          self.lineEdit_8.setEnabled(False) 

        else :
          self.lineEdit_3.setEnabled(True) 
          self.lineEdit_4.setEnabled(True) 
          self.lineEdit_5.setEnabled(True) 
          self.lineEdit_6.setEnabled(True) 
          self.lineEdit_7.setEnabled(True) 
          self.lineEdit_8.setEnabled(True)      

# This slot is for  "File Open" button
    @QtCore.pyqtSlot() 
    def slot1(self):     

        try:
            i = 0
            self.mytree.clear()
            self.df_list = []
            self.mytree_item_list = []


            """ To load only one file you have to use "getOpenFileName", but multiple files you have to use "getOpenFileNames"
            fname return a type of Touple. please check it with print(fname[0]) and print(fname) how are different """    

            fname = QFileDialog.getOpenFileNames(self, 'Open file', "", "All Files(*);; CSV Files(*.csv)") 
            print(fname)
          
            if fname[0]:
 
                for temp in fname[0]:
                    self.mytree_item_list.append(QTreeWidgetItem(self.mytree) )
                                  
                for line in fname[0]:
                    self.mytree_item_list[i].setText(0, basename(line)) # 'basename' is a method only to extract file name such as) 'C:\\notebook\\test\\text.txt' -> 'text.txt'

                    df = pd.read_csv(line)

                    """ 
                    # 2 ways extract the first and last index of specific column. (using 'name' and 'column' number)
                    # please figure out, how are they different.
                    # Good reference written by korean.
                    # https://dandyrilla.github.io/2017-08-12/pandas-10min/
                    #
                    # starttime = df.iloc[[0],[1]] 
                    # endtime = df.iloc[[-1],[1]] 
                    """ 
                                
                    starttime = df.iloc[0]['Time']  
                    endtime = df.iloc[-1]['Time'] # -1' means the last index.        
                      

                    self.mytree_item_list[i].setText(3,  starttime)
                    self.mytree_item_list[i].setText(4,  endtime)

                   #pandas just doesn't work well with custom date-time formats, <class 'pandas.core.indexes.datetimes.DatetimeIndex'>
                    df['Time'] = pd.to_datetime(df['Time'], format='%Y-%m-%d %H:%M:%S', errors='raise') 
                    df.drop('Index',axis=1, inplace=True)
                    df.set_index('Time', inplace=True)
                    self.df_list.append(df)

                    """  
                    # This is to merge all csv files opened, based on "Time" sorting.
                    # 'outer' mean full merge.
                    # Please refer to the link below, which written by korean language.
                    # https://rfriend.tistory.com/m/258 
                    """
                    if i != 0:
                        self.df_list[0] = pd.merge(self.df_list[0], self.df_list[i], how='outer', on='Time') 

                    i = i + 1

               #To extract DataFrame headers (OID value).
                df_Column_naming_list = list(self.df_list[0].columns)
                   
                #print(self.df_list[0].iloc[[0,-1],:])

               #This is to write dataframe headers (OID number ) to each QTreeWidgetItem
               #'Qt.ItemIsEditable' has user edit each items.   
                for j in range(i):            
                  self.mytree_item_list[j].setText(9, df_Column_naming_list[j] )
                  self.mytree_item_list[j].setFlags(self.mytree_item_list[j].flags() | Qt.ItemIsEditable)
                
               #This is for initialzie comboBox option, So that comboBox item goes into comboBox and into an object of "QTreeWidgetItem" (self.mytree_item_list)
           
                for x in range(i):  
                    self.combo_box_colors = QComboBox(self.mytree)
                    self.combo_box_colors.addItem('blue')      
                    self.combo_box_colors.addItem('green')           
                    self.combo_box_colors.addItem('red')     
                    self.combo_box_colors.addItem('cyan')   
                    self.combo_box_colors.addItem('magenta')   
                    self.combo_box_colors.addItem('yellow') 
                    self.combo_box_colors.addItem('black')                       
                    self.combo_box_colors.addItem('white')               
                    self.mytree.setItemWidget(self.mytree_item_list[x], 11, self.combo_box_colors)

                    self.combo_box_graph_types = QComboBox(self.mytree)
                    self.combo_box_graph_types.addItem('Plot')
                    self.combo_box_graph_types.addItem('Bar')
                    self.mytree.setItemWidget(self.mytree_item_list[x], 8, self.combo_box_graph_types) 

            else :
                QtWidgets.QMessageBox.about(self, "Warning", "Please select files.")

        except:
            QtWidgets.QMessageBox.about(self, "Warning", "excep")
            pass

# This slot is for  "Plotting" button in TAB-1
    @QtCore.pyqtSlot() 
    def slot2(self):

        hour_locator = mdates.HourLocator() 
        day_locator = mdates.DayLocator()  # range(60) is the default
        weekly_locator = mdates.WeekdayLocator(interval=1) # interval=1 means '7 days' interval.
        month_locator = mdates.MonthLocator() 
        year_locator = mdates.YearLocator()   
        
       
        """plot_item_dict is dictionary, which going to save items from QTreeWidgetItem,
           such as ) 
               FileName, Title, X axis label, Start time(X xias), End time (X xias), Y axis label, Y axis Min value, Y axis Max value, Graph Type (Plot, Bar), OID,Legend, Color 
          {0: ['1.csv', 'a', 'a', '2020-08-13 19:08:13', '2020-08-13 22:15:00', 'a', '0', '100', 'Plot', 'OID query 1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0_x', 'a', 'blue'], 
          1: ['2.csv', 'b', 'b', '2020-08-13 19:08:13', '2020-08-13 22:15:00', 'b', '0', '100', 'Plot', 'OID query 1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0_y', 'b', 'blue'] }"""
        plot_item_dict = {}



        #self.mytree (Table) -> self.mytree_item_list (Table Row)
        #self.mytree is an object of QTreewidget, which used to establesh a table.
        #mytree_item_list is an object to take in items such as) File Name, Title, X axis label, Starttime,,,and so on
        root = self.mytree.invisibleRootItem() 

        # 'child_count' is about how many QTreeWidgetItem are
        child_count = root.childCount()

        try : 
          if not self.df_list : 
              raise Exception('please check Above steps if you missed/made a mistake, or check CSV data ') 
 

          if not self.mytree_item_list:
                
             raise Exception('please check Above steps if you missed/made a mistake, or check CSV data ') 


          for i in range(child_count):  
                 # item has each QTreeWidgetItem while it's running on 'for' statement.
                  item = root.child(i)            
                 #Below is to take DropBox 5, 11 items value chosen into dictionary. 
                  for j in range(12):
                        if j == 8 or j == 11:
                            qComboBox = self.mytree.itemWidget(self.mytree_item_list[i], j)
                            text_selected = qComboBox.currentText()
                            plot_item_dict.setdefault(i, []).append(text_selected)
                        else :
                              plot_item_dict.setdefault(i, []).append(item.text(j))
                       
         #To extract DataFrame headers (OID value).      
          df_Column_naming_list = list(self.df_list[0].columns)

    
          """
          # Below are for 'plot all in the figure.', if 'plot all in the figure.' button clicked. 
          """

          if self.radioButton_1.isChecked():
              fig = plt.figure(figsize=(int(self.lineEdit_21.text()),int(self.lineEdit_22.text())))
 
              rc('font', family='NanumGothic')  # Ths is to support korean language.
              plt.grid( linestyle='--')
              plt.locator_params(axis='y', nbins=10) 
              #plt.xticks(rotation=45)

              for i in range(child_count ):
                    
                  x = 'line' + str(i)
                  
       
                  #print(self.df_list[0])
                  #self.df_list[0] = self.df_list[0][plot_item_dict[i][3]:plot_item_dict[i][4]]
                  #print(self.df_list[0])

                  if plot_item_dict[0][8] == 'Bar' :
                    x, = plt.bar(self.df_list[0].index, self.df_list[0].iloc[:,i], width=1./24/60/60, align='edge',color=plot_item_dict[i][11], label=plot_item_dict[i][10])
                  else :                     
                    x, = plt.plot(self.df_list[0].index, self.df_list[0].iloc[:,i], color=plot_item_dict[i][11], label=plot_item_dict[i][10])
   

              if plot_item_dict[0][6] and plot_item_dict[0][7]:  # To set 'ylim' of the graph.
                  plt.ylim(int(plot_item_dict[0][6]),int(plot_item_dict[0][7]))


              plt.legend(loc='best') # 'best' option means, legend goes displayed properly in the figure.

              plt.title(plot_item_dict[0][1])
              plt.ylabel(plot_item_dict[0][5])
              plt.xlabel(plot_item_dict[0][2])


          """
          # Below are for "multiple axes", when 'multiple axes' button clicked. 
          # Unlike "plot all in the figure.", for subplot(like this), when you do subplot, you have to set Ddateformatter, amd time Locator at the moment.  
          # So, if you look this subplot, 'for' statements, it runs until complete one subplot, and then goes to the next drawing subplot. 

          """

          if self.radioButton_2.isChecked(): 

              # figure options under "Options" of 'multiple axes'
              # self.lineEdit_15 : width
              # self.lineEdit_16 : height
              fig = plt.figure(figsize=(int(self.lineEdit_15.text()),int(self.lineEdit_16.text())))
              ax = [] #This is for subplot list

               #(Row X Column)  
               #self.lineEdit   : Row
               #self.lineEdit_2 : Column            
              for i in range(child_count):
                i = i +1
                numbering = self.lineEdit.text() + self.lineEdit_2.text() + str(i)
                ax.append(fig.add_subplot(int(numbering)))
                rc('font', family='NanumGothic')  # To support Korean language.
                plt.grid( linestyle='--')
                plt.locator_params(axis='y', nbins=10) 
                #plt.xticks(rotation=45)

                i = i -1
                  
                if plot_item_dict[i][8] == 'Bar' :
                    ax[i].bar(self.df_list[0].index, self.df_list[0].iloc[:,i], width=1./24/60/60, align='edge',color=plot_item_dict[i][11], label=plot_item_dict[i][10])
                else :         
                    ax[i].plot(self.df_list[0].index, self.df_list[0].iloc[:,i], color=plot_item_dict[i][11], label=plot_item_dict[i][10])


               #hour graph  
                if self.radioButton.isChecked():              
                            myFmt = mdates.DateFormatter('%H:%M')
                            ax[i].xaxis.set_major_formatter(myFmt)
                            plt.setp(ax[i].xaxis.get_majorticklabels(), rotation=int(self.lineEdit_25.text()))

               #Daily graph
                if self.radioButton_3.isChecked():
                              hour_locator = mdates.HourLocator()        
                              day_locator = mdates.DayLocator()  # range(60) is the default
                              majorFmt = mdates.DateFormatter('%m-%d')  
                              ax[i].xaxis.set_major_locator(day_locator) 
                              ax[i].xaxis.set_major_formatter(majorFmt)
                              plt.setp(ax[i].xaxis.get_majorticklabels(), rotation=int(self.lineEdit_25.text()))  
                              if self.checkBox_2.isChecked():
                                ax[i].xaxis.set_minor_locator(hour_locator)
                           
               #Weekly graph   
                if self.radioButton_4.isChecked():        
                              day_locator = mdates.DayLocator()  # range(60) is the default
                              weekly_locator = mdates.WeekdayLocator(interval=1) 
                              majorFmt = mdates.DateFormatter('%m-%d')
                              ax[i].xaxis.set_major_locator(weekly_locator) 
                              ax[i].xaxis.set_major_formatter(majorFmt)
                              plt.setp(ax[i].xaxis.get_majorticklabels(), rotation=int(self.lineEdit_25.text()))  
                              if self.checkBox_2.isChecked():
                                ax[i].xaxis.set_minor_locator(day_locator)
 
               #Month graph
                if self.radioButton_5.isChecked():
                              month_locator = mdates.MonthLocator()   
                              weekly_locator = mdates.WeekdayLocator(interval=1) 
                              majorFmt = mdates.DateFormatter('%Y-%m')                  
                              ax[i].xaxis.set_major_locator(month_locator) 
                              ax[i].xaxis.set_major_formatter(majorFmt)
                              plt.setp(ax[i].xaxis.get_majorticklabels(), rotation=int(self.lineEdit_25.text()))  
                              if self.checkBox_2.isChecked():
                                ax[i].xaxis.set_minor_locator(weekly_locator)
                      
               #Year graph
                if self.radioButton_6.isChecked():
                              year_locator = mdates.YearLocator()   
                              month_locator = mdates.MonthLocator() 
                              majorFmt = mdates.DateFormatter('%Y')                     
                              ax[i].xaxis.set_major_locator(year_locator) 
                              ax[i].xaxis.set_major_formatter(majorFmt)
                              plt.setp(ax[i].xaxis.get_majorticklabels(), rotation=int(self.lineEdit_25.text()))  
                              if self.checkBox_2.isChecked():
                                ax[i].xaxis.set_minor_locator(month_locator)
                              
              # To set 'ylim' of each subplot
                if plot_item_dict[i][6] and plot_item_dict[i][7]:  
                    ax[i].set_ylim([int(plot_item_dict[i][6]), int(plot_item_dict[i][7])])

                ax[i].set_xlabel(plot_item_dict[i][2])
                ax[i].set_ylabel(plot_item_dict[i][5])
                ax[i].set_title(plot_item_dict[i][1])

 
                ax[i].legend(loc='best')

                """
                #self.comboBox is the Option for "Spacing" under "multiple axes" group
                #'tight_layout()' set the figure size and space properly.
                # self.lineEdit_3 : left
                # self.lineEdit_4 : bottom
                # self.lineEdit_5 : right       
                # self.lineEdit_6 : top
                # self.lineEdit_7 : hspace
                # self.lineEdit_8 : wspace"""

              if self.comboBox.currentText() == 'Automatic' :
                    plt.tight_layout()  

              if self.comboBox.currentText() == 'Manual' :
                    plt.subplots_adjust(left = int(self.lineEdit_3.text()), bottom = int(self.lineEdit_4.text()), right = int(self.lineEdit_5.text()), top = int(self.lineEdit_6.text()), hspace = int(self.lineEdit_7.text()), wspace = int(self.lineEdit_8.text())) 
         
          """
          # Below are for "plot all in the figure."
          """

         #hour graph
          if self.radioButton.isChecked():                
            if self.radioButton_1.isChecked():       
                myFmt = mdates.DateFormatter('%H:%M')
                plt.gca().xaxis.set_major_formatter(myFmt)
                plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=int(self.lineEdit_23.text()))
                plt.gcf().autofmt_xdate()


         #Daily graph
          if self.radioButton_3.isChecked():
            majorFmt = mdates.DateFormatter('%m-%d')  
            if self.radioButton_1.isChecked():
              plt.gca().xaxis.set_major_locator(day_locator)
              plt.gca().xaxis.set_major_formatter(majorFmt)
              plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=int(self.lineEdit_23.text()))
              if self.checkBox.isChecked():
                 plt.gca().xaxis.set_minor_locator(hour_locator)
              plt.gcf().autofmt_xdate()
                           
         #Weekly graph
          if self.radioButton_4.isChecked():
            majorFmt = mdates.DateFormatter('%m-%d')              
            if self.radioButton_1.isChecked():    
              plt.gca().xaxis.set_major_locator(weekly_locator)
              plt.gca().xaxis.set_major_formatter(majorFmt)
              plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=int(self.lineEdit_23.text()))
              if self.checkBox.isChecked():
                plt.gca().xaxis.set_minor_locator(day_locator)
              plt.gcf().autofmt_xdate()

         #Month graph                
          if self.radioButton_5.isChecked():
            majorFmt = mdates.DateFormatter('%Y-%m')   
            if self.radioButton_1.isChecked():
              plt.gca().xaxis.set_major_locator(month_locator)
              plt.gca().xaxis.set_major_formatter(majorFmt)
              plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=int(self.lineEdit_23.text()))
              if self.checkBox.isChecked():
                plt.gca().xaxis.set_minor_locator(weekly_locator) 
              plt.gcf().autofmt_xdate()

         #Year graph
          if self.radioButton_6.isChecked():
            majorFmt = mdates.DateFormatter('%Y')  
            if self.radioButton_1.isChecked():
              plt.gca().xaxis.set_major_locator(year_locator)
              plt.gca().xaxis.set_major_formatter(majorFmt)
              plt.setp(plt.gca().xaxis.get_majorticklabels(), rotation=int(self.lineEdit_23.text()))
              if self.checkBox.isChecked():
                plt.gca().xaxis.set_minor_locator(month_locator)
              plt.gcf().autofmt_xdate()

          plt.show()


        except Exception as e:
            #print('messages :  ', e)
                pop_up_error(e)
                pass

# This slot is for  "Reset" button  
    @QtCore.pyqtSlot() 
    def slot3(self):
        self.mytree.clear()
        self.df_list = []
        self.mytree_item_list = []
