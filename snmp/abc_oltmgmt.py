from abc import ABC, abstractmethod


class OLTManager(ABC):

    @classmethod
    @abstractmethod
    def indexonu_to_ports(cls, indexonu: str):
        return None

    @classmethod
    @abstractmethod
    def port_to_indexonu(cls, device=0, slot=0, port=1, onu=1):
        return None

    @abstractmethod
    def get_index_onu(self):
        return None



    @abstractmethod
    def get_onu_status(self, index):
        return None

    @abstractmethod
    def reboot_onu(self, index_onu):
        return None

    @abstractmethod
    def autofind(self):
        return None

    @abstractmethod
    def get_autofind(self):
        return None

    @abstractmethod
    def add_onu(self, mac, port=1, onu_id=1):
        return None

    @abstractmethod
    def onu_descr(self, descr, port=1, onu_id=1):
        return None

    @abstractmethod
    def onu_delete(self, port=1, onu_id=1):
        return None

    @abstractmethod
    def save_config(self):
        return None
