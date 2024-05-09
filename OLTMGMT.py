#!/usr/bin/env python

from snmp.FD12XX import FD1204, FD1208
from snmp.abc_oltmgmt import OLTManager
from argparse import ArgumentParser


def get_oltmgmt(model: str, host, community) -> OLTManager:
    olt_models = {'FD1204': FD1204, 'FD1208': FD1208}
    if model in olt_models.keys():
        return olt_models[model](host, community)
    else:
        raise KeyError(f'Model {model} not supported')


def autofind(model, host, community):
    olt = get_oltmgmt(model, host, community)
    result = olt.autofind
    print('host: ', olt._hostname)
    if result:
        print('port|  index   |    mac     ')
        for port, value in result.items():
            for i in value:
                print(f'{port:4}|{i['index']:10}|{i['mac']:12}')
    else:
        print('unregisterd ont not found')


def get_ont(model, host, community):
    olt = get_oltmgmt(model, host, community)
    result = olt.get_index_onu()
    print('port | onu  |   index    |         mac         |')
    for mac, index in result.items():
        frame, slot, port, onu = olt.indexonu_to_ports(index)
        print(f'{port:5}|{onu:5} | {index:10} | {mac:20}|')


def add_ont(model, host, community, port, ont_id, mac, descr=''):
    olt = get_oltmgmt(model, host, community)
    olt.add_onu(mac, port, ont_id)
    olt.onu_descr(descr, port, ont_id)
    olt.save_config()
    print(f'added port {port} ont id {ont_id} mac {mac} descr {descr}')

def ont_delete(model, host, community, port, ont_id):
    olt = get_oltmgmt(model, host, community)
    olt.onu_delete(port, ont_id)
    olt.save_config()
    print(f'port {port} ont {ont_id} deleted')


if __name__ == '__main__':
    parser = ArgumentParser(prog='OLT-MGMT')
    parser.add_argument('--version','-v', action="version", version='%(prog)s 0.0.1')
    parser.add_argument('command', type=str, choices=['autofind', 'get_ont', 'add_ont', 'ont_delete'],
                        help="choose an action")

    parser.add_argument('-model', type=str, choices=['FD1204', 'FD1208'], default='FD1204', help="choice of model")
    parser.add_argument('-host', type=str, help="host name or IP address")
    parser.add_argument('-c', type=str, help="snmp community write v2")
    parser.add_argument('-action', type=str, help="snmp username")
    parser.add_argument('-port', type=int, help="number pon port")
    parser.add_argument('-ont', type=int, help="number of ont")
    parser.add_argument('-mac', type=str, help="mac address ont")
    parser.add_argument('-descr', type=str,default='', help="description of ont")
    args = parser.parse_args()
    match args.command:
        case 'autofind':
            autofind(args.model, args.host, args.c)
        case 'get_ont':
            get_ont(args.model, args.host, args.c)
        case 'add_ont':
            add_ont(model=args.model, host=args.host, community=args.c, port=args.port, ont_id=args.ont, mac=args.mac,
                    descr=args.descr)
        case 'ont_delete':
            ont_delete(model=args.model, host=args.host, community=args.c, port=args.port, ont_id=args.ont)
