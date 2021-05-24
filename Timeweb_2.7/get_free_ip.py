#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import re
import argparse
import requests
import json
import logging
import logging.handlers
import ipaddress
from twtools import dbw

__version__ = '0.0.4'

LOG_HOST = "syslog"
LOG_PORT = 1114
NOC_PORTAL_API_URL = "http://nocportal:7508/api/v1.0/NOC"
USER = "noc"
PASS = "oopaOeCIdeKotAFaaY"
GET_FREE_IP_METHOD = "GetFreeIp"
CONVERT_METHOD = "Ipv4toIpv6"
RUN_BY = "%s@%s" % (os.getenv('USER'), os.uname()[1])
HELP = '''
        Скрипт возвращает свободный ip адрес в зависимости от переданных
    параметров. Для получения ip адреса необходимо передать параметр target
    (ключ -t) и location (ключ -d) скрипту, либо, вместо этих параметров,
    передать ключ -s с названием сервера (в этом случае указанные параметры
    берутся из данных сервера). По-умолчанию (если не переданы ключи -4 или -6)
    скрипт возвращает IPv4 адрес.
        Ключ -6 позволяет получить IPv6 адрес для определенного вида сервера.
    Ключи -4 и -6 могут использоваться одновременно, скрипт вернет два адреса,
    переконвертировав IPv4 в IPv6.
        Ключ -c используется для конвертирования ipv4 адреса в ipv6.
        Маска подсети для выдаваемых адрсеов IPv6 = /96
        Маска подсети для выдаваемых внешних адресов IPv4 = /24
        Маска подсети для выдаваемых локальных адресов IPv4 = /24

    Допустимые значения target:

    [Обязательльно задать location]
        1) colocation          - выделенные сервера с нашей админкой
        2) noadm               - выделенные сервера без нашей админки
        3) hosting             - хостинговые сервера
        4) hosting-personal    - выделенный ip адрес для клиента виртуального
                                 хостинга (тоже самое что и -t hosting -p)
        5) service             - адреса для служебных серверов
    [location отсутсвует, либо всегда указывать 1 (опция -d 1)]
        6) vps                 - внешние клиентские адреса для VDS/VPS сервера
        7) ipmi                - адреса для внешнего доступа по IPMI
        8) ipmi-local          - адреса для локального доступа по IPMI (сервера
                                 с нашим администрированием)
        9) free                - нераспределенные адреса (могут использоваться
                                 для тестов)
       10) local               - локальные адреса


    Допустимые значения location:

	Для получения БЕЛОГО ip адреса:
          4 - датацентр Селектел Цветочная 1
          9 - датацентр Селектел Цветочная 2
	Для получения СЕРЕГО ip адреса
          1 - датацентр Селектел Цветочная 1
          2 - датацентр Селектел Цветочная 2
        location 1 так же используется для выдачи адресов, не
          привязанных к дата-центру (IPMI и CDN)

    Примеры использования:

        1) Получение БЕЛОГО адреса для выделенного сервера с нашим админ:
            get_free_ip.py -t colocation -d 4       # Цветочная 1
            get_free_ip.py -t colocation -d 9       # Цветочная 2
        2) Получение БЕЛОГО адреса для выделенного сервера без админ:
            get_free_ip.py -t noadm -d 4            # Цветочная 1
            get_free_ip.py -t noadm -d 9            # Цветочная 2
        3) Получение БЕЛОГО клиентского адреса для VDS/VPS сервера:
            get_free_ip.py -t vps -d 4              # Цветочная 1
            get_free_ip.py -t vps -d 9              # Цветочная 2
        4) Получение СЕРОГО адреса для локальной сети:
            get_free_ip.py -t local -d 1            # Цветочная 1
            get_free_ip.py -t local -d 2            # Цветочная 2
        5) Получение адреса IPv4 и IPv6 для выделенного сервера с нашим
        админ:
            get_free_ip.py -t colocation -d 4 -6 -4   # Цветочная 1
            get_free_ip.py -t colocation -d 9 -6 -4   # Цветочная 2
        6) Конвертировать ipv4 адрес 92.53.116.1 в ipv6:
            get_free_ip.py -c 92.53.116.1
        7) Получить клиентский IPv6 адрес для VDS/VPS сервера:
            get_free_ip.py -t vps -d 4 -6           # Цветочная 1
            get_free_ip.py -t vps -d 9 -6           # Цветочная 2
        8) Получить DDoS guard защищенный ip адрес:
            get_free_ip.py -t hosting-personal -d 4 -p   # Цветочная 1
            get_free_ip.py -t hosting-personal -d 9 -p   # Цветочная 2
       9) Получить основной ip адрес для сервера BITRIX116:
            get_free_ip.py -s bitrix116
       10) Получить адрес хостингового сервера bitrix116 с выводом в формате
        JSON:
            get_free_ip.py -s bitrix116 -j'''

