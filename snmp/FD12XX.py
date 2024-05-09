import datetime
from enum import Enum

from pyasn1.type import univ
from pysnmp.hlapi import ObjectType, ObjectIdentity, SnmpEngine, EndOfMibView, CommunityData, Integer32, NoSuchInstance
from pysnmp.proto.rfc1902 import OctetString

from .oid.oid_FD12 import *

from .connect import SNMP
from .abc_oltmgmt import OLTManager

def mac(mac_snmp: str):
    mac = []
    for i in map(int, mac_snmp):
        mac.append(i.to_bytes(1).hex())
    return f'{mac[0]}:{mac[1]}:{mac[2]}:{mac[3]}:{mac[4]}:{mac[5]}'


def hex_to_date(hex_date: str) -> datetime:
    year = int(hex_date[0:2].hex(), 16)
    month = int(hex_date[2:3].hex(), 16)
    day = int(hex_date[3:4].hex(), 16)
    hours = int(hex_date[4:5].hex(), 16)
    minutes = int(hex_date[5:6].hex(), 16)
    seconds = int(hex_date[6:7].hex(), 16)
    return datetime.datetime(year=year, month=month, day=day, hour=hours, minute=minutes, second=seconds)


class STATUS(Enum):
    UP = 1
    DOWN = 2
    TESTING = 3


