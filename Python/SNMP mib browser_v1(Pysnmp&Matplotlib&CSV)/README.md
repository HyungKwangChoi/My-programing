## Intro

 Working as a Network Engineer, I’ve experienced some common needs.

 It's about small programs which helpful & convenient at a practical usage perspective, and license free.

 So i am on the step with small dreams hoping networkers to be happy.
 
 And
 
 Hoping my challenge will not stop.

 If you want to add more meaningful features to this tool, send me email (s99225078@gmail.com).
 
 Let's see where/how this network tool gona evolve, with fun.....


## SNMP mib browser_v1 Running Capture

![running](https://user-images.githubusercontent.com/33049747/80051850-2bfd7780-8554-11ea-8212-107575b701fb.png)


## Building Environment.(Further details, please refer to the manual "SNMP Mib Browser_v1 manual.pdf")

  * Using Multiprocessing and Queue() to communicate between multi-processes

  * Pysnmp lib
     - Install : pip install pysnmp
     - Aysncio snmp feature used. Which is not working with python 3.7.2, but 3.8.2


  * Matplotlib lib
     - Install : pip install matplotlib.
     - 2 Graph features used to draw in real time : plt.plot(), plt.bar()
       1). plt.plot() : for X, Y axis , LIST has to be used. 


  * csv lib
     - Install : pip install csv
     - This used to save data(current time and value)



## Block diagram

![diagram](https://user-images.githubusercontent.com/33049747/80051913-5cddac80-8554-11ea-9dc6-9d12c7dc5314.png)