from abc import ABC, abstractmethod

from app.external.sync.binance_api import BinanceApiInterface
from app.utils.rounding import round_crypto, round_usd


class CompositeBase(ABC):

    def get_component_data(self):
        return {
            'display_name': self.display_name,
            'token': round_crypto(self.crypto_currency_value),
            'usd': round_usd(self.usd_value),
            'staked': self.staked,
        }

    @property
    @abstractmethod
    def crypto_currency_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def usd_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def display_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def staked(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _children(self):
        raise NotImplementedError


class DefiPortfolioAdapterBase(CompositeBase):

    def __init__(self, tracked_wallets, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tracked_wallets = tracked_wallets
        self._child_adapters = self._build_child_adapters(self.tracked_wallets, self._usd_rate)

    @property
    def composite_data(self):
        data = []
        for child in self._children:
            data.append(child.get_component_data())
        data.append(self.get_component_data())
        return data

    @property
    def binance_api(self):
        return BinanceApiInterface.instance()

    @property
    def crypto_currency_value(self):
        return sum([child.crypto_currency_value for child in self._children])

    @property
    def usd_value(self):
        return sum([child.usd_value for child in self._children])

    @property
    def _children(self):
        return self._child_adapters

    @property
    @abstractmethod
    def _child_adapter_cls(self):
        raise NotImplementedError

    def _build_child_adapters(self, tracked_wallets, *adapter_args):
        children = []
        for tracked_wallet in tracked_wallets:
            children.append(self._child_adapter_cls(tracked_wallet, *adapter_args))
        return children

    @property
    def display_name(self):
        return 'Portfolio Total'

    @property
    def staked(self):
        return 'N/A'

    @property
    @abstractmethod
    def _usd_rate(self):
        raise NotImplementedError


class DefiWalletAdapterBase(CompositeBase):

    def __init__(self, wallet_data, usd_rate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = self._network_interface_cls.instance(**self._network_interface_cls_kwargs)
        self._usd_rate = usd_rate
        self.staked_bool = wallet_data.is_staked
        self.name = wallet_data.display_name

    @property
    @abstractmethod
    def _network_interface_cls(self):
        raise NotImplementedError

    @property
    def _network_interface_cls_kwargs(self):
        return dict()

    @property
    def _children(self):
        return []

    @property
    @abstractmethod
    def crypto_currency_value(self):
        raise NotImplementedError

    @property
    def usd_value(self):
        return self.crypto_currency_value * self._usd_rate

    @property
    def display_name(self):
        return self.name

    @property
    def staked(self):
        return str(self.staked_bool)
