import base64
import hashlib
from cryptography.fernet import Fernet
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
'''
def write_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)'''


def load_key():
    file = open(os.path.join(BASE_DIR, "key.key"), "rb")
    key = file.read()
    file.close()
    return key

pwd = input("Master pwd:")
key = base64.urlsafe_b64encode(hashlib.sha256(load_key() + pwd.encode()).digest())
fer = Fernet(key)

def view():
   with open(os.path.join(BASE_DIR, 'passwords.txt'), 'r') as f:
        for line in f.readlines():
            data = line.rstrip()
            user, passw = data.split("|")
            print("User: ", user, "| Password: ",
             fer.decrypt(passw.encode()).decode())



def add():
    name = input('account Name: ')
    password = input("password:")

    with open(os.path.join(BASE_DIR, 'passwords.txt'), 'a') as f:
        f.write(name + "|" + fer.encrypt(password.encode()).decode() + "\n")

def delete():
    with open(os.path.join(BASE_DIR, 'passwords.txt'), 'r') as f:
        lines = f.readlines()
    
    for i, line in enumerate(lines):
        user = line.rstrip().split("|")[0]
        print(i+1, "-", user)
    choice = input("Number to delete (press enter to cancel): ")
    if not choice.isdigit or not 1 <= int(choice) <= len(lines):
        print("Cancelled")
        return
    lines.pop(int(choice) - 1)

    with open(os.path.join(BASE_DIR, 'passwords.txt'), 'w') as f:
        f.writelines(lines)
    print("Deleted")

while True:
    mode = input("Add new, view existing ones or delete? press q to quit: ")
    if mode == "q":
        break

    if mode == "view":
        view()
    elif mode == "add":
        add()
    elif mode == "delete":
        delete()
    else:
        print("Invalid. type 'view', 'add' or 'delete'")
        continue
#deleting works, adding works, viewing works
