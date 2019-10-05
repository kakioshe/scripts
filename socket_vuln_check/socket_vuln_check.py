import socket
import sys
import os
import re

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return

def checkVulns(banner, filename):
    f = open(filename, 'r')
    for line in f.readlines():
        if line.strip('\n') in banner:
            print("[+] Server is vulnerable: " + banner.strip('\n'))
    return

def main():
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        if not os.path.isfile(filename):
            print(filename + " Does not Exist")
            exit(0)
        if not os.access(filename, os.R_OK):
            print(filename + "Access Denied")
            exit(0)
    else:
        print(str(sys.argv[0] + " Requires a vulnerabilities list"))
        exit(0)
    portList = [21, 22, 25, 80, 110, 443]
    while True:
        baseIp = input("Insert the first three part of IPV4 address (e.g : 192.168.1.) : ")
        valid = re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.$", baseIp)
        if not valid:
            print("Enter correct IP")
        else:
            break
    for x in range(1, 255):
        ip = baseIp + str(x)
        print("[+] Testing IP: " + ip)
        for port in portList:
            banner = retBanner(ip,port)
            if banner:
                print('[+] ' + ip + ': ' + banner)
                checkVulns(banner, filename)
        
    
if __name__ == '__main__':
    main()
