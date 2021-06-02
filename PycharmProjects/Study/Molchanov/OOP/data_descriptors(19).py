"""Дескрипторы данных"""

from time import time
import ctypes
# Смотрим, что передается в качестве аргументов в дескриптор
class Epoch:
    def __get__(self, instance, owner_class):
        print(f'Self: ', self) # в первый и во второй разы тут экземпляр класса Epoch
        print(f'Instance: ', instance) # в первый раз тут экземпляр класса MyTime, во второй раз None
        print(f'Owner class: ', owner_class) # в первый и во второй разы тут сам класс MyTime
        return int(time())

class MyTime:
    epoch = Epoch()

m = MyTime()

print('Первый вызов из экземпляра класса MyTime')
print(m.epoch)
print(2*'\n', 'Второй вызов из самого класса MyTime')
print(MyTime.epoch)

# Вот такое поведение как выше, позволяет возвращать разные значения в зависимости откуда был вызов свойства. На этом
# принципе работает property(): при вызове из класса возвращает экезмпляр класса property, при вызове из экземпляра
# твоего класса возвращает значение свойства. Делаем также ниже

class Epoch2:
    def __get__(self, instance, owner_class):
        print(f'id of self: {id(self)}')
        if instance is None:
            return self
        return int(time())

    def __set__(self, instance, value):
        pass


class MyTime2:
    epoch = Epoch2()

m2 = MyTime2()
m3 = MyTime2()
m2.epoch
m3.epoch

# Так делать неправильно, нужно хранить значения в специальном словаре экземпляра дескриптора, c контролем на основе
# экземпляра основного класса (instance)

class IntDescriptor:
    def __init__(self):
        self._values = {}

    def __set__(self, instance, value):
        self._values[instance] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance)

class Vector:
    x = IntDescriptor()
    y = IntDescriptor()

v1 = Vector()
v2 = Vector()

print(v1.x, v2.x)
v1.x = 5
print(v1.x, v2.x)
v2.x = 10
print(v1.x, v2.x)
print('Распечаем сам словарь, где ключи доступа являются ссылками на'
      ' вызывающие дескриптор экземпляры класса Vector', '\n', Vector.x._values)


# Остается недостаток - на каждое генерацию свойства создаются избыточные ссылки, которые могут привести к утечке
# памяти. Чтобы этого избежать нуэно использовать слабые ссылки (weakrefs). В следующих занятиях.
