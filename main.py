import sqlite3 as sl
import random, string

import base64
import os,sys
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class SetAccount:
    LOCASE_CHARACTERS = list(string.ascii_lowercase)
    UPCASE_CHARACTERS = list(string.ascii_uppercase)
    DIGITS = list(string.digits)
    SYMBOLS = list(string.punctuation)

    random.shuffle(LOCASE_CHARACTERS)
    random.shuffle(UPCASE_CHARACTERS)
    random.shuffle(DIGITS)
    random.shuffle(SYMBOLS)

    all_characters = LOCASE_CHARACTERS + UPCASE_CHARACTERS + DIGITS + SYMBOLS
    random.shuffle(all_characters)


    def __init__(self, email, encryption_password, passwordLenght = 12):
        self.email = email
        self.encryption_password = encryption_password.encode()
        self.passwordLenght = passwordLenght
        self.password = ""
        self.salt = os.urandom(32)
        self.token = b""
        self.link = "example.com"

        self.createPassword()
        self.encrypt()
        self.setData()

    def createPassword(self):
        passList = []
        rand_digit = random.choice(SetAccount.DIGITS)
        rand_upper = random.choice(SetAccount.UPCASE_CHARACTERS)
        rand_lower = random.choice(SetAccount.LOCASE_CHARACTERS)
        rand_symbol = random.choice(SetAccount.SYMBOLS)

        passList.extend([rand_digit, rand_upper, rand_lower, rand_symbol])

        for i in range(self.passwordLenght - 4):
            passList.append(random.choice(SetAccount.all_characters))
            random.shuffle(passList)

        for x in passList:
            self.password += x


    def encrypt(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.encryption_password))
        f = Fernet(key)
        self.token = f.encrypt(self.password.encode())

    def setData(self):
        with sl.connect('PasswordDatabase.sqlite') as db:
            cur = db.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Password_Book (Link, Email, Password, Salt)")
            cur.execute(
                "INSERT INTO Password_Book VALUES (? ,? ,? ,? )", (self.link, self.email, self.token, self.salt))
            db.commit()


class GetAccount:
    def __init__(self, encryption_password, website):
        self.encryption_password = encryption_password.encode()
        self.password = ""
        self.website = website

        with sl.connect('PasswordDatabase.sqlite') as db:
            cur = db.cursor()
            cur.execute(f"SELECT * FROM Password_Book WHERE Link LIKE '%{self.website}%'")
            data = cur.fetchall()
            if len(data) == 0:
                sys.exit("Website not found.")
            elif len(data)== 1:
                for i in data:
                    self.link = i[0]
                    self.email = i[1]
                    self.token = i[2]
                    self.salt = i[3]
            elif len(data) > 1:
                k = 0
                for i in data:
                    print(f"[{k}] Link:{i[0]}, Email: {i[1]}")
                    k = k+1
                x = int(input("Select account: "))

                self.link = data[x][0]
                self.email = data[x][1]
                self.token = data[x][2]
                self.salt = data[x][3]


        self.decrypt()

    def decrypt(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=390000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.encryption_password))
        f = Fernet(key)
        self.password = f.decrypt(self.token).decode()

example = SetAccount("abcd@gmail.com", "98742365")

print(example.password)

print("-----------")

x = GetAccount("98742365", "example")

print(x.password)