class FD12(OLTManager):
    port_ratio = 0

    def __init__(self, hostname, community):

        self.engine = SnmpEngine()
        self._hostname = hostname
        self._community = CommunityData(community, mpModel=1)
        self.autofind_table = {}
        self.list_onu = {}
        self._snmp_host = SNMP(self._community, self._hostname)

    @classmethod
    def indexonu_to_ports(cls, indexonu: str):
        indexonu = f'{indexonu:08X}'
        device = int(indexonu[0:2], 16)
        slot = int(indexonu[2:4], 16)
        port = int(indexonu[4:6], 16) - cls.port_ratio
        onu = int(indexonu[6:], 16)
        return device, slot, port, onu

    @classmethod
    def port_to_indexonu(cls, device=1, slot=0, port=1, onu=1):
        port = port + cls.port_ratio
        indexonu = f'{device:02x}{slot:02X}{port:02X}{onu:02X}'
        return int(indexonu, 16)

    def get_index_onu(self):
        mac_onu_oid = (ObjectType(ObjectIdentity(onuMacAddress)),)
        onus = self._snmp_host.bulk(mac_onu_oid)

        for varbind in onus:
            if isinstance(varbind[1], EndOfMibView):
                break
            self.list_onu[mac(varbind[1])] = varbind[0][-1]
        return self.list_onu

    def get_onu_status(self, index):
        onu_status = {}
        onu_status_param = {}
        indexOnu = index
        onu_status_q = (ObjectType(ObjectIdentity(onuName + (indexOnu,))),
                        ObjectType(ObjectIdentity(onuOperationStatus + (indexOnu,))),
                        ObjectType(ObjectIdentity(onuTestDistance + (indexOnu,))),
                        ObjectType(ObjectIdentity(onuChipVendor + (indexOnu,))),
                        ObjectType(ObjectIdentity(onuChipType + (indexOnu,))),
                        ObjectType(ObjectIdentity(onuTimeSinceLastRegister + (indexOnu,))),
                        ObjectType(ObjectIdentity(onuTimeLastRegister + (indexOnu,))),)

        onus = self._snmp_host.get(onu_status_q)
        for varbind in onus:
            if varbind[0][:-1] == onuName:
                onu_status_param['Name'] = str(varbind[1])
            if varbind[0][:-1] == onuOperationStatus:
                if isinstance(varbind[1], NoSuchInstance):
                    onu_status['info'] = {'message': 'No such instance'}
                    return onu_status
                onu_status_param['OperStatus'] = STATUS(varbind[1])
            if varbind[0][:-1] == onuTestDistance:
                onu_status_param['Distance'] = int(varbind[1])
            if varbind[0][:-1] == onuChipVendor:
                onu_status_param['ChipVendor'] = str(varbind[1])
            if varbind[0][:-1] == onuChipType:
                onu_status_param['onuChipType'] = str(varbind[1])
            if varbind[0][:-1] == onuTimeSinceLastRegister:
                onu_status_param['onuTimeSinceLastRegister'] = str(
                    datetime.timedelta(seconds=int(varbind[1])))
            if varbind[0][:-1] == onuTimeLastRegister:
                onu_status_param['onuTimeLastRegister'] = hex_to_date(bytes(varbind[1]))
        onu_status['info'] = onu_status_param
        if onu_status_param['OperStatus'] == STATUS.UP:
            onu_status['optical'] = self._get_onu_optical(indexOnu)

        return onu_status

    def _get_onu_optical(self, indexOnu):
        onu_optical = {}
        onu_status_q = (ObjectType(ObjectIdentity(onuReceivedOpticalPower + (indexOnu, 0, 0,))),
                        ObjectType(ObjectIdentity(onuTramsmittedOpticalPower + (indexOnu, 0, 0,))),
                        ObjectType(ObjectIdentity(onuBiasCurrent + (indexOnu, 0, 0,))),
                        ObjectType(ObjectIdentity(onuWorkingVoltage + (indexOnu, 0, 0,))),
                        ObjectType(ObjectIdentity(onuWorkingTemperature + (indexOnu, 0, 0,))),)
        onus = self._snmp_host.get(onu_status_q)

        for varbind in onus:

            if isinstance(varbind[1], NoSuchInstance):
                onu_optical['message'] = 'No Such Instance...ists at this OID'
                return onu_optical
            if varbind[0][:-3] == onuReceivedOpticalPower:
                onu_optical['ReceivedOpticalPower (dBm)'] = int(varbind[1]) / 100
            if varbind[0][:-3] == onuTramsmittedOpticalPower:
                onu_optical['TransmittedOpticalPower (dBm)'] = int(varbind[1]) / 100
            if varbind[0][:-3] == onuBiasCurrent:
                onu_optical['BiasCurrent (mA)'] = int(varbind[1]) / 1000
            if varbind[0][:-3] == onuWorkingVoltage:
                onu_optical['WorkingVoltage (V)'] = int(varbind[1]) / 10000
            if varbind[0][:-3] == onuWorkingTemperature:
                onu_optical['WorkingTemperature (C)'] = int(varbind[1]) / 100
        return onu_optical

    def reboot_onu(self, indexOnu):
        rebootonu = (ObjectType(ObjectIdentity(resetOnu + (indexOnu,)), Integer32(1)),)
        self._snmp_host.set(rebootonu)

    @property
    def autofind(self):
        self.autofind_table = {}
        self.get_autofind()
        return self.autofind_table

    def get_autofind(self):
        findIndex = (ObjectType(ObjectIdentity(onuAutoFindMacAddress)),)

        for i, v in self._snmp_host.bulk(findIndex):
            if isinstance(v, EndOfMibView):
                continue
            port, onu_id = self.indexonu_to_ports(i[-1])[2:]
            self.autofind_table[port] = []
            self.autofind_table[port].append({'index': onu_id, 'mac': mac(v)})

    def add_onu(self, mac, port=1, onu_id=1):
        mac = '{}{}{}{}{}{}'.format(*mac.split(':'))
        port = port
        onu_index = self.port_to_indexonu(port=port, onu=onu_id)
        add_onu = (ObjectType(ObjectIdentity(onuAuthenMacAddress + (onu_index,)),
                              OctetString(hexValue=mac)),
                   ObjectType(ObjectIdentity(onuAuthenRowStatus + (onu_index,)),
                              Integer32(RowStatus.active.value)),)
        res = self._snmp_host.set(add_onu)

    def onu_descr(self, descr, port=1, onu_id=1):
        index_onu = self.port_to_indexonu(port=port, onu=onu_id)
        descr = (ObjectType(ObjectIdentity(onuName + (index_onu,)), OctetString(descr)),)
        self._snmp_host.set(descr)

    def onu_delete(self, port=1, onu_id=1):
        onu_index = self.port_to_indexonu(port=port, onu=onu_id)
        onu_del = (ObjectType(ObjectIdentity(onuAuthenRowStatus + (onu_index,)), Integer32(RowStatus.destroy.value)),)
        self._snmp_host.set(onu_del)

    def save_config(self):
        save = (ObjectType(ObjectIdentity(saveConfig + (0,)), Integer32(1)),)
        self._snmp_host.set(save)


class FD1204(FD12):
    port_ratio = 6


class FD1208(FD12):
    port_ratio = 12


