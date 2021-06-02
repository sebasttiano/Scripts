"""Хэшируемые объекты и равенство"""
# Иногда нужно чтобы наши объекты были ключами в словарях. Ключом может быть только неизменяемый объект, словарь
# ищет ключи на основе хэширования. Для хэширования нужно выбрать свойство, которое не может меняться - read only
# свойство. И еще нужно переопределить магические методы __hash__ и __eq__

class Person:
    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, person_obj):
        return isinstance(person_obj, Person) and self.name == person_obj.name

p1 = Person('Ivan')
p2 = Person('Ivan')

print(p1 == p2)

p3 = Person('Oleg')
print(p1 == p3)
print(hash(p1), '\n', hash(p2))

# Мы можем использовать эти экземпляры как ключи в словаре
d = {p1: 'Ivanov Ivan'}
print(d.get(p1))
