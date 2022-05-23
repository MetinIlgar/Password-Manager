import sqlite3 as sl
import random, string

class PasswordManager:
    emailList = set()

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

    @classmethod
    def yourEmails(cls):
        print(cls.emailList)

    def __init__(self, email, passwordLenght = 12):
        self.email = email
        self.passwordLenght = passwordLenght
        self.password = ""
        PasswordManager.emailList.add(self.email)

    def createPassword(self):
        passList = []
        rand_digit = random.choice(PasswordManager.DIGITS)
        rand_upper = random.choice(PasswordManager.UPCASE_CHARACTERS)
        rand_lower = random.choice(PasswordManager.LOCASE_CHARACTERS)
        rand_symbol = random.choice(PasswordManager.SYMBOLS)

        passList.extend([rand_digit, rand_upper, rand_lower, rand_symbol])

        for i in range(self.passwordLenght - 4):
            passList.append(random.choice(PasswordManager.all_characters))
            random.shuffle(passList)

        for x in passList:
            self.password += x






sample_account = PasswordManager("abcde@gmail.com")
sample_account2 = PasswordManager("abcde@outlook.com")

sample_account.yourEmails()
print("------------------------------")

sample_account.createPassword()
print("email: " + sample_account.email)
print("password: " + sample_account.password)


print("------------------------------")

sample_account2.createPassword()
print("email: " + sample_account2.email)
print("password: " + sample_account2.password)