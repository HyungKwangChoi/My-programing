###################################################################################################
# How to run
#
# Simply run the python program after you put host, user, password properly such as) ./telnet_v1.py
#
####################################################################################################

import sys
import telnetlib
import time

host = "X.X.X.X"      # put host address properly 
user = "XXXX"         # put user name   
password = "XXXXX"    # put pw
timeout = 1  # 3sec


tn = telnetlib.Telnet(host)


print(tn.read_until(b"login:").decode('ascii'))
tn.write(user.encode("ascii")+ b"\n")


print(tn.read_until(b"Password:").decode('ascii'))
tn.write(password.encode("ascii")+b"\n")

#time.sleep(1)

print(tn.read_until(b"jun>").decode('ascii'))

 
tn.write(b"configure \n")


while True:
    

    ######################## debugging#####################
    #   tn.set_debuglevel(1)
    #   tn_read = tn.read_all()
    #   print (repr(tn_read))
    #######################################################

    line = tn.read_until(b"\n",timeout)          #reading it from buffer until "\n". If nothing found it waits until timeout,
    print(line)                                 # then 'read_until' returns it red whole in buf becuase it red buf until it found.
    a = line.decode('ascii')                    # via socket, we receive/send binary, so we need to encode/decode ascii.
                                                #if you do " print(line) " you can see it as bindary 
                                                # one more thing. Once if you read data with read_until or whatever, it cleared at Socket buf. 
                                                #If you don't read data on Socket, because buf size is small, so you can't receive more data by then.


    if a.find("jun#") >= 0: # find : if you find matching, it returns the address of Char/Num found, if nothing found, it returns "-1"
        user = input("enter your command ") #Python 2.7 you have to use raw_input()
        tn.write(user.encode('ascii') + b"\n")
       #tn.write(b'\x1b') <==== For special Characters "http://donsnotes.com/tech/charsets/ascii.html#cntrl"
        continue

    elif a.find(")---") >= 0:
        user = input()
        tn.write(user.encode('ascii') + b"\n")  #when it sends it needs encode, and receive it nees decode.


tn.close()

#output = tn.read_all() 

#fp = open("Output.txt","w") 
#fp.write(output) 
#fp.close()


##########ETC####################
#careful
#1.Try clearing read buffer before sending any command 
# read_very_eager() is the command, it will read anything on the buffer without blocking the IO so call t.read_very_eager() before calling 
#
#0. useful code
#    if not t.expect(["login : "], timeout=10):  # Expect username prompt
#        raise Exception('No login prompt is received')
#
#
#
#  Many changed between 2.7 and 3.7
#
# https://docs.python.org/2.7/library/telnetlib.html
#    =>2.7 : print line , raw_input()
#
# https://docs.python.org/3.7/library/telnetlib.html
#    => 3.7 : print (line), input()
################################

