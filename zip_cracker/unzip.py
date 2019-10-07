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


def argCheck(files):
  if files:
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

def main(zFile, dictfile):

  argCheck([zFile, dictfile])
  zFile = zipfile.ZipFile(zFile)
  dictList = open(dictfile)

  for line in dictList.readlines():
    password = line.strip('\n')
    t = Thread(target=tryPass, args=(zFile, password))
    t.start()

def parse_arguments():
  parser=argparse.ArgumentParser(
    description='''Basic Zip File Password Cracker''',
    usage='unzip.py [-h] -f <ZIPFILE> -d <DICTFILE>',
    epilog='-- Created by N4L.A')
  parser.add_argument('-f', '--file', dest='zFile', type=str,  help='Specify ZIP file')
  parser.add_argument('-d', '--dict', dest='dictfile',type=str, help='Specify Dictionary file')
  args=parser.parse_args()
  if args.zFile == None or args.dictfile == None:
    print(parser.usage)
    exit(0)
  return args.zFile, args.dictfile

if __name__ == '__main__':
  zFile, dictfile = parse_arguments()
  main(zFile, dictfile)