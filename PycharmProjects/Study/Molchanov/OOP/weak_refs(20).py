"""Слабые ссылки weakref и проблема хранения данных в экземпляре дескриптора"""
# weakref (слабые ссылки)  - это такие же ссылки, только они не учитываются сборщиком мусора. Они делаются с помощью
# модуля weakref

import weakref
from weakref import WeakKeyDictionary
class Person:
    pass

p = Person()
w = weakref.ref(p)
print(w) # Видим, что это ссылка смотрит на объект Person

del p
print(w) # Теперь объекта нет (dead). Но объект ссылки еще в памяти

p2 = Person()
w2 = weakref.ref(p2)
print(w2()) # При вызове объекта слабой ссылки возвращается обхект на который ведет ссылка


del p2
print(w2()) # Возвращает None, т.к. объект удален

p3 = Person()

d = weakref.WeakKeyDictionary() # Специальный словарь для слабых ссылок
d[p3] = 10
print(d[p3], '\n', dir(d))
print(d.keyrefs()) # Возвращает список со всеми слабыми ссылками
del p3
print(d.keyrefs()) # Пустой словарь
# Пример из прошлого видео с применением слабых ссылок

print(2*'\n', 'Пример с классом Vector')
class IntDescriptor:
    def __init__(self):
        self._values = WeakKeyDictionary()

    def __set__(self, instance, value):
        self._values[instance] = value

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance)

class Vector:
    x = IntDescriptor()
    y = IntDescriptor()

v = Vector()
print(hex(id(v)))
v.x = 10
print(Vector.x._values.keyrefs())

del v
print(Vector.x._values.keyrefs())