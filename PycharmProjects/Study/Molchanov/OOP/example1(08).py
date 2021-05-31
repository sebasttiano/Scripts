# -*- coding: utf-8 -*-
""" Объединение пройденного в примере. Классический пример с банковским счетом"""
from datetime import datetime
import pytz

WHITE = '\033[00m'
GREEN = '\033[0;92m'
RED = '\033[1;31m'

class Account:
    def __init__(self, name, balance):
        self.name = name
        self.balance = balance
        self.history = []

    # приватный статический метод
    @staticmethod
    def _get_current_time():
        return pytz.utc.localize(datetime.utcnow())

    def deposit(self, amount):
        self.balance += amount
        self.show_balance()
        self.history.append([amount, self._get_current_time()])

    def withdraw(self, amount):
        if self.balance > amount:
            self.balance -= amount
            print(f'You spent {amount} units')
            self.show_balance()
            self.history.append([-amount, self._get_current_time()])
        else:
            print('Not enough money')
            self.show_balance()

    def show_balance(self):
        print(f'Balance: {self.balance}')

    def show_history(self):
        for amount, date in self.history:
            if amount > 0:
                transaction = 'deposited'
                color = GREEN
            else:
                transaction = 'withdrawn'
                color = RED
            print(f'{color} {amount} {WHITE} {transaction} on date'
                  f' {date.astimezone()}')

a = Account('Sergey', 0)

a.deposit(100)
a.deposit(100)
a.deposit(550)
a.withdraw(100)
a.show_history()
