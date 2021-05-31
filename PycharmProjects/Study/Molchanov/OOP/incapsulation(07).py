'''Инкапсуляция, приватные атрибуты и публичный интерфейс'''

# Приватные (вне класса не предполагается использование)
# аттрибуты принято выделять с помощью одинарного нижнего подчеркивания _
class Person:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname
        self.public_name = f'{self._name} {self._surname}'


p = Person('Sergey', 'Voronov')
print(p.public_name)