import os
import urllib2

def deleteFile(fname):
    os.remove(fname)
    print "remove the file :", fname

def changeFile(fname):
    os.remove(fname)
    f = open(fname, 'wb')
    response = urllib2.urlopen("http://srv/new/file/url")
    f.write(response.read())
    f.close()

def cleanRegistry(fname):
    pass

def cleanService(fname):
    pass