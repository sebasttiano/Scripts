# -*- coding: utf-8 -*-

"""
Задание 18.1

create_db.py
* сюда должна быть вынесена функциональность по созданию БД:
 * должна выполняться проверка наличия файла БД
 * если файла нет, согласно описанию схемы БД в файле dhcp_snooping_schema.sql,
   должна быть создана БД (БД отличается от примера в разделе)

В БД теперь две таблицы (схема описана в файле dhcp_snooping_schema.sql):
 * switches - в ней находятся данные о коммутаторах
 * dhcp - эта таблица осталась такой же как в примере, за исключением поля switch
  * это поле ссылается на поле hostname в таблице switches

Код должен быть разбит на функции.
Какие именно функции и как разделить код, надо решить самостоятельно.
Часть кода может быть глобальной.
"""

import os
import sqlite3


db_filename = 'dhcp_snooping.db'
schema_filename = 'dhcp_snooping_schema.sql'


def create_db(filename):
    conn = sqlite3.connect(filename)
    print('Creating schema...')
    with open(schema_filename, 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    print('Done')


def check_availability(filename):
    '''Checks, if the db exists, else runs create_db func'''
    db_exists = os.path.exists(filename)
    if db_exists:
        print('Database exists, assume dhcp table does, too!!!')
        return True
    else:
        return False


def main():
    print('The main has been worked nice!!')

if __name__ == '__main__':
    if check_availability(db_filename):
        main()
    else:
        create_db(db_filename)
        main()





