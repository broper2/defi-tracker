from abc import ABC, abstractmethod


class AccountAdapterBase(ABC):

    @property
    @abstractmethod
    def crypto_currency_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def usd_value(self):
        raise NotImplementedError
