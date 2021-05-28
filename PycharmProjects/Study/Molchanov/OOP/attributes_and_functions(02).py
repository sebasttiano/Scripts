# Объявляем класс
class Person:
    name = 'Sergei'

# Вызываем класс, создаем экземпляр класса
p = Person()
print(type(p))

# у класса есть такие свойства
print(dir(p))

# функция type возвращает ссылку на объект класса, как и p.__class__
new_person = type(p)()
print(type(new_person))

# Все аттрибуты и функции класса хранятся в переменной __dict__
print(Person.__dict__)
Person.age = 3233
print(Person.__dict__)

# Функции которые вызывают, добавляют и удаляют аттрибуты в классе
print(getattr(Person, 'name'))
setattr(Person, 'DoB', '1999')
print(Person.__dict__)
print(Person.__dict__['DoB'])
delattr(Person, 'DoB')
print(Person.__dict__)
print('\n'*3)


class Person2:
    name = 'Ivan'

    def hello():
        print('Hello')

# в __dict__ есть подпись, что объект hello - это функция класса
print(Person2.__dict__)