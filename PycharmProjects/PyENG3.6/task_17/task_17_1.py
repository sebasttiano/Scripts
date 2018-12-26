# -*- coding: utf-8 -*-

'''
Задание 17.1

В этом задании нужно:
* взять содержимое нескольких файлов с выводом команды sh version
* распарсить вывод команды с помощью регулярных выражений и получить информацию об устройстве
* записать полученную информацию в файл в CSV формате

Для выполнения задания нужно создать две функции.

Функция parse_sh_version:
* ожидает аргумент output в котором находится вывод команды sh version (не имя файла)
* обрабатывает вывод, с помощью регулярных выражений
* возвращает кортеж из трёх элементов:
 * ios - в формате "12.4(5)T"
 * image - в формате "flash:c2800-advipservicesk9-mz.124-5.T.bin"
 * uptime - в формате "5 days, 3 hours, 3 minutes"

Функция write_to_csv:
* ожидает два аргумента:
 * имя файла, в который будет записана информация в формате CSV
 * данные в виде списка списков, где:
    * первый список - заголовки столбцов,
    * остальные списки - содержимое
* функция записывает содержимое в файл, в формате CSV и ничего не возвращает

Остальное содержимое скрипта может быть в скрипте, а может быть в ещё одной функции.

Скрипт должен:
* обработать информацию из каждого файла с выводом sh version:
 * sh_version_r1.txt, sh_version_r2.txt, sh_version_r3.txt
* с помощью функции parse_sh_version, из каждого вывода должна быть получена информация ios, image, uptime
* из имени файла нужно получить имя хоста
* после этого вся информация должна быть записана в файл routers_inventory.csv

В файле routers_inventory.csv должны быть такие столбцы:
* hostname, ios, image, uptime

В скрипте, с помощью модуля glob, создан список файлов, имя которых начинается на sh_vers.
Вы можете раскомментировать строку print(sh_version_files), чтобы посмотреть содержимое списка.

Кроме того, создан список заголовков (headers), который должен быть записан в CSV.
'''

import glob
import re
import csv


HEADERS = ['hostname', 'ios', 'image', 'uptime']
TARGET_FILENAME = 'routers_inventory.csv'


def get_hostname(filename):
    """:returns str - hostname"""
    regex = '^sh_version_([\w\W]+)\.txt'
    match = re.search(regex, filename)
    return match.group(1)


def parse_file(file):
    content = ''
    with open(file, 'r') as f:
        for line in f:
            content += line.rstrip()
    return content


def parse_sh_version(output):
    """:returns tuple with data (ios, image, uptime)"""
    regex = '.*Version (\d+\.\d+\(\d+\)\w+)' \
            '.*uptime is ([\w\W]+minute\w?)' \
            '.*image file is "([\w\W]+?)"'
    match = re.search(regex, output)
    return match.groups()


def write_to_csv(filename, list):
    """Write the result of parsing to csv"""
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        for row in list:
            writer.writerow(row)


def main():
    list_to_write = []
    sh_version_files = glob.glob('sh_vers*')
    for i in sh_version_files:
        # load content from files
        text = parse_file(i)
        hostname = get_hostname(i)
        data_list = list(parse_sh_version(text))
        a = data_list.pop(2)
        data_list.insert(1, a)
        data_list.insert(0, hostname)
        list_to_write.append(data_list)
    list_to_write.insert(0, HEADERS)
    #write the data to csv
    write_to_csv(TARGET_FILENAME, list_to_write)


if __name__ == '__main__':
    main()