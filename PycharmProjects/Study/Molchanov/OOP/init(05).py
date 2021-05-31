''' О инициализации экземпляров'''


class Person:
    def create(self):
        self.name = 'Sergei'

    def display(self):
        print(self.name)

p = Person()
# при создании экземпляра, у него нет никаких аттрибутов
print(p.__dict__)

p.create()
print(p.__dict__)

# Есть встроенная функция инициализации (вместо нашей create), которая вызывается автоматически при
# создании экземпляра __init__()


class Person2:
    def __init__(self, name):
        self.name = name

    def display(self):
        print(self.name)


p2 = Person2('Sergei')
print(p2.name)

# При создании экземпляра сначала вызывается функциия __new__(), которая создает экземпляр. А затем __init__(self),
# которая инициализирует его.