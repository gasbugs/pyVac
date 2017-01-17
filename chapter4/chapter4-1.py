import file_exe
import os

def scanExe():
    print "detected : EXE"

def scanDll():
    print "detected : DLL"

def scanZip():
    print "detected : ZIP"

def scanPdf():
    print "detected : PDF"

def scanEveryting():
    scanExe()
    scanDll()
    scanZip()
    scanPdf()

def dirScan(dir):
    for root, dirs, files in os.walk(dir):
        for file in files:
            file_scan( str(root) + "\\" + file)

def file_scan(fname):
    result = file_exe.id_filename(fname)

    if result == "exe":
        scanExe()
    elif result == "dll":
        scanDll()
    elif result == "zip":
        scanZip()
    elif result == "pdf":
        scanPdf()
    else :
        scanEveryting()

if __name__ == "__main__":
    file_scan("c:/windows/system32/notepad.exe")