logger = logging.getLogger("get_free_ip")

def _parse_config():
    formatter_class = lambda prog: argparse.RawTextHelpFormatter(prog,
                                                                 indent_increment=8, max_help_position=40)
    parser = argparse.ArgumentParser(usage='''\n\tget_free_ip.py <options>''',
                                     epilog=HELP,
                                     formatter_class=formatter_class, add_help=False)
    # Conflicting params
    conflicting_params = parser.add_mutually_exclusive_group()
    conflicting_params.add_argument('-t', '--target', type=str,
                                    help='- Назначение ip адреса;')
    conflicting_params.add_argument('-c', '--convert', type=str,
                                    help='- IPv4 адрес, который необходимо\n'
                                    ' конвертировать в IPv6;')
    conflicting_params.add_argument('-s', '--server', type=str,
                                    help='- Выдать адрес по типу и размещению\n  сервера.'
                                    'Не чувствителен к регистру;')
    conflicting_params.add_argument('-n', '--networks', type=str, help='- ТОЛЬКО для'
                                    ' сетевых инженеров;')
    # Other params
    parser.add_argument('-a', '--all', action='store_true',
                        help='- Вывести все свободные ip адреса'
                        ' этой\n  категории;')
    parser.add_argument('-d', '--location', type=str,
                        help='- Датацентр;')
    parser.add_argument('-6', '--six-version', action='store_true',
                        help='- Сгенерировать IPv6 адрес;')
    parser.add_argument('-4', '--four-version', action='store_true',
                        help='- Сгенерировать IPv4 адрес.\n'
                        '  Используется по-умолчанию;')
    parser.add_argument('-j', '--json', action='store_true',
                        help='- результат в формате JSON;')
    parser.add_argument('--not-block', action='store_true',
                        help='- Не блокировать выданный ip\n  на 5 минут;')
    parser.add_argument('-p', '--protect', action='store_true',
                        help='- Защищенный(ddos_guard) ip адрес,\n '
                        ' выбирается для каждой услиги и расположения\n  из отдельных подсетей')
    parser.add_argument('-h', '--help', action='help',
                        default=argparse.SUPPRESS,
                        help='- Вывести на экран документацию;')
    parser._optionals.title = 'Параметры'
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        sys.exit(0)

    try:
        args = parser.parse_args()
    except:
        sys.exit(1)

    #  CONVERT IP
    # ~~~~~~~~~~~~
    # Convert ipv4 to ipv6
    if args.convert:
        try:
            return CONVERT_METHOD, {"ip": args.convert}, args.json
        except:
            parser.error("Cannot convert the given ip address")
            sys.exit(1)

    # default config
    config = {"runby": RUN_BY}

    #  BASE PARAMS
    # ~~~~~~~~~~~~~
    # ipv4 and ipv6
    if args.six_version:
        config["ipv6"] = True
    if args.four_version:
        config["ipv4"] = True
    if not args.six_version and not args.four_version:
        config["ipv4"] = True
    # Block ip in database or not
    if args.not_block:
        config["freeze"] = False
    # Show all ip addresses (return python list)
    if args.all:
        config['ip-list'] = True
    if args.protect:
        config['ddos_protection'] = "Y"

    #  SEARCH IN NEWROKS
    # ~~~~~~~~~~~~~~~~~~~
    # if set network
    if args.networks:
        if args.location:
            parser.error("argument -n/--networks: not allowed"
                         " with argument -d/--location")
        for n in args.networks.split(","):
            config["subnets"] = []
            try:
                ipaddress.ip_network(n)
            except:
                parser.error("%s is not correct network\n" % n)
                sys.exit(1)
            config["subnets"].append(n)
        return GET_FREE_IP_METHOD, config, args.json

    #  SEARCH BY SERVER NAME
    # ~~~~~~~~~~~~~~~~~~~
    if args.server:
        if args.location:
            parser.error("argument -s/--server: not allowed"
                         " with argument -d/--location")
        # Get target and location by server name
        config["target"], config[
            "location"] = _get_server_target_location(str(args.server))
        # Get personal ip
        #if args.protect:
            # костыль для инженерского скрипта /usr/local/sbin/install_ssl.py
        #    if config["target"] != 'colocation':
        #        config["target"] += "-personal"
        return GET_FREE_IP_METHOD, config, args.json

    #  SEARCH IN TARGET AND LOCATION
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    if args.target:
        if args.location:
            config["location"] = str(args.location)
        else:
            parser.error(
                "param -d/--location must be set with param -t/--target")
        # Old type call script get_free_ip from panel
        if args.target == 'virtual':
            config["target"] = "hosting"
            config["location"] = '4'
        # default location for ipmi,cdn = 1
        elif args.target in ["ipmi", "cdn"]:
            config["target"] = args.target
            config["location"] = '1'
        else:
            config["target"] = args.target
        # Get personal ip
        #if args.personal:
        #    config["target"] += "-personal"
        return GET_FREE_IP_METHOD, config, args.json

    parser.error("params (-t and -d) or -s or -n must be set")

