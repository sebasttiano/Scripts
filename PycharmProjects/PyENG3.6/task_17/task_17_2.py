# -*- coding: utf-8 -*-

'''
Задание 17.2

Создать функцию parse_sh_cdp_neighbors, которая обрабатывает
вывод команды show cdp neighbors.

Функция ожидает, как аргумент, вывод команды одной строкой (не имя файла).
Функция должна возвращать словарь, который описывает соединения между устройствами.

Например, если как аргумент был передан такой вывод:
R4>show cdp neighbors

Device ID    Local Intrfce   Holdtme     Capability       Platform    Port ID
R5           Fa 0/1          122           R S I           2811       Fa 0/1
R6           Fa 0/2          143           R S I           2811       Fa 0/0

Функция должна вернуть такой словарь:
{'R4': {'Fa0/1': {'R5': 'Fa0/1'},
        'Fa0/2': {'R6': 'Fa0/0'}}}

При этом интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.


Проверить работу функции на содержимом файла sh_cdp_n_sw1.txt
'''


import re

FILE = 'sh_cdp_n_sw1.txt'


def parse_file(file):
    content = ''
    with open(file, 'r') as f:
        for line in f:
            content += line.rstrip()
    return content


def parse_sh_cdp_neighbors(output):
    """:returns Example
    {'R4': {'Fa0/1': {'R5': 'Fa0/1'},
            'Fa0/2': {'R6': 'Fa0/0'}}}"""
    hostname = re.search('(\w+)>', output).group(1)
    #print(hostname)
    local_int = re.findall(r'.*(Eth|Fa /d/+).*', output)
    print(local_int)


a = parse_file(FILE)
parse_sh_cdp_neighbors(a)