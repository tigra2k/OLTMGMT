from enum import Enum
from pysnmp.hlapi import *

engine = SnmpEngine()


class SNMPError(Exception):
    pass


class SNMP:
    def __init__(self, community: CommunityData, host, port=161):
        self.snmpEngine = SnmpEngine()
        self.community = community
        self.host = host
        self.port = port

    def get(self, oid: tuple) -> list:
        var_tables = getCmd(self.snmpEngine,
                            self.community,
                            UdpTransportTarget((self.host, self.port), retries=1),
                            ContextData(), *oid, lexicographicMode=False, lookupMib=False)
        result = []
        for errorIndication, errorStatus, errorIndex, varBinds in var_tables:
            if errorIndication:
                raise SNMPError('SNMPError: %s' % errorStatus.prettyPrint())
            else:
                if errorStatus:
                    raise SNMPError( 'SNMPError: %s ' % errorStatus.prettyPrint())
                else:
                    for varBind in varBinds:
                        result.append(varBind)
        var_tables.close()
        return result

    def set(self, oid):
        var_tables = setCmd(self.snmpEngine,
                            self.community,
                            UdpTransportTarget((self.host, self.port)),
                            ContextData(), *oid)
        result = []
        for errorIndication, errorStatus, errorIndex, varBinds in var_tables:
            if errorIndication:
                raise SNMPError(errorIndication, errorStatus)
            else:
                if errorStatus:
                    raise SNMPError('SNMPError: %s ' % errorStatus.prettyPrint())

                else:
                    for varBind in varBinds:
                        result.append(varBind)

        return result

    def bulk(self, oid: tuple):
        varTables = bulkCmd(self.snmpEngine,
                            self.community,
                            UdpTransportTarget((self.host, self.port), timeout=2, retries=1),
                            ContextData(),
                            0, 2,
                            *oid, lexicographicMode=False, lookupMib=False)
        result = []
        for errorIndication, errorStatus, errorIndex, varBinds in varTables:
            if errorIndication:
                raise SNMPError(errorIndication, errorStatus)
            else:
                if errorStatus:
                    print(
                        '%s at %s' % (errorStatus.prettyPrint(), varBinds[int(errorIndex) - 1] if errorIndex else '?'))
                else:
                    for varBind in varBinds:
                        result.append(varBind)
        varTables.close()
        return result
