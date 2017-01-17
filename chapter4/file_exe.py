import subprocess
import re

def id_filename(scan_file):
    file_exe  = "C:\\file0.6.2-win32\\bin\\file.exe"
    command = file_exe + " " + scan_file
    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    pattern = "\[[A-Za-z0-9]*\]"
    pat = re.findall(pattern, out)

    try :
        return pat[1][1:-1]
    except :
        return None

def main():
    scan_file = "C:\\file0.6.2-win32\\bin\\file.exe"
    result = id_filename(scan_file)
    print result


if __name__ == "__main__":
    main()
