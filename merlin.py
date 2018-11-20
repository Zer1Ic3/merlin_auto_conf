import sys
import os
import subprocess


cl_agent = '/opt/merlin/cmd/merlinagent'
cl_server = '/opt/merlin'
merlin_back = '/opt/merlin/cmd/merlinagent_bak'


def clean_up():
    os.chdir(cl_agent)
    os.system('rm -R *')
    os.chdir(cl_server)
    os.system('rm -R merlinserver')

print("Starting Merlin now")
os.system('sleep 2')
os.system('c')
clean_up()

interface = input("Please select which interface to be used \n 1)eth0 \n 2)wlan0 \n")
if interface == '1':
    os.system('ip addr |grep eth0')
    os.system('sleep 4')
elif interface == '2':
    os.system('ip addr |grep wlan0')
    os.system('sleep 4')
else:
    print("Error in Interface selection")
    exit(0)

ip_addr = input("Please enter your IP Addr to be used for merlin \n Example https://127.0.0.1:443 \n")

def merlin_agent():
    os.chdir(merlin_back)
    os.system('cp main.go ../merlinagent')
    os.chdir(cl_agent)
merlin_agent()

with open("main.go","r") as f:
    newline=[]
    for word in f.readlines():
        newline.append(word.replace("https://127.0.0.1:443/",ip_addr))
with open("main.go","w") as f:
    for line in newline:
        f.write(line)

os.system('cat main.go')
os.system('sleep 4')
os.system('c')

os.chdir('/opt/merlin/data/x509')
os.system('rm -R server*')
subj = input("Please enter subject name for ssl certifcat \n Example /CN=xx \n")
days = input("Please enter number of days cert must be valid \n Example 2 \n")
subprocess.call(["openssl","req","-x509","-newkey","rsa:4096","-sha256","-nodes","-keyout","server.key","-out","server.crt","-subj", subj,"-days", days])
os.system('sleep 4')
os.system('c')

go_command = input("Please enter go command need to run \n Example GOOS=windows OSARCH=amd64 go build \n")
os.chdir('/tmp')
os.system('rm -R merlin.sh*')

with open("merlin.sh", "w") as f:
    f.write("#!/bin/bash")
    f.write("\n")
    f.write("\n")
    f.write("cd /opt/merlin/cmd/merlinagent/")
    f.write("\n")
    f.write(go_command)
    f.write("\n")
    f.write("cd ../merlinserver")
    f.write("\n")
    f.write("go build")
    f.close()
os.system('chmod +x merlin.sh')
os.system('./merlin.sh')
os.chdir('/opt/merlin/cmd/merlinserver')
os.system('mv merlinserver ../.. ')
os.system('sleep 4')
os.system('c')
ip_addr1 = input("Please enter IP addr of your system: \n")
os.chdir('/opt/merlin')
subprocess.call(["./merlinserver","-i", ip_addr1])

exit(0)
