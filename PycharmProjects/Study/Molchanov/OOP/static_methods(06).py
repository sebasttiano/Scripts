""" Статические методы"""

# Если в методе нам не требуется доступ к свойствам экземпляра, то можно сделать общий метод для всех экземпляров,
# статический, с помощью декоратора @staticmethod, что экономит ресурсы компьютера.


class Person:
    def hello(self):
        print('Hello!')

    @staticmethod
    def goodbye():
        print('Goodbye!')

a = Person()
b = Person()

print(type(a.goodbye))
print(type(a.hello))
# print(id(a.hello))
# print(id(b.hello))

Person.goodbye()

