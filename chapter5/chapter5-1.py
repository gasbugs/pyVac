import hashlib
import os
import cureVirus as cv

fileNameList = []
fileSizeList = []
fileHashList = []

fdb = open("main.hdb","rb")
for hdb in fdb.readlines():
    hdb = hdb.strip()
    fileNameList.append(hdb.split(':')[2])
    fileSizeList.append(int(hdb.split(':')[1]))
    fileHashList.append(hdb.split(':')[0])
fdb.close()

def fileScan(fileName):
    print "[+] " + fileName + " : filescan start"
    if (checkFileSize(fileName)):
        matchHashValue(fileName)
        # sample 3-3
        
        if(matchHashValue(fileName)):
            return 1
    return 0
        
def checkFileSize(fileName):
    fsize = os.path.getsize(fileName)
    for size in fileSizeList:
        if fsize == size:
            print "\t[+] File Size is Correct"
            return 1
    print "\t[-] File Size is not Correct"
    return 0
    
def matchHashValue(fileName):
    f = open(fileName,"rb")
    buf = f.read()
    f.close()

    md5 = hashlib.md5()
    md5.update(buf)
    fmd5 = md5.hexdigest()
    for hashValue in fileHashList:
        if fmd5 == hashValue:
        #if 0<fileHashList.index(fmd5):
            print "\t\t[+] " + fileName + " is eicar file"
            return 1
    print "\t\t[-] " + fileName + " is not eicar file"
    return 0

def dirScan(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            # sample 5-1
            if(fileScan( str(root) + "\\" + file)):
                print "\n======== delete ========\n" + str(root) + "\\" + file + "\n"
                cv.deleteFile(str(root) + "\\" + file)
            
if __name__ == "__main__":
    dir = "c:\\test"
    dirScan(dir)
