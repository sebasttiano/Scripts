# -*- coding: utf-8 -*-
""" Name mangling theme """
from datetime import datetime
import pytz

WHITE = '\033[00m'
GREEN = '\033[0;92m'
RED = '\033[1;31m'


class Account:
    def __init__(self, name, balance):
        self.name = name
        # Name mangling... Два нижних подчеркивания спереди
        self.__balance = balance
        self._history = []

    # приватный статический метод
    @staticmethod
    def _get_current_time():
        return pytz.utc.localize(datetime.utcnow())

    def deposit(self, amount):
        self.__balance += amount
        self.show_balance()
        self._history.append([amount, self._get_current_time()])

    def withdraw(self, amount):
        if self.__balance > amount:
            self.__balance -= amount
            print(f'You spent {amount} units')
            self.show_balance()
            self._history.append([-amount, self._get_current_time()])
        else:
            print('Not enough money')
            self.show_balance()

    def show_balance(self):
        print(f'Balance: {self.__balance}')

    def show_history(self):
        for amount, date in self._history:
            if amount > 0:
                transaction = 'deposited'
                color = GREEN
            else:
                transaction = 'withdrawn'
                color = RED
            print(f'{color} {amount} {WHITE} {transaction} on date'
                  f' {date.astimezone()}')

a = Account('Sergey', 0)

a.show_balance()
a.__balance = 100000
# Name mangling защищает критичные данные от перегрузки(одно имя используется более чем в одном контексте
# или имеет несколько значений) и переопределения свойств, чтобы случайно не изменить что-то важное.
# Происходит подмена аттрибута __balance на _Account__balance (название класса и одним подчеркиванием подставляется
# спереди. Name mangling работает не только в ООП
a.show_balance()

print(a.__dict__)
