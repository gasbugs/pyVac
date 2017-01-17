#sample 2-2


import hashlib


f = open("eicar.txt","rb")
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
