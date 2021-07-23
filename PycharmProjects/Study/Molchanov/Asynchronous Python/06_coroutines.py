"""
Async in Python with coroutines and yield from
First example without "yield from"
"""

# g = subgen()
# # g.send(None)  --- инициализация генератора, иначе исключение возникает
# g.send('Ок')

# Декоратор инициализурющий генератор
def gen_init(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


def subgen():
    x = 'Ready to accept messages'
    message = yield x  # метод send() передает в yield значение. и присваивается в message, а x возвращается
    # получается двусторонняя передача значений в и из генератора
    print('Subgen received:', message)


class BlaBlaException(Exception):
    pass


@gen_init
def average():
    '''Генератор, который возвращает среднее арифметическое'''
    count = 0
    sum = 0
    average = None


    # Выход из этого бесконечного цикла, возможен например, если передать в генератор
    # контролирующее исключение с помомщью метода throw. average().throw(StopIteration)
    # при этом значение, которое должно было вернуться return сохраняется в аттрибут класса
    # StopIteration.value
    while True:
        try:
            x = yield average  # average отдается при вызове функций send() или next()
        except StopIteration:
            print('Done')
            break
        except BlaBlaException:
            print('..........')
            break
        else:
            count += 1
            sum += x
            average = round(sum/count, 2)

    # Генератор также возвращает "накопленное" значение"
    return average