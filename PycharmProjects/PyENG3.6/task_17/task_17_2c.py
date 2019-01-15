# -*- coding: utf-8 -*-

'''
Задание 17.2c

С помощью функции draw_topology из файла draw_network_graph.py
сгенерировать топологию, которая соответствует описанию в файле topology.yaml

Обратите внимание на то, какой формат данных ожидает функция draw_topology.
Описание топологии из файла topology.yaml нужно преобразовать соответствующим образом,
чтобы использовать функцию draw_topology.

Для решения задания можно создать любые вспомогательные функции.

Не копировать код функции draw_topology.

В итоге, должно быть сгенерировано изображение топологии.
Результат должен выглядеть так же, как схема в файле task_10_2c_topology.svg

При этом:
* Интерфейсы могут быть записаны с пробелом Fa 0/0 или без Fa0/0.
* Расположение устройств на схеме может быть другим
* Соединения должны соответствовать схеме


> Для выполнения этого задания, должен быть установлен graphviz:
> apt-get install graphviz

> И модуль python для работы с graphviz:
> pip install graphviz

'''


import yaml
from task_17.draw_network_graph import draw_topology


def read_from_yaml(file):
    with open (file) as f:
        templates = yaml.load(f)
    return templates


def convert_to_the_format(templates):
    result_dict = {}
    for host in templates:
        for local_port in templates[host]:
            result_dict [(host, local_port)] = (list(templates[host][local_port].keys())[0],
                                                list(templates[host][local_port].values())[0])
    return result_dict


def delete_dublicates(dictionary):
    for keys in list(dictionary.keys()):
        for values in list(dictionary.values()):
            if keys == values:
                del(dictionary[keys])
    return dictionary


def main():
    data = read_from_yaml('topology.yaml')
    preform = delete_dublicates(convert_to_the_format(data))
    draw_topology(preform)


if __name__ == '__main__':
    main()