from abc import ABC, abstractmethod


class DefiNetworkInterfaceBase(ABC):

    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    @abstractmethod
    def is_valid_account_pubkey(self, pubkey):
        raise NotImplementedError

    @abstractmethod
    def get_account_balance(self, pubkey):
        raise NotImplementedError