#sample 2-1
f = open("eicar.txt","rb")
buf = f.read()
f.close()

print buf

if buf[:3] == "X5O":
    print "detected"
else:
    print "nothing found"
