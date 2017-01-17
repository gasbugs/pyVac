# -*- coding:UTF-8 -*-
import hashlib
import os

import win32con
import win32api
import win32security

import wmi
import sys

def get_process_privileges(pid):
    try :
        # 타깃 프로세스의 핸들 구하기
        hproc = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION
                                     ,False , pid)
        
        # 메인 프로세스 토큰 열기
        htok = win32security.OpenProcessToken(hproc, win32con.TOKEN_QUERY)
        
        # 활성화된 권한 목록 추출
        privs = win32security.GetTokenInformation(htok, win32security.TokenPrivileges)
        
        # 권한에 대해 루프를 돌면서 활성화된 권한 출력
        priv_list = ""
        for i in privs:
            # 권한에 대해 루프를 돌면서 활성화된 권한 출력
            if i[1] == 3:
                priv_list += "%s|" % win32security.LookupPrivilegeName(None, i[0])
                
    except Exception as e:
        print e
        priv_list = "N/A"
    
    return priv_list
                    
                            

def log_to_file(message):
    fd = open("process_monitor_log.csv", "ab")
    fd.write("%s\r\n"% message)
    fd.close()
    
    return


fileNameList = []
fileSizeList = []
fileHashList = []

#sample 3-2

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
        '''
        if(matchHashValue(fileName)):
            return 1
    return 0
    '''
        
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
            fileScan( str(root) + "\\" + file)
            # sample 3-3
            '''
            if(fileScan( str(root) + "\\" + file)):
                print "\n======== delete ========\n" + str(root) + "\\" + file + "\n"
                import curemod
                curemod.delete(str(root) + "\\" + file)
            '''
# 로그 파일 표제 생성
log_to_file("Time,User,Executable,CommandLine,PID,Parent,Privileges")

# WMI 인터페이스 초기화
c = wmi.WMI()




            
if __name__ == "__main__":
    #dir = "c:\\test"
    #dirScan(dir)

    # 프로세스 모니터 생성
    process_watcher = c.Win32_Process.watch_for("creation")

    while True:
        try:
            new_process = process_watcher()
            
            proc_owner  = new_process.GetOwner()
            proc_owner  = "%s\\%s" % (proc_owner[0], proc_owner[2])
            
            process_log_message = "%s, %s, %s, %s, %s, %s, %s\r\n" % (new_process.CreationDate, proc_owner, new_process.ExecutablePath, new_process.CommandLine, new_process.ProcessId, new_process.ParentProcessId, get_process_privileges(new_process.ProcessId))
            
            print process_log_message

            if(fileScan(new_process.ExecutablePath)):
                print "[*] prcoess in hdb"
            
        except Exception as e:
            print e
            pass
