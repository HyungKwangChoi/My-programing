

* Python Version : 3.7 64bit

* description: These is a FTP interactive program.
   - supports several commands such as : dir, cd, get, put, mkdir, rmdir, delete, debug


* To notice


	host = "X.X.X.X"      # put host address properly 
	user = "XXXX"         # put user name   
	password = "XXXXX"    # put pw

 
	print(tn.read_until(b"login:").decode('ascii')) <==== From python 3.7, you have to prepend "b", which means binary. Decode binary to ascii.

	print(tn.read_until(b"jun>").decode('ascii')) <===== you need to change it properly. As it's Telnet_v1. So later, i will add an enhancement.


* Usage:
C:\Python35\studyrootm>py telnet_v1.py

