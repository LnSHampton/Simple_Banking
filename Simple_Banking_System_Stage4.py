# -*- coding: utf-8 -*-
"""
Created on Wed Jan 13 23:10:16 2021

@author: LnSHa

Stage 4/4: Advanced system

DESCRIPTION

You have created the foundation of our banking system. Now let's take the 
opportunity to deposit money into an account, make transfers and close an 
account if necessary.

Now your menu should look like this:

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit

If the user asks for Balance, you should read the balance of the account from 
the database and output it into the console.

Add income item should allow us to deposit money to the account.

Do transfer item should allow transferring money to another account. You 
should handle the following errors:

If the user tries to transfer more money than he/she has, output: "Not enough 
money!"
If the user tries to transfer money to the same account, output the following 
message: “You can't transfer money to the same account!”
If the receiver's card number doesn’t pass the Luhn algorithm, you should 
output: “Probably you made a mistake in the card number. Please try again!”
If the receiver's card number doesn’t exist, you should output: “Such a card 
does not exist.”
If there is no error, ask the user how much money they want to transfer and 
make the transaction.
If the user chooses the Close account item, you should delete that account 
from the database.

Do not forget to commit your DB changes right after executing a query!

Examples
The symbol > represents the user input. Notice that it's not a part of the 
input.

Example 1:

1. Create an account
2. Log into account
0. Exit
>1

Your card has been created
Your card number:
4000009455296122
Your card PIN:
1961

1. Create an account
2. Log into account
0. Exit
>1

Your card has been created
Your card number:
4000003305160034
Your card PIN:
5639

1. Create an account
2. Log into account
0. Exit
>2

Enter your card number:
>4000009455296122
Enter your PIN:
>1961

You have successfully logged in!

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>2

Enter income:
>10000
Income was added!

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>1

Balance: 10000

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>3

Transfer
Enter card number:
>4000003305160035
Probably you made a mistake in the card number. Please try again!

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>3

Transfer
Enter card number:
>4000003305061034
Such a card does not exist.

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>3

Transfer
Enter card number:
>4000003305160034
Enter how much money you want to transfer:
>15000
Not enough money!

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>3

Transfer
Enter card number:
>4000003305160034
Enter how much money you want to transfer:
>5000
Success!

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>1

Balance: 5000

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit

>0
Bye!
Example 2:

1. Create an account
2. Log into account
0. Exit
>1

Your card has been created
Your card number:
4000007916053702
Your card PIN:
6263

1. Create an account
2. Log into account
0. Exit
>2

Enter your card number:
>4000007916053702
Enter your PIN:
>6263

You have successfully logged in!

1. Balance
2. Add income
3. Do transfer
4. Close account
5. Log out
0. Exit
>4

The account has been closed!

1. Create an account
2. Log into account
0. Exit
>2

Enter your card number:
>4000007916053702
Enter your PIN:
>6263

Wrong card number or PIN!

1. Create an account
2. Log into account
0. Exit
>0

Bye!



"""
import random
import sys
import sqlite3

conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS card (id integer, number, pin, balance integer default 0) """)


class CreditCard:
    IIN = '400000'

    def __init__(self):
        self.balance = 0
        self.PIN = '{:0<4}'.format(random.randint(0, 9999))
        while True:  # Check whether the account already exists
            self.cardnumber = self.generate_card_number()
            cur.execute("SELECT 1 FROM card WHERE number = ?", (self.cardnumber,))
            if not cur.fetchone():
                break

    def generate_card_number(self):
        t_cardnumber = CreditCard.IIN + '{:0<9}'.format(random.randint(0, 999999999))
        checksum = (10 - (self.luhn(t_cardnumber) % 10)) % 10  # catches a zero remainder
        return t_cardnumber + str(checksum)
    
    def luhn(self, c_number):
        ns = list(map(int, c_number))  # convert string into a numeric list
        for n in range(0, len(ns), 2):  # manipulate every other digit
            ns[n] = ns[n] * 2 if ns[n] * 2 < 10 else ns[n] * 2 - 9
        return sum(ns)


def checksum_check(c_number):
    ns = list(map(int, c_number[:-1]))  # Convert up to the last digit
    for n in range(0, len(ns), 2):  # manipulate every other digit
        ns[n] = ns[n] * 2 if ns[n] * 2 < 10 else ns[n] * 2 - 9
    return c_number[-1] == str((10 - (sum(ns) % 10)) % 10)


def access_account():
    user_cardnumber = input('Enter your card number:\n')
    user_pin = input('Enter your PIN:\n')
    r = cur.execute("SELECT id, balance FROM card WHERE number = ? and pin = ?",
                   (user_cardnumber, user_pin)).fetchone()
    if r:
        a_id, a_balance = r[0], r[1]
        print('You have successfully logged in!')
        command = int(input(menu_02).strip())
        while True:
            if command == 1:  # Balance
                print(f'Balance {a_balance}')
            elif command == 2:  # Add income
                income = int(input('Enter income:\n'))
                a_balance += income
                cur.execute("UPDATE card SET balance = ? WHERE id = ?", (a_balance, a_id))
                conn.commit()
                print('Income was added!')
            elif command == 3:  # Do transfer
                account_transfer(a_id, a_balance)
            elif command == 4:  # Close account
                cur.execute("DELETE FROM card WHERE id = ?", (a_id,))
                conn.commit()
                print('The account has been closed!')
            elif command == 5:  # Log out
                break
            elif command == 0:  # Exit
                print('Bye!')
                sys.exit()
            command = int(input(menu_02).strip())
    else:
        print('Wrong card number or PIN!')


def account_transfer(p_id, p_balance):
    to_card = input('Transfer\nEnter card number:\n')
    if not checksum_check(to_card):
        print('Probably you made a mistake in the card number. Please try again!')
    else:
        r = cur.execute("SELECT id, balance FROM card WHERE number = ?",
                        (to_card,)).fetchone()
        if not r:
            print('Such a card does not exist.')
        else:
            to_id, to_bal = r[0], r[1]
            t_funds = int(input('Enter how much money you want to transfer:\n'))
            if t_funds > p_balance:
                print('Not enough money!')
            else:
                cur.execute("UPDATE card SET balance = ? WHERE id = ?", (p_balance - t_funds, p_id))
                cur.execute("UPDATE card SET balance = ? WHERE id = ?", (to_bal + t_funds, to_id))
                conn.commit()
                print('Success!')
                

def print_db():
    cur.execute("SELECT id, number, pin, balance FROM card ORDER BY number DESC")
    print('{:<4}  {:<16} {:<4} {:<8}'.format('ID', 'NUMBER', 'PIN', 'BALANCE'))
    print('{:-<4}  {:-<16} {:-<4} {:-<8}'.format('-', '-', '-', '-'))
    for r in cur:
        print('{:<4}  {:<16} {:<4} {:>8}'.format(r[0], r[1], r[2], r[3]))


random.seed()
# menu_01 = """1. Create an account\n2. Log into account\n0. Exit\n"""
menu_01 = """1. Create an account\n2. Log into account\n3. List Accounts\n0. Exit\n> """
menu_02 = """1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n> """
gv_command = int(input(menu_01).strip())
while gv_command != 0:
    if gv_command == 1:
        new_card = CreditCard()
        cur.execute("INSERT INTO card (number, pin, balance)values (?, ?, ?)",
                    (new_card.cardnumber, new_card.PIN, new_card.balance))
        conn.commit()
        print(f'Your card has been created\nYour card number:\n{new_card.cardnumber}')
        print(f'Your card PIN:\n{new_card.PIN}')
    elif gv_command == 2:
        access_account()
    elif gv_command == 3:
        print_db()
    gv_command = int(input(menu_01).strip())
print('Bye!')

cur.close()
conn.close()

#%%
# When I posted my solution, mine was the shortest of all others
#%%
# Vitalii Yatchenko's solution
# This is a beautiful solution. I like the way it is organized.

# banking.py
from card_manager import CreditCardManager
from db import CreditCard, CardsModel, SQLiteDBHelper


class WrongCredentialsError(Exception):
    pass


class BankApp:

    def __init__(self, cards_model: CardsModel):
        self.cards_model = cards_model

    def create_card(self) -> CreditCard:
        card = self.cards_model.add_card()
        print('Your card has been created')
        print('Your card number:')
        print(card.number)
        print('Your card PIN:')
        print(card.pin)
        return card

    def login(self, card_number: str, pin: str) -> CreditCard:
        card = self.cards_model.get_card(card_number, pin)
        if not card:
            print('Wrong card number or PIN!')
            raise WrongCredentialsError
        return card

    def main_menu(self):

        while True:
            print('1. Create an account')
            print('2. Log into account')
            print('0. Exit')

            decision = int(input())

            if decision == 1:
                card = bank_app.create_card()

            if decision == 2:
                card_number = input('Enter your card number:')
                pin = input('Enter your PIN:')
                try:
                    card = bank_app.login(card_number, pin)
                except WrongCredentialsError:
                    continue
                print('You have successfully logged in!')

                self.user_menu(card)

            if decision == 0:
                print('Bye!')
                exit()

    def user_menu(self, card: CreditCard):
        while True:
            print('1. Balance')
            print('2. Add income')
            print('3. Do transfer')
            print('4. Close account')
            print('5. Log out')
            print('0. Exit')

            decision = int(input())

            if decision == 0:
                print('Bye!')
                exit()

            if decision == 1:
                balance = self.cards_model.get_card(card.number, card.pin).balance
                print(f'Balance: {balance}')

            if decision == 2:
                print("Enter income:")
                income = int(input())
                self.cards_model.add_income(card.number, income)
                print("Income was added!")

            if decision == 3:
                print("Transfer")
                print("Enter card number")
                card_number = input()

                if not CreditCardManager.check_card_number_validity(card_number):
                    print('Probably you made a mistake in the card number. Please try again!')
                    continue

                if not self.cards_model.check_card_existence(card_number):
                    print('Such a card does not exist.')
                    continue

                print('Enter how much money you want to transfer:')
                amount = int(input())

                if self.cards_model.get_card(card.number, card.pin).balance < amount:
                    print('Not enough money!')
                    continue

                self.cards_model.send_money(card, card_number, amount)

                print('Success!')

            if decision == 4:
                self.cards_model.delete_card(card)
                print('The account has been closed!')
                break

            if decision == 5:
                print('You have successfully logged out!')
                break

db_manager = SQLiteDBHelper("card.s3db")
cards_model = CardsModel(db_manager)
bank_app = BankApp(cards_model)

bank_app.main_menu()

# His database routines
# db.py
from dataclasses import dataclass
from sqlite3 import connect, Cursor, Connection
from typing import Optional
from card_manager import CreditCardManager

card_table_name = 'card'


class SQLiteDBHelper:

    def __init__(self, dbname: str = "card.s3db"):
        self.dbname = dbname
        self.connection: Connection = connect(dbname)
        self.cursor: Cursor = self.connection.cursor()
        self.setup()

    def setup(self):
        # creating card table
        create_table_sql = f"""CREATE TABLE IF NOT EXISTS {card_table_name} (
                            id          integer PRIMARY KEY AUTOINCREMENT NOT NULL,
                            number      text NOT NULL,
                            pin         text NOT NULL,
                            balance     integer default 0
        );"""
        self.cursor.execute(create_table_sql)
        self.connection.commit()

    def execute_query(self, query, args=tuple()):
        self.cursor.execute(query, args)
        self.connection.commit()

    def execute_multiple(self, query):
        self.cursor.executescript(query)
        self.connection.commit()

    def delete_item(self, table_name, iid):
        query = f"DELETE FROM {table_name} WHERE id = (?)"
        args = (iid,)
        self.execute_query(query, args)

    def get_item(self, query, args=tuple()):
        self.cursor.execute(query, args)
        return self.cursor.fetchone()

    def get_all_items(self, query, args=tuple()):
        self.cursor.execute(query, args)
        return self.cursor.fetchall()


@dataclass
class CreditCard:

    def __init__(self, card_id: int, number: str, pin: str, balance: int):
        self.id = card_id
        self.number = number
        self.pin = pin
        self.balance = balance


class CardsModel:

    def __init__(self, db_manager: SQLiteDBHelper):
        self.db_manager = db_manager

    def add_card(self) -> CreditCard:
        card_number, pin = CreditCardManager.generate_credit_card()
        query = f"INSERT INTO {card_table_name} (number, pin, balance) VALUES (?, ?, ?)"
        args = (card_number, pin, 0)
        res = self.db_manager.execute_query(query, args)
        return self.get_card(card_number, pin)

    def delete_card(self, card: CreditCard):
        self.db_manager.delete_item(card_table_name, card.id)

    def get_card(self, number, pin) -> Optional[CreditCard]:
        query = f"SELECT id, number, pin, balance  FROM {card_table_name} WHERE number = (?) AND pin = (?)"
        args = (number, pin)
        card = self.db_manager.get_item(query, args)
        return CreditCard(*card) if card else None

    def check_card_existence(self, number) -> bool:
        query = f"SELECT number FROM {card_table_name} WHERE number = (?)"
        args = (number,)
        return self.db_manager.get_item(query, args) is not None

    def add_income(self, card_number, amount):
        query = f"""
        UPDATE {card_table_name}
        SET balance = balance + (?)
        WHERE number = (?);
        """
        args = (amount, card_number)
        self.db_manager.execute_query(query, args)

    def send_money(self, sender_card: CreditCard, recipient_card_number: str, amount):
        query = f"""
        UPDATE {card_table_name}
        SET balance = balance - {amount}
        WHERE number = {sender_card.number} AND pin = {sender_card.pin};
        UPDATE {card_table_name}
        SET balance = balance + {amount}
        WHERE number = {recipient_card_number};
        """
        self.db_manager.execute_multiple(query)

    def get_all_cards(self):
        sql = f"SELECT * FROM {card_table_name}"
        return self.db_manager.get_all_items(sql)

# His Card_Manager routine
# card_manager.py
import random
import string


class CreditCardManager:
    IIN = '400000'

    @classmethod
    def generate_credit_card(cls) -> tuple:
        return cls._generate_card_number(), cls._generate_pin()

    @staticmethod
    def _generate_pin() -> str:
        return ''.join(random.choices(string.digits, k=4))

    @classmethod
    def _generate_card_number(cls) -> str:
        generated_number = cls.IIN + ''.join(random.choices(string.digits, k=9))
        return generated_number + str(cls._get_checksum(generated_number))

    @classmethod
    def check_card_number_validity(cls, card_number: str):
        checksum: int = cls._get_checksum(card_number[:-1])
        return checksum == int(card_number[-1])

    @staticmethod
    def _get_checksum(code: str) -> int:
        """
        Counts checksum for card number using Lunh algorithm
        :param code:
        :return:
        """
        total = 0

        for index, digit in enumerate(code):
            digit = int(digit)
            if (index + 1) % 2 != 0:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit

        checksum = 10 - total % 10

        return checksum if checksum != 10 else 0



#%%

# Nikita Tihhomirov's solution
# banking.py
import random
import time
import sys
import sqlite3

# sample_database = {
# 4000000123094911:'4211',
# 4000001223243211:'5421',
# 4000004312233543:'4443',
# 4000008431322121:'1255'
# }

# creating a database:
##______________________DB Layer_________________________

db = sqlite3.connect('card.s3db')  # card.s3db
sql = db.cursor()
sql.execute("""CREATE TABLE IF NOT EXISTS card 
(id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER);""")
db.commit()


def insert_record(account):
    # id_n = 0
    with db:
        sql.execute("SELECT * from card WHERE ID = (SELECT MAX(ID) FROM card)")
        id_n = sql.fetchone()
        if id_n == None:
            id_n_n = 1
        else:
            id_n_n = int(id_n[1])
            id_n_n = id_n_n + 1

        sql.execute("INSERT INTO card (id, number, pin, balance) VALUES(?, ?, ?, ?)",
                    (int(id_n_n), str(account.card_no), str(account.pin_no), int(account.balance)))
        db.commit()


def check_if_in_db(account_no):
    with db:
        sql.execute("SELECT number FROM card WHERE number = ?", (account_no,))
        acc_data = sql.fetchone()
        if acc_data == None:
            return False
        else:
            return True


def fetch_login(account):
    with db:
        sql.execute("SELECT * FROM card WHERE number = ?", (account.card_no,))
        return_data = sql.fetchone()
        if return_data is not None:
            card_n, pin_n = int(return_data[1]), int(return_data[2])
            # print(type(card_n))
            # print(type(pin_n))
            # print(type(account.card_no))
            # print(type(account.pin_no))
            # print(card_n, pin_n, account.card_no, account.pin_no)

            if card_n == int(account.card_no) and pin_n == int(account.pin_no):
                return True
            else:
                return False
        else:
            return False


def add_income(account):
    with db:
        sql.execute("SELECT balance from card WHERE number = ?", (account.card_no, ))
        current_bal = int(sql.fetchone()[0])
        current_bal = current_bal + account.balance
        sql.execute("UPDATE card set balance = ? where number = ? ", (current_bal, account.card_no))
        db.commit()


def transfer_balance(account, account2, amount_to_transfer):
    with db:
        sql.execute("SELECT balance FROM card WHERE number = ?", (account2.card_no,))
        balance2 = int(sql.fetchone()[0])

        balance1 = account.balance
        balance1 = balance1 - amount_to_transfer
        balance2 = balance2 + amount_to_transfer

        sql.execute("UPDATE card set balance = ? where number = ?", (balance1, account.card_no,))
        sql.execute("UPDATE card set balance = ? where number = ?", (balance2, account2.card_no,))

        db.commit()


# def fetch_account_data(account):


def delete_account(account):
    with db:
        sql.execute("DELETE FROM card WHERE number = ?", (account.card_no,))
        db.commit()


def verify_luhn_value(temp_card_num):
    temp_card_no = [int(x) for x in temp_card_num[::-1]]
    sum1 = sum(temp_card_no[0::2])
    sum2 = sum([(z * 2) % 10 + (z * 2) // 10 if z >= 5 else z * 2 for z in temp_card_no[1::2]])
    sum_final = sum1 + sum2
    sum_final = str(sum_final)
    if sum_final[-1] == '0':
        return True
    else:
        return False


def fetch_balance(account):
    with db:
        sql.execute("SELECT * FROM card where number = ?", (account.card_no,))
        balance_n = sql.fetchone()
        return balance_n


##____________________End - DB Layer

##_____________________Record - class

class Account():

    def __init__(self, card_no, pin_no, balance):
        self.card_no = card_no
        self.pin_no = pin_no
        self.balance = balance
        # self.account_no = self.card_no[5:9]
        # self.customer_record = {'name': '', 'last_name': ''}

    def create_account(self):
        def generate_account_no():
            while True:
                account_no = ''
                temp_list = []
                random.seed(time.process_time())
                temp_list.append([random.randint(0, 9) for x in range(9)])
                temp_no = [4, 0, 0, 0, 0, 0] + (temp_list[0])
                temp_sum_sum = [(z * 2) % 10 + (z * 2) // 10 if z >= 5 else z * 2 for z in temp_no[0::2]]
                temp_sum_no = [int(x) for x in temp_no[1::2]]
                pre_final_no = sum(temp_sum_sum) + sum(temp_sum_no)
                control_num = (pre_final_no * 9) % 10
                account_no = ''.join(str(y) for y in temp_no)
                account_no = account_no + str(control_num)
                check_db = check_if_in_db(account_no)
                if check_db == False:
                    return account_no
                    break
                else:
                    continue

        self.card_no = generate_account_no()

    def create_pin(self):
        random.seed(time.process_time())
        temp_pin_no = str(random.randint(0, 9999))
        self.pin_no = temp_pin_no.zfill(4)

    def account_getter(self):
        return account.card_no

    def account_setter(self, acc_no):
        self.card_no = acc_no[1]
        self.pin_no = acc_no[2]
        self.balance = int(acc_no[3])


# Validating the Luhn algorithm checksum when entering the card number


while True:
    break_loop = False
    print('1. Create an account' + '\n' + '2. Log into account' + '\n' + '' + '0. Exit')
    choice = int(input('Enter number'))
    if choice == 1:
        account = Account(card_no=None, pin_no=None, balance=0)
        account.create_account()
        account.create_pin()
        print('Your card has been created')
        print('Your card number:')
        print(account.card_no)
        print('Your card PIN:')
        print(account.pin_no)
        # account.store_account_details()
        # sample_database.update({int(account.card_no): account.pin_no})
        # check the id of the last record and add extra to the id. If no id, start with id one
        # sample_database.execute("INSERT INTO cards (id, number, pin, balance) VALUES (?,?,?,?)", id_n, account.card_no, account.pin_no, account_balance)
        insert_record(account)

    if choice == 2:
        account = Account(card_no=input('Enter your card number: '), pin_no=input('Enter your PIN: '), balance=0)
        account_data = fetch_login(account)
        print(account_data)
        if account_data == True:
            print('You have successfully logged in!')
            while True:
                # current_account = account.account_getter()
                # account.account_setter(current_account)
                print('1. Balance')
                print('2. Add income')
                print('3. Do transfer')
                print('4. Close account')
                print('5. Log out')
                print('0. Exit')
                login_options = int(input('Enter a number: '))
                if login_options == 1:
                    account.balance = int(fetch_balance(account)[3])
                    print('Balance: ', account.balance)
                    print(account.card_no)
                    continue
                if login_options == 2:
                    account.balance = int(input('Enter income: '))
                    add_income(account)
                    print('Income was added!')
                    continue
                if login_options == 3:
                    temp_card_num = input('Enter your card number: ')
                    luhn_checksum = verify_luhn_value(temp_card_num)
                    if luhn_checksum == False:
                        print('Probably you made a mistake in the card number. Please try again!')
                        continue
                    else:
                        check_card_exists = check_if_in_db(temp_card_num)
                        #print(check_card_exists)
                        #print(type(check_card_exists))
                        #print(check_card_exists[1])
                        if check_card_exists == False:
                            print('Such a card does not exist')
                            continue
                        else:
                            if account.card_no == temp_card_num:
                                print("You can't transfer money to the same account!")
                                continue
                            else:
                                current_balance = int(fetch_balance(account)[3])
                                account2 = Account(card_no=temp_card_num, pin_no=None, balance=0)
                                acc2_data = fetch_balance(account2)
                                account2.account_setter(acc2_data)
                                # account.account_setter(temp_card_num)
                                print(account2.__dict__)
                                print(account.__dict__)
                                amount_to_transfer = int(input('Enter the amount to be transferred:'))
                                if amount_to_transfer > current_balance:
                                    print('Not enough money!')
                                    continue
                                else:
                                    transfer_balance(account, account2, amount_to_transfer)
                                    print(account.balance, account2.balance)
                                    continue

                if login_options == 4:
                    delete_account(account)
                    print('The account has been closed!')
                    break
                if login_options == 5:
                    print('You have successfully logged out!')
                    break
                if login_options == 0:
                    break_loop = True
                    break
        else:
            print('Wrong card number or PIN!')
            continue
    if choice == 0 or break_loop == True:
        print('Bye!')
        break
#%%
# JogikInt's solution
from random import randint
import sqlite3


class BankingSystem:
    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        try:
            self.cur.execute('CREATE TABLE card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER '
                             'DEFAULT 0);')
            self.conn.commit()
        except sqlite3.OperationalError:
            pass
        self.start_menu()

    def start_menu(self):
        user_input = input('1. Create an account\n2. Log into account\n0. Exit\n')
        if user_input == '0':
            print('\nBye')
            quit()
        elif user_input == '1':
            self.db_card_add()
        elif user_input == '2':
            self.login()
        self.start_menu()

    def db_card_add(self):
        card_number = self.luhn_card_create()
        pin = str(randint(1, 9999)).zfill(4)
        self.cur.execute(f'INSERT INTO card (number, pin) VALUES ({card_number}, {pin});')
        self.conn.commit()
        print(f'\nYour card has been created\nYour card number:\n{card_number}\nYour card PIN:\n{pin}\n')

    def check_login(self, card_number, pin):
        self.cur.execute(f'SELECT id FROM card WHERE number = {card_number} AND pin = {pin};')
        return bool(self.cur.fetchall())

    def login(self):
        card_number = input('\nEnter your card number:\n')
        pin = input('Enter your PIN:\n')
        if self.check_login(card_number, pin):
            print('\nYou have successfully logged in!\n')
            self.logged_in_menu(card_number)
        print('\nWrong card number or PIN!\n')
        self.start_menu()

    def logged_in_menu(self, card_number):
        user_input = input('1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n')
        if user_input == '0':
            print('\nBye')
            quit()
        elif user_input == '1':
            print(f'\nBalance: {self.check_balance(card_number)}\n')
        elif user_input == '2':
            self.add_income(card_number)
        elif user_input == '3':
            self.transfer(card_number)
        elif user_input == '4':
            self.close_account(card_number)
            self.start_menu()
        elif user_input == '5':
            self.start_menu()
        self.logged_in_menu(card_number)

    def check_balance(self, card_number):
        self.cur.execute(f'SELECT balance FROM card WHERE number = {card_number};')
        return self.cur.fetchall()[0][0]

    def add_income(self, card_number):
        amount = int(input('Enter income:\n'))
        self.change_balance(card_number, amount)
        print('Income was added!')

    def transfer(self, card_number):
        target = input('Enter card number:\n')
        if not self.luhn_card_check(target):
            print('Probably you made a mistake in the card number. Please try again!')
        elif target == card_number:
            print('You can\'t transfer money to the same account!\n')
        elif self.cur.execute(f'SELECT id FROM card WHERE number = {target};').fetchall():
            amount = int(input('Enter how much money you want to transfer:\n'))
            if self.cur.execute(f'SELECT id FROM card WHERE number = {card_number} AND balance >= {amount};').fetchall():
                self.change_balance(card_number, -amount)
                self.change_balance(target, amount)
                print('Success!')
            else:
                print('Not enough money!')
        else:
            print('Such a card does not exist.')

    def change_balance(self, card_number, amount):
        self.cur.execute(f'''UPDATE card
                SET balance = (SELECT balance FROM card WHERE number = {card_number}) + {amount}
                WHERE number = {card_number};''')
        self.conn.commit()

    def close_account(self, card_numbner):
        self.cur.execute(f'DELETE FROM card WHERE number = {card_numbner};')
        self.conn.commit()
        print('The account has been closed!')

    @staticmethod
    def luhn_card_create():
        card_number = [int(x) for x in list('4000000') + [str(randint(0, 9)) for _ in range(8)]]
        card_digits = [card_number[x] * 2 if x % 2 == 0 else card_number[x] for x in range(len(card_number))]
        card_digits = [x - 9 if x > 9 else x for x in card_digits]
        checksum = 10 - (sum(card_digits) % 10) if sum(card_digits) % 10 != 0 else 0
        card_number.append(checksum)
        return ''.join(list(map(str, card_number)))

    @staticmethod
    def luhn_card_check(card_number):
        card_digits = [int(x) for x in card_number]
        checksum = card_digits.pop(-1)
        card_digits = [card_digits[x] * 2 if x % 2 == 0 else card_digits[x] for x in range(len(card_digits))]
        card_digits = [x - 9 if x > 9 else x for x in card_digits]
        return (sum(card_digits) + checksum) % 10 == 0


if __name__ == '__main__':
    banking_system = BankingSystem()
    
#%%
