"""Дескрипторы. Non-data дескрипторы"""

# Дескриптор - это аттрибут какого-либо объекта и он сам являтся объектом определенного класса (у кого определены
# магические методы __get__()__, __set__(), __del__() или __set_name__() Используются для валидации данных.
# Ключевой момент :возможность использовать код дескриптора для одного класса многократно, где требуется одинаковое
# поведение

class StringD:
    def __init__(self, value=None):
        if value:
            self.set(value)

    def set(self, value):
        self._value = value

    def get(self):
        return self._value


class Person:
    def __init__(self, name, surname):
        self.name = StringD(name)
        self.surname = StringD(surname)


p = Person('Ivan', 'Ivanov')

print(p.name.get()) # такая конструкция не удобна, желательно, чтобы при обращении к свойству, возвращался не
                    # экземпляр класса, а вызывался автоматически метод, например get()

# Дескрипторы могут быть двух видов: non data - которые только отдают значение и data дескрипторы, которые могут
# изменять данные

# Non data

from time import time, sleep
from random import choice

class Epoch:
    def __get__(self, instance, owner_class):
        return int(time())

class MyTime:
    epoch = Epoch()

m = MyTime
print(m.epoch)
sleep(1)
print(m.epoch)
sleep(1)
print(m.epoch)

print(2*'\n', 'Пример игры')
# С помощью property создаем игры. есть избыточный код choice(), который повторяется
class Game:
    @property
    def rock_paper_scissors(self):
        return choice(['Rock', 'Paper', 'Scissors'])

    @property
    def flip(self):
        return choice(['Heads', 'Tails'])

    @property
    def dice(self):
        return choice(range(1, 7))

g = Game()
for i in range(3):
    print(g.dice)
    print(g.flip)
    print(g.rock_paper_scissors)

# Тот же пример с использование дескрипторов
print(2*'\n', 'Пример игры с использование non data дескрипторов')
class Choice:
    def __init__(self, *choice):
        self._choice = choice

    def __get__(self, obj, owner):
        return choice(self._choice)

class Game2:
    dice = Choice(1, 2, 3, 4, 5, 6)
    flip = Choice('Heads', 'Tails')
    rock_paper_scissors = Choice('Rock', 'Paper', 'Scissors')

g2 = Game2()
for i in range(3):
    print(g2.dice)
    print(g2.flip)
    print(g2.rock_paper_scissors)