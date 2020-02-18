#!app/bin/python
# -*- coding: utf-8 -*-

"""
Portal module that manages network devices and ip addresses.

This exports:
    - NOC.ARPEntry() - manage ARP entry on routers (today support only clear)
    - NOC.FindMAC() - search MAC address in NOCProject database
    - NOC.ServerPortControl() - up/down switch port for dedicated server
    - NOC.GetFreeIp() - get free ip by purpose
    - NOC.GetIpPurpose() - get purpose by ip
    - NOC.Ipv4toIpv6() - convert ipv4 to ipv6

Last edited by:  v.ponomarjov@timeweb.ru
          Date:  16.11.2016
        Author:  Vadim Ponomarev
"""

__all__ = ["ServerPortControl","ARPEntry","FindMAC","GetFreeIp","GetIpPurpose", "Ipv4toIpv6"]
__version__ = '0.0.1'
__author__ = 'Vadim Ponomarev'

import os
import sys
from flask import abort
import logging
from ConfigParser import RawConfigParser

# append inlude from <root_path>/include
sys.path.append('./include')
# import base portal function
import portal
# For PostgreSQL
import psycopg2
import psycopg2.extras
import pymongo
# For check ip
from ncclient import manager
# For GetFreeIp class
sys.path.append('/usr/local/lib/noc')
import iptools


# For NCClient: sudo apt-get install build-essential libssl-dev libffi-dev
# python-dev 
# For MySQLdb: sudo apt-get install libmysqlclient-dev
__dependencies__ = ["psycopg2", "ncclient", "pymongo", "mysql-python", "netaddr"]

logger = logging.getLogger("portal-wsgi")

# Global
CONFIG_FILE = "/etc/noc-script/portal-noc-module.conf"


def _clear_arp(ip):
    if not iptools.is_ip(ip=ip):
        raise Exception("string '%s' is not valid ip address" % ip)
    cnf = portal.load_config(CONFIG_FILE)['Network']
    routers = cnf['routers'].replace(" ", "").split(",")
    for r in routers:
        try:
            with manager.connect(host=r,
                                 port=22,
                                 username=cnf['user'],
                                 password=cnf['password'],
                                 timeout=10,
                                 device_params={'name': 'junos'},
                                 hostkey_verify=False) as conn:
                result = conn.command(command='clear arp hostname %s' % ip,
                                      format='text')
                try:
                    logger.info(result.xpath('output')[0].text.strip())
                except IndexError:  # error: no entry for 8.8.8.8
                    logger.info("error: no entry for %s" % ip)
        except Exception, e:
            logger.error("Router {} connection failed! Error: {}".format(r, e),
                         exc_info=False)
            raise


def _find_mac(mac):
    """Find MAC address in NOCProject database.

    Function load config from CONFIG_FILE, connect to PostgreSQL, MongoDB and 
    search mac address.

    Args:
        mac: MAC address
    """
    mac = iptools.mac_to_unix_format(mac)
    mac = mac.upper()
    cnf_mongo = portal.load_config(CONFIG_FILE)['MongoDB']
    cnf_psql = portal.load_config(CONFIG_FILE)['PostgreSQL']
    cnf_psql['dbname'] = 'noc'
    connection = pymongo.MongoClient(cnf_mongo['host'], int(cnf_mongo['port']))
    db = connection.noc
    for mac_entry in db.noc.macs.find({"mac": "%s" % mac},
                                      {"vlan": 1, "interface": 1, "last_changed": 1}):
        interfaces = db.noc.interfaces.find({"_id": mac_entry['interface']}, {
                                            "name": 1, "description": 1, "managed_object": 1})
        if interfaces is not None:
            intf = interfaces[0]
            try:
                conn = psycopg2.connect(**cnf_psql)
            except:
                return {'interface': intf['name'],
                        'vlan': mac_entry['vlan'],
                        'interface-description': intf['description'],
                        'last-changed': mac_entry['last_changed']}
            cur = conn.cursor()
            q = '''SELECT id, name,address
                FROM sa_managedobject WHERE id='%s';
                ''' % intf['managed_object']
            cur.execute(q)
            rows = cur.fetchall()
            if len(rows) == 1:
                return {'switch': rows[0][1],
                        'switch-ip': rows[0][2],
                        'interface': intf['name'],
                        'vlan': mac_entry['vlan'],
                        'interface-description': intf['description'],
                        'last-changed': mac_entry['last_changed']}
        else:
            return {'vlan': mac_entry['vlan'],
                    'last-changed': mac_entry['last_changed']}
    return "MAC not found"


def _insert_task_to_netcron_db(server_id, task):
    """Add task to netcron PostgreSQL database in blocks table.

    Args:
        server_id: server id from database billing.servers
        task: 0 (disable) or 1 (enable)
    """
    # Load configuration from CONFIG_FILE_PORT_CONTROL
    cnf = portal.load_config(CONFIG_FILE)['PostgreSQL']
    cnf['dbname'] = 'cron'
    # Connect to PostgreSQL database "cron"
    conn = psycopg2.connect(**cnf)
    conn.autocommit = True
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    q = """
        INSERT INTO blocks (serv_id, operation) 
        VALUES (%s, %s);
        """ % (server_id, task)
    try:
        cur.execute(q)
        conn.close()
        logger.info("Add block server ID %s operation %s" %
                    (server_id, task))
    except Exception as e:
        conn.close()
        logger.error("PostgeSQL error: %e " % e)
        logger.debug("Query: %s" % q.strip())
        abort(500, "Fail set task in network cron.")


