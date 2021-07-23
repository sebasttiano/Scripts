"""
Async in Python with coroutines and yield from
Second example with "yield from and constructions of delegating generator and subgenerator"
"""

# Декоратор инициализурющий генератор
def gen_init(func):
    def inner(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return inner


class BlaBlaException(Exception):
    pass

#Подгенератор тот, что вызывается вышестоящим генератором
#@gen_init- yield from из делегатора сам инициализирует это генератор
def subgen():
    while True:
        try:
            message = yield
        except BlaBlaException:
            print('Bla-Bla-Bla')
        except StopIteration:
            break
        else:
            print('...........', message)
    return 'Returned from subgen()'

# Делегирующий генератор, этот тот, который вызывает другой генератор
@gen_init
def delegator(g):
    # while True:
    #     try:
    #         data = yield
    #         g.send(data)
    #     except BlaBlaException as e:
    #         g.throw(e)
    #     except StopIteration as stop:
    #         g.throw(stop)
    # Все вышенаписанное, а также обработку return можно заменить c помощью "yield from g"
    result = yield from g
    print(result)


# Подгенератор должен обязательно иметь мезанизм завершения, т.к .он блокирует делегирующий генератор.
# yield from в других языках называется await.
# по факту yield from просто возвращает итерируемый объект по одному значению, как бы проходясь по нему в цикле for
def simple_generator():
    yield from 'voron'