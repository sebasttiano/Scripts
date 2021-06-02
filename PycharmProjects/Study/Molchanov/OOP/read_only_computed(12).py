""" Свойства только для чтения и вычисляемые свойства """

# Чтобы создать свойство только для чтения, нужно использовать декоратор property с одним getter, без setter

class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

p = Person('Sergey')
print(p.name)
# Тут возникнет исключение
#p.name = 'Ivan'
# AttributeError: can't set attribute
print(2*'\n', 'Пример вычисляемого свойства')

class Person2:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname

    @property
    def full_name(self):
        return f'{self._name} {self._surname}'


p2 = Person2('Ivan', 'Ivanov')
print(p2.full_name)

print(2*'\n', 'Пример вычисляемого свойства со сменой фамилии и использовании кэша, для вычислений'
              'свойств только при смене исходных данных')
class Person3:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname
        self._fullname = None # нужно для кэша

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value
        self._fullname = None # нужно для кэша

    @property
    def surname(self):
        return self._surname

    @surname.setter
    def surname(self, value):
        self._surname = value
        self._fullname = None  # нужно для кэша

    @property
    def full_name(self):
        if self._fullname is None:  # Проверка для кэшерования
            self._fullname = f'{self._name} {self._surname}'  # Данное вычисление бужет исполнено, если менялись _name или _surname
        return self._fullname


p3 = Person3('Ivan', 'Ivanov')
print (p3.full_name)
p3.surname = 'Petrov'
print (p3.full_name)
