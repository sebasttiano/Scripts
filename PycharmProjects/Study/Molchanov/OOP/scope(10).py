
# Пространстро имен в подавляющем большинстве случаев это словарь.
# Область видимости это путь, по которому Python ищет определении имени в пространстве имен. По сути перечисление
# словарей через запятую(LEGB)
# Local - локальная
# Enclosed - вложенная
# Global - глобальная
# Builtins - уровень модуля builtins
# но есть исключения, например при определении класса

name = 'Sergey'

class Person:
    # Это не вложенная область для метода, а локальная область для класса
    # метод не может читать напрямую отсюда.
    name = 'Dima'

    def print_name(self):
        # Это локальная область метода
        print(name)
        # Но можно прочитать через поиск Python, если будет объявлено так, но изменить нельзя, т.к. создастся локальное
        # свойство в экземпляре
        print(self.name)

p = Person()
print(p.__dict__)
p.print_name()
p.name = 'ssdasadsad'
print('Instance dict:', p.__dict__)
print('Person.name:', Person.name)

# Для того, чтобы изменять свойства класса можно создавать методы класса (привязку функции и объекта класса). С помощью
#декоратора @classmethod. Передается функции ссылка на сам класс, неявная переменная cls (вместо self). Если изменить
# свойства класса, то изменятся эти же свойства у всех экземпляров. Удобно для глобальных настроек каких-то. Метод класса
# можно вызывать из любого экземпляра класса

print(2*'\n', "Ниже пример метода класса" )


class Person2:
    name = 'Dima'

    @classmethod
    def change_name(cls, name):
        cls.name = name

p2 = Person2()
print(p2.__dict__)
p2.change_name('asadsad')
print('Instance dict:', p2.__dict__)
print('Person2.name:', Person2.name)

# Часто методы класса используются для описания альтернативных инициализаторов (__init__())

class Person3:
    def __init__(self, name):
        self.name = name

    # Первый вариант
    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            name = f.read().strip()
        return cls(name=name)

    # Второй вариант
    @classmethod
    def from_obj(cls, obj):
        if hasattr(obj, 'name'):
            name = getattr(obj, 'name')
            return cls(name=name)
        return cls

p3 = Person3('Sergey')
print(2*'\n', "Ниже пример нескольких инициализаторов")
print(p3.__dict__)

p3 = Person3.from_file('file_scope')
print(p3.__dict__)

# Пример из объекта

class Config:
    name = "Igor"

p3 = Person3.from_obj(Config)
print(p3.__dict__)