import sys
import ftplib
import os
 
myftp = ftplib.FTP("X.X.X.X") # or session = ftplib.FTP('ip', 'id', 'pw')
myftp.login("XX", "XXXX")

#################################################################################
#ftp = ftplib.FTP()
#ftp.connect('192.168.1.102',2233) You can separate port number like with method.
#
################################################################################
myftp.dir() # reading directory file list. or myFtp.dir("/var")
            # Another way to list up.
            #        data = []
            # 
            # myftp.dir(data.append)
            # 
            # myftp.quit()
            # 
            # for line in data:
            #     print "-", line
            #

def my_ownload(ftp, filename):
    ext = os.path.splitext(filename)[1] #This is to separate download mode as Text/Binary. https://iamhoh.blog.me/221396426230
    if ext in (".txt", ".htm", ".html"):
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'w')
            ftp.retrlines("RETR " + filename ,fd.write)
            fd.close()
                                                     # myftp.retrlines : for the Ascii file. 
            #myftp.retrbinary("RETR "+filename, fd.write)# myftp.retrlbinary : for binary, writing files to above open(), 주의핡것 "RETR " RETR에서 한간 안띄우면, permission 500에러뜸.

            #fd = open("C:\\Python35\\studyrootm\\" + filename, 'wb') #open() used for where/with what's name file will be saved in your PC/Mobile.
                                                                  #For the directory set, you have to use double "\\""
        except:
             print ("Error occureddddddddddddddddddddddddd")

    else:
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'wb')
            ftp.retrbinary("RETR " + filename ,fd.write)
            fd.close()

        except:
             print ("Error else")


##############################################
#
#
#  Reference : OS
# https://iamhoh.blog.me/221396426230
#################################################

def my_upload(ftp, filename):
    ext = os.path.splitext(filename)[1] #This is to separate download mode as Text/Binary. https://iamhoh.blog.me/221396426230
    if ext in (".txt", ".htm", ".html"):
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb') #type must be 'rb'. If you set 'r', it returns an error.
            ftp.storlines("STOR " + filename ,fd)
            fd.close()

        except:
             print ("Error occureddddddddddddddddddddddddd")

    else:
        try:
            fd = open("C:\\Python35\\studyrootm\\" + filename, 'rb')
            ftp.storbinary("STOR " + filename ,fd, 1024)
            fd.close()

        except:
             print ("Error else")

download = "hi"
upload = "hi.txt"

#ROOT= '/var/home/jun'
#myftp.cwd(ROOT) : Chaning directory


#my_download(myftp, download)
my_upload(myftp, upload)
myftp.quit()



