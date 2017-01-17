#sample 2-4

import hashlib
import os

def fileScan(fileName):
    print "[+] " + fileName + ": filescan start"
    if (checkFileSize(fileName)):
        matchHashValue(fileName)
        
def checkFileSize(fileName):
    fsize = os.path.getsize(fileName)
    if fsize == 68:
        print "\t[+] File Size is Correct"
        return 1
    else:
        print "\t[-] File Size is not Correct"
        return 0
    
def matchHashValue(fileName):
    f = open(fileName,"rb")
    buf = f.read()
    f.close()

    md5 = hashlib.md5()
    md5.update(buf)
    fmd5 = md5.hexdigest()

    if fmd5 == "44d88612fea8a8f36de82e1278abb02f":
        print "\t\t[+] " + fileName + " is eicar file"
    else:
        print "\t\t[+] " + fileName + " is not eicar file"

dir = "c:\\test"

for root, dirs, files in os.walk(dir):
    for file in files:
        fileScan( str(root) + "\\" + file)

