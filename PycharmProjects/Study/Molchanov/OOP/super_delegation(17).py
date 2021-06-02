"""super() и делегирование родителям"""

# Иногда после переопределения метода, нужно вызвать родительский метод (оригинальный)
class Person:
    def __init__(self, name):
        self.name = name


class Student(Person):
    def __init__(self, name, surname):
        # Передаем управление родительскому классу и вызываем его метод __init__() и ВАЖНО он связан с экземпляром
        # класса от куда он был  вызван. super() ищет методы по всем вышестоящим классам
        super().__init__(name)
        self.surname = surname

s = Student('Ivan', 'Ivanov')
print(s.__dict__)


class Person2:
    def hello(self):
        print(f'Bound with {self}')


class Student2(Person2):
    def hello(self):
        print('Student obj.hello() is called')
        super().hello()

s2 = Student2()
s2.hello()
print(hex(id(s2)))

