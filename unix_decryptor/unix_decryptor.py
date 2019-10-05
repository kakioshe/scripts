import crypt
import sys
import os
import argparse
from threading import Thread

def passCheck(cryptPass):
    salt = cryptPass[0:2]
    dictFile = open(sys.argv[2],'r')
    result = []
    for word in dictFile.readlines():
        word = word.strip('\n')
        if not (result):
            t = Thread(target=tryPass, args=(cryptPass, word, salt, result ))
            t.start()
        elif (result):
            return
    t.join()
    print ("Password Not Found.\n") if not result else True

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
    print("Password List and Dictionary List are required. Use -h for help")
    exit(0)

def tryPass(cryptPass, word, salt, result):
    cryptWord = crypt.crypt(word,salt)
    if (cryptWord == cryptPass):
        print ("Found Password: " + word + "\n")
        result.append(word)
        return word
            

def main():
    argCheck()

    passFile = open(sys.argv[1])
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptPass = line.split(":")[1].strip(' ').strip('\n')
            print("Cracking Password For: " + user)
            passCheck(cryptPass)

def parse_arguments():
  parser=argparse.ArgumentParser(
    description='''Basic Unix Decryptor''',
    epilog='-- Created by N4L.A')
  parser.add_argument('PassFile', nargs='+', help='Encrypted Password List File')
  parser.add_argument('dictFile', nargs='+', help='Dictionary list file')
  args=parser.parse_args()
  return args

if __name__ == '__main__':
  arguments = parse_arguments()
  main()