# -*- coding: utf-8 -*-

'''
Задание 9.3a

Переделать функцию parse_cfg из задания 9.3 таким образом, чтобы она возвращала словарь:
* ключ: имя интерфейса
* значение: кортеж с двумя строками:
  * IP-адрес
  * маска

Например (взяты произвольные адреса):
{'FastEthernet0/1':('10.0.1.1', '255.255.255.0'),
 'FastEthernet0/2':('10.0.2.1', '255.255.255.0')}

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла config_r1.txt.

Обратите внимание, что в данном случае, можно не проверять корректность IP-адреса,
диапазоны адресов и так далее, так как обрабатывается вывод команды, а не ввод пользователя.

'''

import re
from sys import argv

filename = argv[1]

def parse_cfg(filename):
    result = {}
    source = '/home/svoronov/pyneng-examples-exercises/exercises/09_regex/{}'.format(filename)
    with open(source, 'r') as file:
        cfg = file.read()
        regex = re.compile('interface (?P<inf>[LE]\S+)\n [^n].*?p address (?P<ip>\d+\.\d+\.\d+\.\d+) +(?P<mask>\d+\.\d+\.\d+\.\d+)', re.DOTALL)
        match = regex.findall(cfg)
        for i in match:
            result[i[0]] = tuple(i[1:])
        return result


parse_cfg(filename)