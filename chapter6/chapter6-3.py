import _winreg as winreg

def get_installed_runs():
    python_core = winreg.CreateKey(winreg.HKEY_LOCAL_MACHINE,
                                   "Software\\Microsoft\\Windows\\CurrentVersion\\Run")
    tuple1 = winreg.QueryInfoKey(python_core)

    list1 = []

    for i in range(tuple1[1]):
        try:
            list1.append(winreg.EnumValue(python_core, i))
        except WindowsError:
            break

    winreg.CloseKey(python_core)

    print "List for HKEY_LOCAL_MACHINE\\" + "Software\\Microsoft\\Windows\\CurrentVersion\\Run"

    for (name,value,i) in list1:
        print name, ":", value

get_installed_runs()