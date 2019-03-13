#!/usr/bin/python
import crypt
import sys
import string
import random
import argparse

def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--string',default='',help='Password string, default is empty and will be generate randomly whith ASCII char letters')
    parser.add_argument('-l','--length',default=8, help='Length of password, default is "8"')
    parser.add_argument('-c','--create-hash',default='yes', help='Create a hash for unix account, default is "yes"')
    parser.add_argument('-f','--vault-password-file',default='/home/grahov/.ansible_pass.txt',help='Path to vault password file')
    return parser

from ansible.parsing.vault import VaultLib
from ansible.parsing.vault import VaultSecret



def random_string(length):
    return ''.join(random.choice(string.ascii_letters) for m in range(length))

def read_text_file(file_path):
    return open(file_path).read().replace('\n','')


if __name__ == "__main__":
    parser = createParser()
    namespase = parser.parse_args(sys.argv[1:])
    vaultsecret = read_text_file(namespase.vault_password_file)

    vault = VaultLib([(True, VaultSecret(vaultsecret))])
    if namespase.string != '':
      password = namespase.string
    else:
      password = random_string(int(namespase.length))
print(password)
if namespase.create_hash == 'yes':
  hash_string = crypt.crypt(password)
  print(hash_string)
  encrypted_str = vault.encrypt(hash_string)
  print(encrypted_str)
else:
  encrypted_str = vault.encrypt(password)
  print(encrypted_str)

