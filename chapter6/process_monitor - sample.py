#!python
# -*- coding:UTF-8 -*-
# Black Hat Python - 저스틴 자이츠 참고


import win32con
import win32api
import win32security

import wmi
import sys
import os

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

# 로그 파일 표제 생성
log_to_file("Time,User,Executable,CommandLine,PID,Parent,Privileges")

# WMI 인터페이스 초기화
c = wmi.WMI()

# 프로세스 모니터 생성
process_watcher = c.Win32_Process.watch_for("creation")

while True:
    try:
        new_process = process_watcher()
        
        proc_owner  = new_process.GetOwner()
        proc_owner  = "%s\\%s" % (proc_owner[0], proc_owner[2])
        
        process_log_message = "%s, %s, %s, %s, %s, %s, %s\r\n" % (new_process.CreationDate, proc_owner, new_process.ExecutablePath, new_process.CommandLine, new_process.ProcessId, new_process.ParentProcessId, get_process_privileges(new_process.ProcessId))
        
        print process_log_message
        
        log_to_file(process_log_message)
        
    except Exception as e:
        print e
        pass
