#https://asyncio.readthedocs.io/en/latest/hello_world.html
#https://www.guru99.com/python-queue-example.html

import logging
import asyncio
import time
from multiprocessing import Process, log_to_stderr
from multiprocessing import Queue
import matplotlib.pyplot as plt
import datetime
from pysnmp.hlapi.asyncore.cmdgen import lcd
import matplotlib.dates as mdates
logger = log_to_stderr(logging.INFO)
import csv

from pysnmp.hlapi.asyncio import (
    getCmd,
    CommunityData,
    UdpTransportTarget,
    SnmpEngine,
    ContextData,
    ObjectIdentity,
    ObjectType,
    isEndOfMib,
)
from pysnmp.error import PySnmpError

LOGGER = logging.getLogger(__name__)

HOSTNAME = '172.27.14.60'
HOSTNAME1 = 'demo.snmplabs.com'
OIDS = '1.3.6.1.4.1.2636.3.1.13.1.8.9.1.0.0'
#OIDS1 = 'sysDescr.0'

#OIDS1 = '1.3.6.1.2.1.1.1.0'
OIDS1 = 'sysDescr.0'


comment_1 = 'first task'
comment_2 = 'second task'
SLEEP_TIME_1 = 1
SLEEP_TIME_2 = 1

async def unconfigure(snmpEngine,authData=None): #if not set, it will throuw exception mesages "Task was destroyed but it is pending!", please refer to below for details.
    lcd.unconfigure(snmpEngine,authData)


async def async_next_snmp_request(snmpEngine,host, oids, sleep_time, comment,queue):
    """Walk SNMP oids asynchronously."""
    
    def g_tick(): # for 1 sec periodic interval
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t + count * sleep_time - time.time(), 0)
    g = g_tick()
   
    def is_number(num): # This is to check if 'num' is number or str. If 'num' is number, i will return True
        try:
            float(num)   # Type-casting the string to `float`.
                         # If string is not a valid `float`, 
                         # it'll raise `ValueError` exception
        except :
            return False

        return True

    N = 1
    while (N == 1):
        print('periodic main', time.time())
        
        try :
            response = await getCmd(
                snmpEngine,
                CommunityData('public', mpModel=0),
                UdpTransportTarget((host, 161), timeout=1,retries=0),
                ContextData(),
                ObjectType(ObjectIdentity(oids))
            )
        
            #  print('middle start', time.time())
            await asyncio.sleep(next(g))
            #  print('middle end', time.time())
            error_indication, error_status, error_index, var_binds = response

            if  error_indication or error_status or error_index :
                print("Error occured")
                queue.put(0)

            else:
                for name, val in var_binds:
                    print('%s = %s' % (name, val))
                    if is_number(val):
                        queue.put(val)
                    else :
                        N = 0  #This is to get out while loop, so that finish this task.
        except :
            N = 0       #When exeption occurs, this is to get out while loop, so that finish this task.
            
 
             
def snmp_polling(queue):
    
        snmpEngine = SnmpEngine()
        loop = asyncio.get_event_loop()

        task = loop.create_task(async_next_snmp_request(snmpEngine, HOSTNAME, OIDS, SLEEP_TIME_1,comment_1 ,queue))  

        loop.run_until_complete(task)
    
        loop.run_until_complete(unconfigure(snmpEngine)) 
        loop.close()
       # alive.clear()


def plot_drawing(queue):
    print("did it start?")

    plt.rcParams["figure.figsize"] = (10,4)
   # plt.rcParams['grid.linestyle'] = "--" 
   # plt.ylim(0, 1000)
    #plt.yticks(np.arange(0,100,100/10))
    plt.locator_params(axis='y', nbins=10) 
    plt.ylabel('Value')
    plt.xlabel('Time')

    plt.grid( linestyle='--')
    #plt.savefig('savefig_default.png')
 
    f = open('hi.csv','w', newline='') # this is to save a file as csv format.
 
    i = 0
    xx = []
    yy = []
    while True:

        current_time = datetime.datetime.now() #current_time = datetime.datetime.now().replace(microsecond=0)
        delta_time = datetime.datetime.now() - datetime.timedelta(minutes=10)
     
  
        y = queue.get()
       
 
        xx.append(current_time.replace(microsecond=0))
        yy.append(y)

        plt.axis([delta_time.replace(microsecond=0), current_time.replace(microsecond=0),0,10]) 
        plt.bar(current_time.replace(microsecond=0),y, width=1./24/60/60, align='edge',color='g') # This is to address 1 sec interval width bar graph, "24 hours/60min/60sec with 1 sec interval"
      
       # print(xx[-2:])
       # print(yy[-2:])
        plt.plot(xx[-2:], yy[-2:], c='red')
        plt.pause(0.0000000001)
         
        wr = csv.writer(f)
        wr.writerow([i,current_time, y])
        i = i+1


        sec = mdates.SecondLocator()
        #mins = mdates.MinuteLocator()
        plt.gcf().autofmt_xdate()
        myFmt = mdates.DateFormatter('%H:%M')

        #plt.gca().xaxis.set_major_locator(mins)
        plt.gca().xaxis.set_major_formatter(myFmt)
        plt.gca().xaxis.set_minor_locator(sec)
        
    plt.show()


    f.close()
 


if __name__ == '__main__':

    queue = Queue()
    p1 = Process(target=snmp_polling, args=(queue,)) 
    p1.start()
    
    p2 = Process(target=plot_drawing, args=(queue,))  
    p2.start()


   # print(f"p1.is_alive() {p1.is_alive()}")
   # print(f"p2.is_alive() {p2.is_alive()}")
    #p1.join() #<===blocking here, Zombie processes: To avoid zombie processes you need to have the parent read its childrens exit codes, you need to run join() in the parent on the child processes to do that


    #if p1.is_alive() == False:
     #   p2.terminate()
      #  p2.join()

   # print(f"p1.is_alive() {p1.is_alive()}")
   # print(f"p2.is_alive() {p2.is_alive()}")

 