def _get_server_target_location(server_name):
    dbc = dbw.DBClient('get_free_ip')
    target = None
    location = None
    q = '''
            SELECT
                location,
                purpose,
                virtual,
                xenpool
            FROM
                billing.servers
            WHERE
                LOWER(`name`)=LOWER('%s')
            LIMIT 1''' % server_name
    serv = dbc.load_object(q)
    if serv:
        # For VDS/VPS servers get location xenpool
        if serv['purpose'] == 'noadm' and serv['virtual'] == 'Y':
            target = 'vps'
            # If server is VDS
            if serv['xenpool'] != "":
                q = '''
                        SELECT location
                        FROM billing.servers
                        WHERE name='%s' LIMIT 1
                        ''' % serv['xenpool']
                location = dbc.load_object(q)['location']
            # If server is old VPS
            else:
                location = serv['location']
        else:
            target = serv['purpose']
            location = serv['location']
    else:
        print(("No found server %s in database" % server_name))
        sys.exit(1)
    return target, location

def _prepare_result(result, method, json_format):
    if json_format:
        return json.dumps(result["data"], indent=4)
    res_string = ""
    if method == GET_FREE_IP_METHOD:
        for version in [4, 6]:
            if 'ipv%s' % version in result['data']:
                for ip in result['data']['ipv%s' % version]:
                    if res_string:
                        res_string += "\n"
                    res_string += ip['ip']
    elif method == CONVERT_METHOD:
        res_string = result['data']['ip']
    return res_string

if __name__ == '__main__':
    # To make sure you're seeing all debug output:
    hdlr = logging.handlers.SysLogHandler(
        address=(LOG_HOST, LOG_PORT),
        facility=logging.handlers.SysLogHandler.LOG_LOCAL3)
    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)s - %(process)d/%(threadName)s %(levelname)-8s : %(message)s")
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.DEBUG)

    method, data, json_format = _parse_config()
    # Request API
    req = requests.Session()
    kwargs = {'data': json.dumps(data),
              'headers': {'content-type': 'application/json'},
              'auth': (USER, PASS)}
    url = '{0}/{1}'.format(NOC_PORTAL_API_URL, method)
    try:
        _response = req.request("GET", url, **kwargs)
        try:
            result = _response.json()
        except Exception as e:
            raise Exception("%s: %s" %
                            (str(e), _response.text.replace('\n', '')))
        if _response.status_code == 200:
            if 'data' not in result:
                print("Empty data")
                sys.exit(1)
            print(_prepare_result(result, method, json_format))
        else:
            if result['msg'] == "Empty list of subnets":
                print("No found ip for this target and datacenter")
            else:
                print("Error: %s" % result['msg'])
            logger.critical(result['msg'])
    except Exception as e:
        logger.critical(e)
