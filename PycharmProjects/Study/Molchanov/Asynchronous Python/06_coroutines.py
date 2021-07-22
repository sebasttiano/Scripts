'''Async in Python with coroutines and yield from'''


def subgen():
    x = 'Ready to accept messages'
    message = yield x  # метод send() передает в yield значение. и присваивается в message
    print('Subgen received:', message)

# g = subgen()
# # g.send(None)
# g.send('Ок')