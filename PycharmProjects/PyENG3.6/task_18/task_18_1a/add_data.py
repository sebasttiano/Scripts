# -*- coding: utf-8 -*-

'''
Задание 18.1

add_data.py
* с помощью этого скрипта, выполняется добавление данных в БД
* добавлять надо не только данные из вывода sh ip dhcp snooping binding, но и информацию о коммутаторах


В файле add_data.py должны быть две части:
* информация о коммутаторах добавляется в таблицу switches
 * данные о коммутаторах, находятся в файле switches.yml
* информация на основании вывода sh ip dhcp snooping binding добавляется в таблицу dhcp
 * вывод с трёх коммутаторов:
   * файлы sw1_dhcp_snooping.txt, sw2_dhcp_snooping.txt, sw3_dhcp_snooping.txt
 * так как таблица dhcp изменилась, и в ней теперь присутствует поле switch, его нужно также заполнять. Имя коммутатора определяется по имени файла с данными

Код должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.
'''


import glob
import sqlite3
import re
import yaml
from task_18.task_18_1.create_db import create_db

db_filename = 'dhcp_snooping.db'
dhcp_snoop_files = glob.glob('sw*_dhcp_snooping.txt')
regex = re.compile('(\S+) +(\S+) +\d+ +\S+ +(\d+) +(\S+)')
switches_list = 'switches.yml'


def parse_from_yml(yml_file):
    flist = []
    with open (yml_file) as f:
        templates = yaml.load(f)
    for i in templates['switches'].items():
        flist.append(i)
    return flist


def parse_outputs(list_with_files):
    result = []
    for i in list_with_files:
        hostname = i[:i.find('_')]
        with open(i) as data:
            for line in data:
                match = regex.search(line)
                if match:
                    ls = list(match.groups())
                    ls.append(hostname)
                    result.append(ls)
    return result


def create_connection(db_name):
    conn = sqlite3.connect(db_name)
    return conn


def write_to_db(connection, query, data_tuple):
    try:
        with connection:
            connection.executemany(query, data_tuple)
    except sqlite3.IntegrityError as e:
        print('Error occured: ', e)
        return False
    except sqlite3.OperationalError as e:
        print('Error occured: ', e)
        print('Recreating tables....')
        create_db(db_filename)
        write_to_db(connection, query, data_tuple)
    else:
        print('Inserted to the db successfully')
        return True


if __name__ == '__main__':
    print('Connecting to the db...', end='', flush=True)
    con = create_connection(db_filename)
    if con:
        print('Done!')
    query_insert_dhcp = 'INSERT INTO dhcp VALUES (?, ?, ?, ?, ?)'
    query_insert_switches = 'INSERT INTO switches VALUES (?, ?)'
    data_dhcp = parse_outputs(dhcp_snoop_files)
    print('Writing to the dhcp table...')
    write_to_db(con, query_insert_dhcp, data_dhcp)
    data_switches = parse_from_yml(switches_list)
    print('Writing to the switches table...')
    write_to_db(con, query_insert_switches, data_switches)
    con.close()
