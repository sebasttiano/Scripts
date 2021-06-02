"""Наследование, перегрузка методов и расширение функциональности"""
class Person:
    age = 0
    def hello(self):
        print('Hello')


class Student(Person):
    pass


s = Student()
print(dir(s)[-2:])
print(s.age)
print(s.__dict__)

# Все начальные свойства классов, например __class__, __doc__ etc, наследуются от базового класса object
print(2*'\n', dir(object))

class IntelCpu:
    cpu_socket = 1151
    name = 'Intel'

class I7(IntelCpu):
    pass

class I5(IntelCpu):
    pass

i5 = I5()
i7 = I7()

# Проверка есть ли у экземпляра класса i5 в цепочке наследования класс IntelCpu
print(isinstance(i5, IntelCpu))
print(type(i5))

class One:
    pass

class Two(One):
    pass

class Three(Two):
    pass

# функции issubclass. Проверка отношений классов, кто предки
print(2*'\n', issubclass(Three, One))

print(isinstance(i5, type(i7)))
print(issubclass(type(i5), type(i7)))

# Перегрузкой называется создание в подклассах свойств и методов с теми же именами, что и в родительском
print('\n', 'Пример перегрузки')
class Person:
    def hello(self):
        print('I am Person')


class Student(Person):
    def hello(self):
        print('I am Student')

s = Student()

s.hello()

# Расширение функциональности класса - это создание подкласса с дополнительными свойствами и методами
print('Пример расширения функционала')
class Person2:
    def hello(self):
        print('I am Person')


class Student2(Person):
    def goodbye(self):
        print('Goodbye')


s2 = Student2()
s2.goodbye()
