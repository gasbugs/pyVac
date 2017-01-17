#!python
# -*- coding: cp949 -*-
# my_debugger.py
#

from ctypes import *
from my_debugger_defines import *
import os

kernel32 = windll.kernel32

class debugger():
    def __init__(self):
        self.h_process          = None
        self.pid                = None
        self.debugger_active    = False
        self.h_thread           = None
        self.context            = None
        self.breakpoints        = {}
        self.exception          = None
        self.exception_address  = None
        

    def load(self, path_to_exe, commandLine=None):

        # 계산기의 GUI를 보고자 한다면 creation_flags를
        # CREATE_NEW_CONSOLE
        create_flags = DEBUG_PROCESS
        #create_flags = CREATE_NEW_CONSOLE
        
        # 구조체의 인스턴스화
        startupinfo         = STARTUPINFO()
        process_information = PROCESS_INFORMATION()

        # 다음의 두 옵션은 두 프로세스 독립적인 창으로 실행되게 만들어준다.
        # 이는 STARTUPINFO struct 구조체의 설정 내용에 따라 디버기 프로세스에
        # 어떤 영향을 미치는지 보여준다.
        startupinfo.dwFlags     = 0x1
        startupinfo.wShowWindow = 0x5 # 0x0 = invisiable

        # 다음에는 STARTUPINFO struct 구조체 자신의 크기를 나타내는 cb변수 값을
        # 초기화한다.
        startupinfo.cb = sizeof(startupinfo)

        if kernel32.CreateProcessA(path_to_exe,
                                   commandLine,
                                   None,
                                   None,
                                   None,
                                   create_flags,
                                   None,
                                   None,
                                   byref(startupinfo),
                                   byref(process_information)):
            print "[*] We have successfully launched the process!"
            self.pid = process_information.dwProcessId
            print "[*] PID: %d" % self.pid

            # 새로 생성한 프로세스의 핸들을 구한후
            # 나중에 접근하기 위해 저장한다.
            self.h_process = self.open_process(process_information.dwProcessId)

        else:
            print "[*] Error: 0x%08x." % kernel32.GetLastError()

    def open_process(self, pid):

        h_process = kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, pid)
        return h_process

    def attach(self, pid):

        self.h_process = self.open_process(pid)

        # 프로세스에 대한 어태치를 시도한다.
        # 실패하면 호출을 종료한다.
        if kernel32.DebugActiveProcess(pid):
            self.debugger_active    = True
            self.pid                = int(pid)
        else:
            print "[*] Unable to attach to the process"
            print "[*] Error: 0x%08x." % kernel32.GetLastError()

    def run(self):
        # 이제는 디버기에 대한 디버그 이벤트를 처리해야 한다.
        while self.debugger_active == True :
            #self.debugger_active = self.get_debug_event()
            self.get_debug_event()

    def detach(self):

        if kernel32.DebugActiveProcessStop(self.pid):
            print "[*] Finished debugging. Exiting..."
            return True
        else:
            print "There was an error"
            return False

    def open_thread(self, thread_id):

        h_thread = kernel32.OpenThread(THREAD_ALL_ACCESS, None, thread_id)

        if h_thread is not None:
            return h_thread
        else:
            print "[*] Could not obtain a valid thread handle"
            return False

    def enumerate_threads(self):
        thread_entry = THREADENTRY32()
        thread_list = []
        snapshot = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPTHREAD,
                                                        self.pid)
        if snapshot is not None:

            # 먼저 구조체의 크기를 설정해야 한다.
            thread_entry.dwSize = sizeof(thread_entry)
            success = kernel32.Thread32First(snapshot, byref(thread_entry))

            while success:
                if thread_entry.th32OwnerProcessID == long(self.pid):
                    thread_list.append(thread_entry.th32ThreadID)
                success = kernel32.Thread32Next(snapshot,
                                                byref(thread_entry))
            kernel32.CloseHandle(snapshot)
            return thread_list
        else:
            return False

    def get_thread_context(self, thread_id=None, h_thread=None):
        context = CONTEXT()
        context.ContextFlags = CONTEXT_FULL | CONTEXT_DEBUG_REGISTERS

        if not h_thread:
            self.open_thread(thread_id)

            # 스레드의 핸들을 구한다.
            h_thread = self.open_thread(thread_id)
            if kernel32.GetThreadContext(h_thread, byref(context)):
                kernel32.CloseHandle(h_thread)
                return context
            else:
                return False

    def printThreadRegisterInfo(self, tid=None):
        if tid:
            thread_list=[tid]
        else:
            thread_list = self.enumerate_threads()
        # 스레드 리스트의 각 스레드에 대한
        # 레지스터 값을 출력한다.
        for thread in thread_list:
            thread_context = self.get_thread_context(thread)

            # 레지스터 내용을 출력한다.
            print "[*] Dumping registers for thread ID : 0x%08x" %thread
            print "[**] EIP : 0x%08x" %thread_context.Eip
            print "[**] ESP : 0x%08x" %thread_context.Esp
            print "[**] EBP : 0x%08x" %thread_context.Ebp
            print "[**] EAX : 0x%08x" %thread_context.Eax
            print "[**] EBX : 0x%08x" %thread_context.Ebx
            print "[**] ECX : 0x%08x" %thread_context.Ecx
            print "[**] EDX : 0x%08x" %thread_context.Edx
            print "[*] END DUMP"

                                            
    def get_debug_event(self):

        debug_event = DEBUG_EVENT()
        continue_status = DBG_CONTINUE

        if kernel32.WaitForDebugEvent(byref(debug_event), INFINITE):
            

            # 스레드의 컨텍스트 정보를 구한다
            self.h_thread = self.open_thread(debug_event.dwThreadId)
            self.context = self.get_thread_context(self.h_thread)

            #print "Event Code: %d Thread ID: %d" %(
            #    debug_event.dwDebugEventCode, debug_event.dwThreadId)

            # 이벤트 처리
            if debug_event.dwDebugEventCode == EXIT_PROCESS_DEBUG_EVENT:
                print "Process Exit"
                return True
            
            # 발생한 이벤트의 종류가 예외 이벤트이면 그것을 좀 더 자세히 조사한다.
            if debug_event.dwDebugEventCode == EXCEPTION_DEBUG_EVENT:
                # 예외 코드를 구한다.
                exception = debug_event.u.Exception.ExceptionRecord.ExceptionCode
                self.exception_address = \
                    debug_event.u.Exception.ExceptionRecord.ExceptionAddress

                if exception == EXCEPTION_ACCESS_VIOLATION:
                    print "Access Violation Detected"
                    self.printThreadRegisterInfo(debug_event.dwThreadId)
                    os.system("taskkill /f /pid %d"% self.pid)
                    
                    return True

                elif exception == EXCEPTION_BREAKPOINT:
                    continue_status = self.exception_handler_breakpoint()
                    
                elif exception == EXCEPTION_GUARD_PAGE:
                    print "Guard Page Access Detected."

                elif exception == EXCEPTION_SINGLE_STEP:
                    print "Single Stepping"

            

            kernel32.ContinueDebugEvent(
                debug_event.dwProcessId,
                debug_event.dwThreadId,
                continue_status)
            
        return False


    def exception_handler_breakpoint(self):
        print "[*] Inside the breakpoint handler."
        print "Exception Address: 0x%08x" %self.exception_address

        return DBG_CONTINUE

    def read_process_memory(self, address, length):
        data        = ""
        read_buf    = create_string_buffer(length)
        count       = c_ulong(0)

        if not kernel32.ReadProcessMemory(self.h_process,
                                          address,
                                          read_buf,
                                          length,
                                          byref(count)):
            return False
        else :
            data += read_buf.raw
            return data

    def write_process_memory(self, address, data):
        count = c_ulong(0)
        length = len(data)

        c_data = c_char_p(data[count.value:])

        if not kernel32.WriteProcessMemory(self.h_process,
                                          address,
                                          c_data,
                                          length,
                                          byref(count)):
            return False
        else:
            return True

    def bp_set(self, address):
        if not self.breakpoints.has_key(address):
            try:
                # 원래의 바이트 값을 저장한다.
                original_byte= self.read_process_memory
                
                # INT3 opcode를 써넣는다.
                self.write_process_memory(address, "\xCC")
                # 내부리스트에 브레이크 포인트를 등록한다.     
                self.breakpoints[address] (original_byte)
            except:
                return False

            return True

    def func_resolve(self, dll, fuction):

        handle = kernel32.GetModuleHandleA(dll)
        address = kernel32.GetPocAddress(handle, function)

        kernel32.CloseHandle(handle)

        return address
