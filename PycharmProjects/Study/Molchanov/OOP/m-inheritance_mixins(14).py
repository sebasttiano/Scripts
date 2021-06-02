"""Множественное наследование, mro, миксины"""

# При наследовании от двух классов может возникуть проблема "ромбовидного" наследования, когда один и тот же метод
# есть в обоих родительских классах.

class Person:
    def hello(self):
        print('I am Person')

class Student(Person):
    def hello(self):
        print('I am Student')

class Prof(Person):
    def hello(self):
        print('I am Prof')

class Someone(Student, Prof):
    pass

s = Someone()
# Экземпляр s наследует методы согласно правилу mro - Method Resolution Order. Кто указан левее из родителей у того
# приоритет. В нашем случае Student
s.hello()
# В этом списке порядок поиска методов по классам
print(s.__class__.mro())

# В python есть миксины - минималистичные классы, которые используются только с другими классами для кастомизации и
# расширении функционала дочерного класса. Создание экземпляра миксин не предполагается.

class FoodMixin:
    food = None

    def get_food(self):
        if self.food is None:
            raise ValueError('Food should be set')
        print(f'I like {self.food}')


class Student2(FoodMixin, Person):
    food = 'Pizza'
    def hello(self):
        print('I am Student')

s2 = Student2()
s2.get_food()