def ARPEntry(method, params):
    """Control ARP entry on routers. 

    Currently only supports removal (method DELETE).

    Args:
        method: request method type (may be: DELETE)
        params: python dict with key 'ip'
    """
    if not params or len(params) > 1:
        abort(400, "request only one param 'ip'")
    if method != "DELETE":
        abort(405, 'method %s not supported' % method)
    # if use URL arguments convert to dict
    if type(params) is list:
        params = {'ip': params[0]}
    if 'ip' not in params:
        abort(400, "request only one param 'ip'")
    _clear_arp(params['ip'])


def FindMAC(method, params):
    """Find MAC address in database NOCProject. 

    Args:
        method: request method type (may be: GET)
        params: python dict with key 'mac'
    """
    if not params or len(params) > 1:
        abort(400, "request only one param 'mac'")
    if method != "GET":
        abort(405, 'method %s not supported' % method)
    # if use URL arguments convert to dict
    if type(params) is list:
        params = {'mac': params[0]}
    if 'mac' not in params:
        abort(400, "request only one param 'mac'")
    return _find_mac(params['mac'])


def ServerPortControl(method, params):
    """Set or delete task for block/unblock server's port on rack switch/ 

    If method DELETE - port disable. IF method POST - port enable.

    Args:
        method: request method type (may be: POST (), DELETE)
        params: python dict/string with server_id
    """
    if not params or len(params) > 1:
        abort(400, "request only one param 'server_id'")
    # if use URL arguments convert to dict
    if type(params) is list:
        params = {'server_id': params[0]}
    if 'server_id' not in params:
        abort(400, "request only one param 'server_id'")
    if method == "DELETE":
        params['task'] = 0
    elif method == "POST":
        params['task'] = 1
    else:
        abort(400, 'method %s not supported' % method)
    logger.debug("call Proxy() method %s params: %s" % (method, params))
    _insert_task_to_netcron_db(**params)


def GetFreeIp(method, params):
    """Get free ip by purpose or in subnets.

    Args:
        method: request method type (may be: GET)
        params: python dict with keys:
            - (target and location) or subnets.
            - ipv4 (bool)
            - ipv6 (bool)
    """
    if type(params) is list:  # if params in URL
        abort(400, "function only supports parameters json format")
    if method != "GET":
        abort(405, 'method %s not supported' % method)
    run_by = None
    if 'runby' in params:
        run_by = params['runby']
    # init class GetFreeIp
    logging.getLogger("iptools").handlers = logger.handlers
    if 'subnets' in params:
        gfip = iptools.GetFreeIp(subnets=params['subnets'], run_by=run_by)
    elif 'target' in params:
        loc = params['location'] if 'location' in params else 1
        gfip = iptools.GetFreeIp(target=params['target'],
                                 location=loc,
                                 run_by=run_by)
    else:
        abort(400, "target and location or subnets parameters must be set")
    if 'ipv4' not in params and 'ipv6' not in params:
        abort(400, "ipv4 or ipv6 parameters must be set")
    # get free ip
    res = {}
    if 'ipv4' in params and params['ipv4']:
        all_ips = False # default return only first ip
        if 'ip-list' in params:
            all_ips = params['ip-list']
        freeze = True # default always freeze ip
        if 'freeze' in params:
            freeze = params['freeze']
        res['ipv4'] = gfip.ipv4(freeze_ip=freeze, all_ips=all_ips)
    if 'ipv6' in params and params['ipv6']:
        res['ipv6'] = gfip.ipv6()
    return res


def GetIpPurpose(method, params):
    """Get ip purpose.

    Args:
        method: request method type (may be: GET)
        params: python dict with keys ip and version (4 or 6).
    """
    if type(params) is list:  # if params in URL
        abort(400, "function only supports parameters json format")
    if method != "GET":
        abort(405, 'method %s not supported' % method)
    if 'ip' in params:
        if 'version' in params and params['version'] == 6:
            return iptools.get_ipv6_assignment(ip=params['ip'])
        # if version == 4 or version not set
        return iptools.get_ipv4_assignment(ip=params['ip'])
    else:
        abort(400, "'ip' parameter must be set")

def Ipv4toIpv6(method, params):
    """Convert ipv4 address to ipv6/

    Args:
        method: request method type (may be only: GET)
        params: python dict with key 'ip'
    """
    if not params or len(params) > 1:
        abort(400, "request only one param 'ip'")
    if method != "GET":
        abort(405, 'method %s not supported' % method)
    # if use URL arguments convert to dict
    if type(params) is list:
        params = {'ip': params[0]}
    if 'ip' not in params:
        abort(400, "request only one param 'ip'")
    return iptools.ipv4_to_ipv6(ipv4=params['ip'])
