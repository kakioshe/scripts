import zipfile
import sys
import os
import argparse
import re
from threading import Thread

def tryPass(zFile, password):
    try:
      zFile.extractall(pwd=bytes(password, 'utf-8'))
      print('Found Password = ' + password + '\n')
    except Exception:
      pass


def argCheck():
  if len(sys.argv) == 3:
    files = sys.argv[1:]
    for file in files:
        if not os.path.isfile(file):
            print(file) + " Does not exist"
            exit(0)
        if not os.access(file, os.R_OK):
            print(file + " Acess Denied")
            exit(0)
  else:
    print(".zip File and Dictionary List are required. Use -h for help")
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
    description='''Basic Zip File Password Cracker ''',
    epilog='-- Created by N4L.A')
  parser.add_argument('zipFile', nargs='+', help='ZIP file')
  parser.add_argument('dictFile', nargs='+', help='Dictionary list file')
  args=parser.parse_args()
  return args

if __name__ == '__main__':
  arguments = parse_arguments()
  main()