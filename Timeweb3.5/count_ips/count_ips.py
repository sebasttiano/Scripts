#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" This version reads ip prefixes from file then count amount of ipv4"""

import sys
from netaddr import IPNetwork, AddrFormatError


def read_file(path_to_the_file):
    """
    @param path_to_the_file: url to the file
    @return list with IPNetwork objects
    """
    res_list = []
    with open(path_to_the_file, 'r') as f:
        try:
            for net in [IPNetwork(line).subnet(24) for line in f]:
                for net24 in net:
                    res_list.append(net24)
            return list(set(res_list))
        except AddrFormatError as e:
            print('Проверьте содержимое файла!\n', e)


print('Количество IP адресов  = {}'.format(len(read_file(sys.argv[1]))*256))
