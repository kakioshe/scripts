import socket

def retBanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return

def main():
    portList = [21, 22, 25, 80, 110, 443]
    print("Python Check")
    for x in range(1, 255):
        ip = '192.168.95.' + str(x)
        print("Trying IP : " + ip)
        for port in portList:

            banner = retBanner(ip, port)
            if banner:
                print('[+] ' + ip + ': ' + banner)

if __name__ == '__main__':
    main()
