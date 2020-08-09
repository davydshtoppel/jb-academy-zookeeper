# Write your code here
import random
import sqlite3


class AccountGenerator:
    iin: str = '400000'

    @staticmethod
    def random_str(digits: int):
        result = ''
        for __ in range(digits):
            result += str(random.randint(0, 9))
        return result

    @staticmethod
    def luhn_hash(digits: str):
        int_list = []
        for it in digits:
            int_list.append(int(it))
        # Multiply odd digits by 2
        counter = 0
        while counter < len(digits):
            multiplied_odd_digit = int_list[counter] * 2
            # subtract 9 to numbers over 9
            if multiplied_odd_digit > 9:
                multiplied_odd_digit -= 9
            int_list[counter] = multiplied_odd_digit
            counter += 2
        # add all numbers
        digits_sum = 0
        for it in int_list:
            digits_sum += it
        # sum should be divisible by 10 without reminder
        remainder = digits_sum % 10
        return 0 if remainder == 0 else 10 - remainder

    @staticmethod
    def generate_number():
        customer_account = AccountGenerator.random_str(9)
        checksum = AccountGenerator.luhn_hash(AccountGenerator.iin + customer_account)
        return AccountGenerator.iin + customer_account + str(checksum)

    @staticmethod
    def check_number(number: str):
        existing_hash = number[-1]
        real_hash = AccountGenerator.luhn_hash(number[:15])
        return True if existing_hash == str(real_hash) else False


class Card:
    def __init__(self, number: str, pin: str):
        self.number = number
        self.pin = pin
        self.balance = 0


class CardRepository:

    def __init__(self):
        self.conn = sqlite3.connect('card.s3db')

    def __del__(self):
        self.conn.close()

    def init(self):
        cur = self.conn.cursor()
        cur.execute(r"""
        CREATE TABLE IF NOT EXISTS card (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            number TEXT,
            pin TEXT,
            balance INTEGER DEFAULT 0
        );
        """)
        self.conn.commit()

    def append(self, item: Card):
        cur = self.conn.cursor()
        cur.execute(f"INSERT INTO card(number, pin) VALUES ('{item.number}', '{item.pin}');")
        self.conn.commit()

    def find(self, number: str, pin: str = None):
        cur = self.conn.cursor()
        if pin is None:
            cur.execute(f"SELECT balance, pin FROM card WHERE number = '{number}'")
        else:
            cur.execute(f"SELECT balance, pin FROM card WHERE number = '{number}' AND pin = '{pin}'")
        row = cur.fetchone()
        self.conn.commit()
        if row is None:
            return None
        else:
            result = Card(number, row[1])
            result.balance = row[0]
            return result

    def update(self, item: Card):
        cur = self.conn.cursor()
        cur.execute(f"UPDATE card SET balance={item.balance} WHERE number = '{item.number}';")
        self.conn.commit()

    def delete(self, item: Card):
        cur = self.conn.cursor()
        cur.execute(f"DELETE FROM card WHERE number = '{item.number}';")
        self.conn.commit()


MAIN_MENU = 1
ACCOUNT_MENU = 2
card_repository = CardRepository()
card_repository.init()

state = MAIN_MENU
card = None
while True:
    if state == MAIN_MENU:
        print('1. Create an account')
        print('2. Log into account')
    elif state == ACCOUNT_MENU:
        print('1. Balance')
        print('2. Add income')
        print('3. Do transfer')
        print('4. Close account')
        print('5. Log out')
    print('0. Exit')

    income = int(input('>'))
    print()

    if income == 0:
        print('Bye!')
        break
    elif income == 1 and state == MAIN_MENU:
        new_card = Card(AccountGenerator.generate_number(), AccountGenerator.random_str(4))
        card_repository.append(new_card)
        print('Your card has been created')
        print('Your card number:')
        print(new_card.number)
        print('Your card PIN:')
        print(new_card.pin)
    elif income == 1 and state == ACCOUNT_MENU:
        print(f'Balance: {card.balance}')
    elif income == 2 and state == MAIN_MENU:
        print('Enter your card number:')
        card_number = input('>')
        print('Enter your PIN:')
        card_pin = input('>')
        existing_card = card_repository.find(card_number, card_pin)
        if existing_card is None:
            print('\nWrong card number or PIN!')
        else:
            state = ACCOUNT_MENU
            card = existing_card
            print('\nYou have successfully logged in!')
    elif income == 2 and state == ACCOUNT_MENU:
        print('Enter income:')
        card.balance += int(input('>'))
        card_repository.update(card)
    elif income == 3 and state == ACCOUNT_MENU:
        print('Transfer')
        print('Enter card number:')
        to_card_number = input('>')
        if not AccountGenerator.check_number(to_card_number):
            print('Probably you made mistake in card number. Please try again!')
        else:
            existing_card = card_repository.find(to_card_number)
            if existing_card is None:
                print('Such a card does not exist.')
            else:
                print('Enter how much money you want to transfer:')
                to_move = int(input('>'))
                if card.balance < to_move:
                    print('Not enough money!')
                else:
                    card.balance -= to_move
                    existing_card.balance += to_move
                    card_repository.update(card)
                    card_repository.update(existing_card)
                    print('Success!')
    elif income == 4 and state == ACCOUNT_MENU:
        card_repository.delete(card)
        card = None
        state = MAIN_MENU
        print('The account has been closed!')
    elif income == 5 and state == ACCOUNT_MENU:
        state = MAIN_MENU
        card = None
        print('You have successfully logged out!')
    else:
        continue

    print()
