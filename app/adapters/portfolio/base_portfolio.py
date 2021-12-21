from abc import ABC, abstractmethod

from app.external.binance_api import BinanceApiInterface
from app.utils.rounding import round_crypto, round_usd


class PortfolioCompositeBase(ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.binance_api = BinanceApiInterface.instance()

    @property
    def composite_data(self):
        data = []
        for child in self._children:
            data.append(child._get_composite_data())
        data.append(self._get_composite_data())
        return data

    def _get_composite_data(self):
        return {
            'display_name': self._display_name,
            'token': round_crypto(self._crypto_currency_value),
            'usd': round_usd(self._usd_value),
            'staked': self._staked,
        }

    @property
    @abstractmethod
    def _children(self):
        raise NotImplementedError

    @property
    def _child_adapter_cls(self):
        raise NotImplementedError

    def _build_child_adapters(self, tracked_wallets, *adapter_args):
        children = []
        for tracked_wallet in tracked_wallets:
            children.append(self._child_adapter_cls(tracked_wallet, *adapter_args))
        return children

    @property
    @abstractmethod
    def _crypto_currency_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _usd_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _display_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _staked(self):
        raise NotImplementedError


class DefiWalletChildAdapter(PortfolioCompositeBase):

    def __init__(self, wallet_data, usd_rate):
        self.interface = self._interface_cls.instance()
        self.usd_rate = usd_rate
        self.staked_bool = wallet_data.is_staked
        self.name = wallet_data.display_name

    @property
    @abstractmethod
    def _interface_cls(self):
        raise NotImplementedError

    @property
    def _children(self):
        return []

    @property
    @abstractmethod
    def _crypto_currency_value(self):
        raise NotImplementedError

    @property
    def _usd_value(self):
        return self._crypto_currency_value * self.usd_rate

    @property
    def _display_name(self):
        return self.name

    @property
    def _staked(self):
        return str(self.staked_bool)
