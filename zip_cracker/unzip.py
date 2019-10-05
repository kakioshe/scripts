import zipfile
import sys
import os
import argparse
import re
from threading import Thread

def tryPass(zFile, password):
    try:
      zFile.extractall(pwd=bytes(password, 'utf-8'))
      print('[+] Password = ' + password + '\n')
    except Exception as e:
      pass

def argCheck():
  if len(sys.argv) == 3:
    filename = sys.argv[1]
    dictFile = sys.argv[2]
    if not os.path.isfile(filename):
        print(filename + " Does not Exist")
        exit(0)
    if not os.path.isfile(dictFile):
        print(dictFile + " Does not Exist")
        exit(0)
    if not os.access(filename, os.R_OK):
        print(filename + "Access Denied")
        exit(0)
    if not os.access(dictFile, os.R_OK):
        print(dictFile + "Access Denied")
        exit(0)
  else:
    print("Specify a .zip file and dict list")
    exit(0)


def main():
  argCheck()
  zFile = zipfile.ZipFile(sys.argv[1])
  dictList = open(sys.argv[2])

  for line in dictList.readlines():
    password = line.strip('\n')
    t = Thread(target=tryPass, args=(zFile, password))
    t.start()

def parse_arguments():
  parser=argparse.ArgumentParser(
    description='''Basic Zip File Password Cracker ''')
  parser.add_argument('zipFile', nargs='+', help='ZIP file')
  parser.add_argument('dictFile', nargs='+', help='Dictionary list file')
  args=parser.parse_args()
  return args

if __name__ == '__main__':
  arguments = parse_arguments()
  main()