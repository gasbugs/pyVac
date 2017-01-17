#sample 2-3


import hashlib
import os


def matchHashValue(fileName):
    f = open(fileName,"rb")
    buf = f.read()
    f.close()

    md5 = hashlib.md5()
    md5.update(buf)
    print "update : " + buf
    fmd5 = md5.hexdigest()
    print "hexdigest : " + fmd5

    if fmd5 == "44d88612fea8a8f36de82e1278abb02f":
        print "detected"
    else:
        print "nothing found"

def checkFileSize(fileName):
    fsize = os.path.getsize(fileName)
    if fsize == 68:
        print "File Size is Correct"
        return 1
    else:
        print "File Size is not Correct"
        return 0

fileName = "eicar.txt"

if (checkFileSize(fileName)):
    matchHashValue(fileName)
else:
    print "nothing found"
