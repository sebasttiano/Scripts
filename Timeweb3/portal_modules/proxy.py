#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
 Script for set protos proxy settting
 Example:
     To enable proxying for ip 92.53.96.240 (hosting), the following must be done :
       get ddog ip for service puprose hosting 185.114.246.50
       ip add add dev eth1.2 185.114.246.50/24
       iptables -t nat -A PREROUTING -d 185.114.246.50/24 -i eth1.2 -j DNAT --to-destination 92.53.96.240
       iptables -t nat -A POSTROUTING -d 92.53.96.240/32 -o eth1.2 -j MASQUERADE
       iptables -t nat -A POSTROUTING -o eth1.2 -s 92.53.96.240/32 -j SNAT --to-source 85.114.246.50
       ip rule add from 92.53.96.240 lookup ddosg_vh

 Routing tables (/etc/iproute2/rt_tables)
    100 ddosg_vh vh
    101 ddosg_110 vdsdc1
    102 ddosg_210 vdsdc2

"""

import logging
import netifaces
import subprocess
from flask import abort
# AF_INET ipv4 protocol
from socket import AF_INET
from pyroute2 import IPRoute
from functools import wraps


# routing tables
 DDOSG_RT_VH = 100
DDOSG_RT_VDS_DC1 = 101
DDOSG_RT_VDS_DC2 = 102

# Vlan interfaces must exist and be UP
INTERFACE_HOSTING = "eth1.2"
INTERFACE_VDS_DC1 = "eth1.110"
INTERFACE_VDS_DC2 = "eth1.210"

# static configuration(netplan) ip addresess
# deny add or delete
STATIC_IP_ADDRESESS = ("92.53.116.110",
                       "185.114.246.2",
                       "185.200.243.103",
                       "185.200.242.114")

__all__ = ["ConfPorxyIP", "CheckProxySettings"]

# Gloabg portal logger
logger = logging.getLogger("portal-wsgi")


def check_interfaces_decorator(func):
    # Used for save function parameters like __name__ (used in check_params_decorator)
    @wraps(func)
    def decorated(*args, **kwargs):
        # list intefases List[str]
        interfaceslist = netifaces.interfaces()
        ipr = IPRoute()
        upinterfaces = ipr.link_lookup(operstate='UP')
        for interface in [INTERFACE_HOSTING, INTERFACE_VDS_DC1, INTERFACE_VDS_DC2]:
            # check what the interface exist
            if interface not in interfaceslist:
                logger.error("inteface {} not found".format(interface))
                abort(500, "inteface {} not found".format(interface))
            # ccheck what the in UP state
            if ipr.link_lookup(ifname=interface)[0] not in upinterfaces:
                logger.error("inteface {} not in UP state".format(interface))
                abort(500, "inteface {} not in UP state".format(interface))
        ipr.close()
        return func(*args, **kwargs)
    return decorated


def check_params_decorator(func):
    def decorated(*args, **kwargs):
        requiredparams = ("ddosgip", "clientip", "purpose", "location", "action")
        allowmethods = ("POST",)

        if func.__name__ == "CheckProxySettings":
            allowactions = ("check",)
        else:
            allowactions = ("add", "del")

        # in args (<method>,<dict data>)
        argmethod = args[0]
        argparams = args[1]

        if argmethod not in allowmethods:
            logger.error("Not allowed method '{}' for {} function".format(argmethod, func.__name__))
            abort(400, "Not allowed method '{}' for {} function".format(argmethod, func.__name__))

        for param in requiredparams:
            if param not in argparams:
                logger.error("Not found param '{}' in request data {}".format(param, argparams))
                abort(400, "Not found param '{}' in request data {}".format(param, argparams))

        if str(argparams["ddosgip"]).lower() in STATIC_IP_ADDRESESS:
            logger.error("Bad ddosgip '{}' static ips: '{}'".format(argparams["ddosgip"], STATIC_IP_ADDRESESS))
            abort(400, "Bad ddosgip '{}' static ips: '{}'".format(argparams["ddosgip"], STATIC_IP_ADDRESESS))

        if argparams["action"] not in allowactions:
            logger.error("Bad action '{}' allowed actions {} ".format(argparams["action"], allowactions))
            abort(400, "Bad action '{}' allowed actions '{}'".format(argparams["action"], allowactions))

        return func(*args, **kwargs)
    return decorated


@check_params_decorator
@check_interfaces_decorator
def ConfPorxyIP(method, params):
    """
        params:
            {"ddosgip":<ip address>,
             "clientip": <ip address>,
             "purpose": <vds, hosting>
             "action": <add, del>
             "location": <4, 9>"}"""

    interface, table = _get_interface_and_table_by_params(params)
    # send action from params
    _manage_ip(params["ddosgip"], interface, params["action"])
    _manage_ip_rules(params["clientip"], table, params["action"])
    _manage_iptables(params["ddosgip"], params["clientip"], interface, params["action"])

    logger.info("Recive and execute request {} ".format(params))


@check_params_decorator
@check_interfaces_decorator
def CheckProxySettings(method, params):
    """Check what ip proxy, not proxy or broken
       if no config ip addr or ip rule  or iptables return {proxy:broken}
       if all config exist for given params return status {proxy:YES}
       if no config exist for given params return {proxy:NO}
       params:
            {"ddosgip":<ip address>,
             "clientip": <ip address>,
             "purpose": <vds, hosting>
             "action": <chek>
             "location": <4, 9>"}"""
    error: str = ""

    # Ckeck flags
    ip_config = False
    ip_rule_config = False
    iptables_config = False

    interface, table = _get_interface_and_table_by_params(params)
    addresess = _get_list_ip_addreses(interface)
    ipr = IPRoute()
    try:
        if params["ddosgip"] in addresess:
            ip_config = True
        else:
            error = error + "ip address '{}' not set on interface '{}', ".format(params["ddosgip"], interface)

        if ipr.get_rules(family=AF_INET, table=table, src=str(params["clientip"])):
            ip_rule_config = True

        else:
            error = error + "ip address '{}' not in ip rule table '{}'".format(params["ddosgip"], table)
        ipr.close()

        preroutingrule = ["iptables", "-t", "nat", "-A", "PREROUTING", "-d", f"{params['ddosgip']}/32", "-i",
                          interface, "-j", "DNAT", "--to-destination", f"{params['clientip']}"]

        postrouting = ["iptables", "-t", "nat", "-A", "POSTROUTING", "-d", f"{params['clientip']}/32", "-o",
                       INTERFACE_HOSTING, "-j", "MASQUERADE"]

        postroutingsnat = ["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", interface,
                           "-s", f"{params['clientip']}/32", "-j", "SNAT", "--to-source", f"{params['ddosgip']}"]

        if _is_rule_exist(preroutingrule) and _is_rule_exist(postrouting) and _is_rule_exist(postroutingsnat):
            iptables_config = True
        else:
            if not _is_rule_exist(preroutingrule):
                error = error + "ip table PREROUTING rule  '{}' not exist, ".format(preroutingrule)
            if not _is_rule_exist(postrouting):
                error = error + "ip table POSTROUTING rule  '{}' not exist".format(postrouting)
            if not _is_rule_exist(postroutingsnat):
                error = error + "ip table POSTROUTING rule  '{}' not exist".format(postroutingsnat)

        # Result
        # All elements is True
        resultlist = [ip_config, ip_rule_config, iptables_config]
        if len([elem for elem in resultlist if elem]) == 3:
            return {"proxy": "yes"}
        # All elements is False
        elif len([elem for elem in resultlist if not elem]) == 3:
            return {"proxy": "no"}

        # Some elements True, broken config
        else:
            logger.error("Broken config '{}'".format(error))
            return {"proxy": "broken", "error": error}

    # CONINUE IPTABLES
    except Exception as e:
        ipr.close()
        logger.error("Error was occured in CheckProxySettings error: '{}'".format(e))
        abort(500, "Error was occured in CheckProxySettings error: '{}'".format(e))
    logger.info("Recive and execute GetProxySettings {} ".format(params))


def _get_interface_and_table_by_params(params):
    """for vps location 4  interface eth1.110 tabe 101
       for vps location 9  interface eth1.210 table 102
       for hosting location any  interface eth1.2 table 100
       """
    if params["purpose"].lower() == "hosting":
        return INTERFACE_HOSTING, DDOSG_RT_VH
    elif params["purpose"].lower() == "vds" and str(params["location"]) == "4":
        return INTERFACE_VDS_DC1, DDOSG_RT_VDS_DC1
    elif params["purpose"].lower() == "vds" and str(params["location"]) == "9":
        return INTERFACE_VDS_DC2, DDOSG_RT_VDS_DC2
    else:
        logger.error("Bad parameter values {} ".format(params))
        abort(400, "Bad parameter values {} ".format(params))


def _manage_ip(ddosgip, interface, action):
    ipr = IPRoute()
    interfaceindex = ipr.link_lookup(ifname=interface)
    try:
        ipr.addr(action, index=interfaceindex, address=ddosgip, mask=24)
    except Exception as e:
        ipr.close()
        logger.error("Error {} ip, interface {}, exception {}".format(action, interface, str(e)))
        raise e
    ipr.close()


def _manage_ip_rules(clientip, rttable, action=None):
    ipr = IPRoute()
    try:
        ipr.rule(action, table=rttable, src=clientip)
    except Exception as e:
        ipr.close()
        logger.error("Error ip rules {} ip {}, table {}, exception {}".format(action, clientip, rttable, str(e)))
        raise e
    ipr.close()


def _is_rule_exist(rule):
    # rule must be list
    # ["iptables", "-t", "nat", "-A", "PREROUTING", "-d", f"{ddosgip}/32", "-i", in_interface,
    #                      "-j", "DNAT", "--to-destination", f"{clientip}/32"]
    # in third position in list  must be action -A or -D
    # action replaces to -C for check if rule exist

    if len(rule) < 4:
        raise Exception(f"Error len of rule {rule}")

    # Create copy of rule
    tmp = rule[:]
    tmp[3] = "-C"
    # if return 0 rule exist
    if subprocess.call(tmp, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5) == 0:
        return True
    else:
        return False


def _manage_iptables(ddosgip, clientip, in_interface, action):
    """Example iptables for ddosgip 185.200.242.114 clientip 92.53.96.240
        iptables -t nat -A PREROUTING -d 185.200.242.114/32 -i eth1.110 -j DNAT --to-destination 92.53.96.240
        iptables -t nat -A POSTROUTING -d 92.53.96.240/32 -o eth1.2 -j MASQUERADE
        iptables -t nat -A POSTROUTING -o eth1.110 -s 92.53.96.240/32 -j SNAT --to-source 185.200.242.114/32
    """
    # static out interface eth1.2
    out_intarface = INTERFACE_HOSTING

    try:
        # Do not add rules if they exist
        # Rules in iptablas may be duplicated
        if action == "add":
            preroutingrule = ["iptables", "-t", "nat", "-A", "PREROUTING", "-d", f"{ddosgip}/32", "-i", in_interface,
                              "-j", "DNAT", "--to-destination", f"{clientip}"]

            postrouting = ["iptables", "-t", "nat", "-A", "POSTROUTING", "-d", f"{clientip}/32", "-o", out_intarface,
                           "-j", "MASQUERADE"]

            postroutingsnat = ["iptables", "-t", "nat", "-A", "POSTROUTING", "-o", f"{in_interface}",
                               "-s", f"{clientip}/32", "-j", "SNAT", "--to-source", f"{ddosgip}"]

            if not _is_rule_exist(preroutingrule):
                if subprocess.call(preroutingrule, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, timeout=5) != 0:
                    raise Exception(f"Error add rule {preroutingrule}")

            if not _is_rule_exist(postrouting):
                if subprocess.call(postrouting, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, timeout=5) != 0:
                    raise Exception(f"Error add rule {preroutingrule}")

            if not _is_rule_exist(postroutingsnat):
                if subprocess.call(postroutingsnat, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL, timeout=5) != 0:
                    raise Exception(f"Error add rule {postroutingsnat}")
        elif action == "del":
            preroutingrule = ["iptables", "-t", "nat", "-D", "PREROUTING", "-d", f"{ddosgip}/32", "-i", in_interface,
                              "-j", "DNAT", "--to-destination", f"{clientip}"]

            postrouting = ["iptables", "-t", "nat", "-D", "POSTROUTING", "-d", f"{clientip}/32", "-o", out_intarface,
                           "-j", "MASQUERADE"]

            postroutingsnat = ["iptables", "-t", "nat", "-D", "POSTROUTING", "-o", f"{in_interface}",
                               "-s", f"{clientip}/32", "-j", "SNAT", "--to-source", f"{ddosgip}"]

            if subprocess.call(preroutingrule, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=5) != 0:
                raise Exception(f"Error delete rule {preroutingrule}")

            if subprocess.call(postrouting, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=5) != 0:
                raise Exception(f"Error delete rule {preroutingrule}")

            if subprocess.call(postroutingsnat, stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL, timeout=5) != 0:
                raise Exception(f"Error delete rule {postroutingsnat}")

    except Exception as e:
        logger.error("Error manage {} iptables ddosgip {}, clientip {}, exception {}".format(action, ddosgip,
                                                                                             clientip, str(e)))
        raise e


def _get_list_ip_addreses(interface):
    # addresess {2: [{'addr': '192.168.1.162',
    # 'netmask': '255.255.240.0',
    # 'broadcast': '192.168.15.255'}], ..}
    all_addresess = netifaces.ifaddresses(interface)
    resultaddresslist = []

    # get all ipv4 addreses on interface
    if AF_INET in all_addresess.keys():
        tmpaddresess = all_addresess[AF_INET]
        for ipaddr in tmpaddresess:
            resultaddresslist.append(ipaddr["addr"])
    return resultaddresslist
