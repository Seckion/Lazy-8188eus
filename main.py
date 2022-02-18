import os

if os.geteuid() != 0:
    print('run as root')
    exit()
   
print("""

  _                                 ___  __  ___   ___                 
 | |                               / _ \/_ |/ _ \ / _ \                
 | |     __ _ _____   _   ______  | (_) || | (_) | (_) | ___ _   _ ___ 
 | |    / _` |_  / | | | |______|  > _ < | |> _ < > _ < / _ \ | | / __|
 | |___| (_| |/ /| |_| |          | (_) || | (_) | (_) |  __/ |_| \__ \
 |______\__,_/___|\__, |           \___/ |_|\___/ \___/ \___|\__,_|___/
                   __/ |                                               
                  |___/                                                

>>>>>>>>>>>>>>>>>>>>>>>>> Created By: Seckion <<<<<<<<<<<<<<<<<<<<<<<<<<


""")

os.system('sudo apt-get update && apt-get upgrade')
os.system('apt-get --assume-yes install dkms bc build-essential linux-headers-$(uname -r) ')
os.system('sudo apt-get install linux-headers-$(uname -r)')
os.system('echo "blacklist 8188eu" >>  "/etc/modprobe.d/realtek.conf"')
os.system('echo "blacklist r8188eu" >> "/etc/modprobe.d/realtek.conf"')
os.system('git clone https://github.com/drygdryg/rtl8188eus.git')
os.chdir('rtl8188eus/')
os.system('sudo make')
os.system('sudo make install')
os.system('sudo modprobe 8188eu')

def configure_startup():
    data = """[Unit]
Description=/etc/rc.local Compatibility
ConditionPathExists=/etc/rc.local

[Service]
Type=forking
ExecStart=/etc/rc.local start
TimeoutSec=0
StandardOutput=tty
RemainAfterExit=yes
SysVStartPriority=99

[Install]
WantedBy=multi-user.target"""

    with open("/etc/systemd/system/rc-local.service",'w')as file:
        file.write(data)
        file.close()    

    commands=f"""#!/bin/bash\nsudo modprobe 8188eu\nexit 0"""

    with open("/etc/rc.local",'w')as file:
        file.write(commands)
        file.close()

    os.system("sudo chmod +x /etc/rc.local")
    os.system("sudo systemctl enable rc-local")
    os.system("sudo systemctl start rc-local")
    os.system("sudo systemctl status rc-local")

configure_startup()

print("\nThe Drivers are installed successfully!\n")
