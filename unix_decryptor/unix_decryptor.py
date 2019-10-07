import crypt
import sys
import os
import argparse
from threading import Thread

def passCheck(cryptPass, dictfile):
    salt = cryptPass[0:2]
    dictFile = open(dictfile,'r')
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

def argCheck(files):
  if files:
    for file in files:
        if not os.path.isfile(file):
            print((file) + " Does not exist")
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
            
def main(passfile, dictfile):
    argCheck([passfile, dictfile])

    passFile = open(passfile)
    for line in passFile.readlines():
        if ":" in line:
            user = line.split(":")[0]
            cryptPass = line.split(":")[1].strip(' ').strip('\n')
            print("Cracking Password For: " + user)
            passCheck(cryptPass, dictfile)

def parse_arguments():
  parser=argparse.ArgumentParser(
    description='''Basic Unix Decryptor''',
    usage='unix_decryptor.py [-h] [-f --file PASSFILE] [-d --dict DICTFILE]',
    epilog='-- Created by N4L.A')
  parser.add_argument('-f', '--file', dest='passfile', type=str,  help='Specify password file')
  parser.add_argument('-d', '--dict', dest='dictfile',type=str, help='Specify Dictionary file')
  args=parser.parse_args()
  if args.passfile == None or args.dictfile == None:
    print(parser.usage)
    exit(0)
    
  return args.passfile, args.dictfile

if __name__ == '__main__':
  passfile, dictfile = parse_arguments()
  main(passfile, dictfile)