import asyncio
from pysnmp.hlapi.asyncio import ( # This is for TAB-4 PYSNMP lib
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

from contextlib import suppress

"""async def sample_coroutine(run_statement):

    if run_statement.value == 1:
        return 1212
    
    elif run_statement.value == 0:
        while True:
                print( "check if  run_statement is in {0}".format(run_statement.value))
                if run_statement.value == 1:
                   print( "checking {0}".format(run_statement.value))
                   break
              #  await asyncio.sleep(0.5)"""

async def monitor(run_statement):
    loop = asyncio.get_event_loop()
    while True:
        if run_statement.value == 0:
           # os.unlink('reset')
            loop.stop()
        await asyncio.sleep(1)


async def async_next_snmp_request(snmpEngine, IP_ADDRESS,COMMUNITY, OIDS, POLLING_INTERVAL, SNMP_GET_TIMEOUT, qq):
    """Walk SNMP oids asynchronously."""
    
    # This is time fuction, which triggers 'await asyncio.sleep(next(g))' with fixed time interval.     
    def g_tick():
        t = time.time()
        count = 0
        while True:
            count += 1
            yield max(t + count * POLLING_INTERVAL - time.time(), 0)

    g = g_tick()
   

    def is_number(num): # This is to check if 'num' is number or str. If 'num' is number, i will return True
        try:
            float(num)   # Type-casting the string to `float`.
                         # If string is not a valid `float`, 
                         # it'll raise `ValueError` exception
        except :
            return False

        return True

   # event = asyncio.Event()
   # loop_pending_resume_task = asyncio.create_task(loopp(event))
   # loop_pending_resume_task = asyncio.create_task(loop_pending_resume(event))
    while True:
   
      #  print('periodic main', time.time())

            try :
    
                
              #  coroutine_object = sample_coroutine(run_statement)
   
               # await coroutine_object
                    response = await getCmd(  #basic asyncio pysnmp get function.
                        snmpEngine,
                        CommunityData(COMMUNITY, mpModel=0),
                        UdpTransportTarget((IP_ADDRESS, 161), timeout=SNMP_GET_TIMEOUT, retries=0),
                        ContextData(),
                        ObjectType(ObjectIdentity(OIDS))
                    )
        
                    await asyncio.sleep(next(g))

                    error_indication, error_status, error_index, var_binds = response

                    if  error_indication or error_status or error_index :
         
                        qq.put(0)

                    else:
                        for name, val in var_binds:
                         #   print('%s = %s' % (name, val))
                            if is_number(val): # This is to check the return value is number or str. In case str, it will return "False"
                                qq.put(val)
                            else :
                                break
 
            except :
                    break
               
        
def snmp_polling(IP_ADDRESS, COMMUNITY, OIDS, POLLING_INTERVAL,SNMP_GET_TIMEOUT, qq, run_statement ):
     
        snmpEngine = SnmpEngine()
        loop = asyncio.get_event_loop()
       # loop.set_debug(True)  # Enable debug
        
        
        from pysnmp.hlapi.asyncore.cmdgen import lcd
        @asyncio.coroutine
        def unconfigure(snmpEngine,authData=None): #if not set, it will throuw exception mesages "Task was destroyed but it is pending!", please refer to below for details.
            lcd.unconfigure(snmpEngine,authData)

        loop.create_task(unconfigure(snmpEngine)) 

         
        while True:

            # This is to stop the loop. Not exiting the 'While loop', but only pending for a while.
            if run_statement.value == 0: 
                   
                continue

            else :
                workers = []
                workers.append(loop.create_task(monitor(run_statement))) # # This is to stop the loop while it's running. 'async def monitor' checks it with 'await asyncio.sleep(1)'  
                workers.append(loop.create_task(async_next_snmp_request(snmpEngine, IP_ADDRESS, COMMUNITY, OIDS, POLLING_INTERVAL,SNMP_GET_TIMEOUT, qq ))  )
 
                loop.run_forever()

                for t in workers: #cancelling event loop.
                    t.cancel()
       
                    with suppress(asyncio.CancelledError):
               
                        loop.run_until_complete(t)

 
