"""Метод дескриптора __set_name__ и хранение данных в экземпляре класса-владельца"""
# Этот метод вызывается один раз, когда python создает экхемпляр дескриптора (x = IntDescriptor()) и ему передается
# имя аттритута, для которого требуется вернуть или записать значение (x)

class ValidString:
    def __set_name__(self, owner_class, property_name):
        print(f'owner_class: {owner_class}')
        print(f'property_name: {property_name}')


class Person:
    name = ValidString()
# Вызов __set_name__ происходит автоматически на этапе компиляции кода


class ValidString2:
    def __set_name__(self, owner_class, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f'{self.property_name} must be a String, '
                             f'but {type(value).__name__} was passed')


class Person2:
    name = ValidString2()

p = Person2()
p.name = 'Ivan'
#p.name = 123 # Здесь возникнет исключение ValueError: name must be a String, but int was passed

# Теперь мы хотим созранить значения в экземпляра класса-владельца

class ValidString3:
    def __set_name__(self, owner_class, property_name):
        self.property_name = property_name

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError(f'{self.property_name} must be a String, '
                             f'but {type(value).__name__} was passed')
        key = '_' + self.property_name
        # setattr(instance, key, value) # Первый вариант сохранения
        instance.__dict__[key] = value # Второй вариант сохранения

    def __get__(self, instance, owner):
        if instance is None:
            return self
        key = '_' + self.property_name
        # return getattr(instance, key, None) # Первый вариант возвращения
        return instance.__dict__.get(key, None) # Второй варинт возвращения

# ! Обращение даже к локальному словарю __dict__ экземпляра происходит через дескриптор

class Person3:
    name = ValidString3()
    surname = ValidString3()

p3 = Person3()
p3.name = 'Ivan'
# p3.surname = 123 #Здесь возникнет исключение ValueError: name must be a String, but int was passed
print('Приватное значение было сохранено в экземпляре класса Person, через дескриптор', '\n', p3.__dict__)