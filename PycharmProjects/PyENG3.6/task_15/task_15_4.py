# -*- coding: utf-8 -*-

'''
Задание 15.4

Создать функцию parse_sh_ip_int_br, которая ожидает как аргумент
имя файла, в котором находится вывод команды show

Функция должна обрабатывать вывод команды show ip int br и возвращать такие поля:
* Interface
* IP-Address
* Status
* Protocol

Информация должна возвращаться в виде списка кортежей:
[('FastEthernet0/0', '10.0.1.1', 'up', 'up'),
 ('FastEthernet0/1', '10.0.2.1', 'up', 'up'),
 ('FastEthernet0/2', 'unassigned', 'up', 'up')]

Для получения такого результата, используйте регулярные выражения.

Проверить работу функции на примере файла sh_ip_int_br_2.txt.

'''

import re
from sys import argv

filename = argv[1]
result = []


def parse_sh_ip_int_br(source):
    with open(source, 'r') as file:
        for line in file:
            regex = re.compile('(?P<int>^\S+) +'
                               '(?P<ip>\S+).+'
                               '(?P<stat>up|administratively down) +'
                               '(?P<proto>\w+)')
            match = regex.findall(line)
            if match:
                result.append(match[0])
    return result

if __name__ == "__main__":
    parse_sh_ip_int_br(filename)
    print(result)