"""Полиморфизм, перегрузка операторов"""

# Полиморфизм - это разное поведение одного и того же метода для разных классов
# + это синтаксический сахар для магического метода __add__()
print('1'.__add__('2'))


class Person:
    age = 1
    def __add__(self, value):
        self.age += 1
        return self.age

p = Person()
print(p + 2000000)
print(p + 'adasda')

print(2*'\n', 'Пример с комнатами')
class Room:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.area = self.x * self.y
    # Сахаром является оператор +
    def __add__(self, room_obj):
        if isinstance(room_obj, Room):
            return self.area + room_obj.area
        raise TypeError('Wrong object')
    # Сахаром является оператор ==
    def __eq__(self, room_obj):
        if isinstance(room_obj, Room) and self.area == room_obj:
            return True
        return False

r1 = Room(3, 5)
r2 = Room(4, 7)
print(r1.area, r2.area)
print('Общая площадь обеих комнат', r1 + r2)

print('Равны ли площади комнтат?', r1 == r2)
