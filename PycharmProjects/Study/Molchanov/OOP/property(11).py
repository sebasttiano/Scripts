"""Свойства @property, геттеры и сеттеры (getter, setter)"""

# Свойство класса - это способ доступа к аттрибутам класса.
# Метод get (getter) - это метод для чтения приватного свойства. Метод set (setter) - метод для установления нового
# значения приватного свойства. Приватност в имени означается нижним подчеркиванием. (self._name, напр.)

class Person:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        print('From get_name()')
        return self._name

    def set_name(self, value):
        print('From set_name()')
        self._name = value

    name = property(fget=get_name, fset=set_name)


p = Person('Dima')
print(p.__dict__)
print(p.name)
p.name = 'Ivan'
print(p.__dict__)

# Сеттеры и геттеры нужны как буферные зоны, где можно делать валидацию значений и т.п. Так же мы не можем поломать
# интерфейс класса при изменении приватного свойства. Можно делать вычисляемые свойства.
# Хорошо работает для обратной совместимости


class Person2:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        print('From get_name()')
        return self._name

    def set_name(self, value):
        print('From set_name()')
        self._name = value
# Такая запись тоже возможна
    name = property()
    name = name.getter(get_name)
    name = name.setter(set_name)

print(2*'\n', 'Пример через декоратор', '\n')


class Person3:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    # имя должно быть одинаковым с первой функцией
    def name(self, value):
        self._name = value

p3 = Person('Dima')
print(p3.__dict__)
print(p3.name)
p3.name = 'Ivan'
print(p3.__dict__)