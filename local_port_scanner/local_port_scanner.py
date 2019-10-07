import argparse
import os
import subprocess
from shutil import which 

REQ_TOOL = 'nmap'

def check_tool():
  return which(REQ_TOOL) is not None

def outputFilter(scanResult):
  localDevices = []
  tempData = []
  localDeviceIp = []
  for line in scanResult: 
    if line == '' and tempData != []:
      localDevices.append(tempData)
      tempData = []
    elif line != '':
      if "All 1000 scanned" in line or 'Nmap done' in line:
        tempData = []
      else:
        tempData.append(line)
        if 'Nmap scan report for' in line:
          localDeviceIp.append(line.split(' ')[-1].strip('()'))
  return localDevices, localDeviceIp

def retScanIp():
  localIp = os.popen(r'ifconfig en0 | grep "inet\ " | cut -d: -f2 | cut -d" " -f2').read()
  localIp = localIp.split('.')[:-1]
  return localIp[0] + '.' + localIp[1] + '.' + localIp[2] + '.*'

def fetchNMap(ip):
  nmapScan = subprocess.Popen(('nmap', ip), stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
  scanResult, err = nmapScan.communicate()
  if (err):
    print(err)
    exit(0)
  return scanResult

def printOutput(localDevices, localDeviceIp):
  for device in localDevices:
    deviceName = device[0].split(' ')[-2:]
    if deviceName[0] == 'for':
      print(deviceName[1])
    else: 
      print(deviceName[0] + ' ' + deviceName[1])
    print(device[3])
    i = 4
    while i < len(device):
      print(device[i])
      i += 1
    print()
  print("Connected devices: ", end = '' )
  print(*localDeviceIp, sep = ', ')


def main():

  if not (check_tool()):
    print("NMap is required")
    exit(0)
  
  scanIp = retScanIp()
  print("\nScanning for {} ... \n".format(scanIp))

  scanResult = fetchNMap(scanIp)
  localDevices, localDeviceIp = outputFilter(scanResult.decode('utf-8').split('\n')[1:])

  printOutput(localDevices, localDeviceIp)

def parse_arguments():
  parser=argparse.ArgumentParser(
    description='''Local Network Port Scanner''',
    usage='unix_decryptor.py [-h]',
    epilog='-- Created by N4L.A')
  args=parser.parse_args()
    
  return args

if __name__ == "__main__":
  args = parse_arguments()
  main()