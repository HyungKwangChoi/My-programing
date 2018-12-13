

* Python Version : 3.7 64bit

* description: These is a simple FTP program.
   - just simply/quickly to download/upload files


* To notice


	myftp = ftplib.FTP("X.X.X.X") <=== please put FTP server addr
	myftp.login("XX", "XXXX")     <=== please put id, password

	def my_ownload(ftp, filename):
	           fd = open("C:\\Python35\\studyrootm\\" + filename, 'w') <==== please put your local directory properly. If not, it will return an error.
 		   fd = open("C:\\Python35\\studyrootm\\" + filename, 'wb')

	def my_upload(ftp, filename):
		fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb')<==== please put your local directory properly. If not, it will return an error.
 		fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb')

  
	download = "hi"   <=== please put filename, which you are trying to download
	upload = "hi.txt" <=== please put filename, which you are trying to upload



* Usage:
C:\Python35\studyrootm>py ftp.py

