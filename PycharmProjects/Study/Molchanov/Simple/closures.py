# Closures. Замыкания

def one():
    x = ['one', 'two']
    y = 'sadsadsd'
    def inner():
        print(x)
        print(y)
        print(id(x))
    return inner

o = one()

# переменная ссылается на внутреннюю функцию inner
print(o)

o()
# и после вызова становятся доступны переменные x, y, которые были в другом namespace, это и есть замыкания
print(o.__closure__)
print(o.__closure__[0].cell_contents, o.__closure__[1].cell_contents)
a = o.__closure__[0].cell_contents
print(id(a))

# Можно изменить список и он изменится в функции o (inner)

a.append('three')
o()
