from abc import ABC, abstractmethod
import asyncio
from functools import cached_property

from app.external.binance_api import BinanceApiInterface
from app.utils.rounding import round_crypto, round_usd


class AsyncCompositeBase(ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_name_str = 'display_name'
        self.token_str = 'token'
        self.usd_str = 'usd'
        self.staked_str = 'staked'

    @abstractmethod
    def get_component_data(self):
        raise NotImplementedError

    @abstractmethod
    def _crypto_currency_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _display_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _staked(self):
        raise NotImplementedError

    def _get_usd_value(self, tokens, usd_rate):
        return tokens * usd_rate

    def _build_component_data(self, token_value, usd_rate):
        return {
            self.display_name_str: self._display_name,
            self.token_str: round_crypto(token_value),
            self.usd_str: round_usd(self._get_usd_value(token_value, usd_rate)),
            self.staked_str: self._staked,
        }


class AsyncDefiPortfolioAdapterBase(AsyncCompositeBase):

    def __init__(self, tracked_wallets, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._children = self._build_child_adapters(tracked_wallets, self._usd_rate)
        self.child_data = self._build_child_data()

    @property
    def composite_data(self):
        return self.child_data + [self.get_component_data()]

    def get_component_data(self):
        token_value = self._crypto_currency_value()
        usd_rate = self._usd_rate
        return self._build_component_data(token_value, usd_rate)

    @property
    @abstractmethod
    def _child_adapter_cls(self):
        raise NotImplementedError

    @cached_property
    @abstractmethod
    def _usd_rate(self):
        raise NotImplementedError

    def _build_child_data(self):
        return asyncio.run(self._get_child_composite_data())

    async def _get_child_composite_data(self):
        return await asyncio.gather(*(child.get_component_data() for child in self._children))

    @property
    def _binance_api(self):
        return BinanceApiInterface.instance()

    def _crypto_currency_value(self):
        return sum([data[self.token_str] for data in self.child_data])

    def _build_child_adapters(self, tracked_wallets, *adapter_args):
        children = []
        for tracked_wallet in tracked_wallets:
            children.append(self._child_adapter_cls(tracked_wallet, *adapter_args))
        return children

    @property
    def _display_name(self):
        return 'Portfolio Total'

    @property
    def _staked(self):
        return 'N/A'


class AsyncDefiWalletAdapterBase(AsyncCompositeBase):

    def __init__(self, wallet_data, usd_rate, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.interface = self._network_interface_cls.instance(**self._network_interface_cls_kwargs)
        self._usd_rate = usd_rate
        self.staked_bool = wallet_data.is_staked
        self.name = wallet_data.display_name
        self.wallet_key = wallet_data.key

    async def get_component_data(self):
        token_value = await self._crypto_currency_value()
        usd_rate = self._usd_rate
        return self._build_component_data(token_value, usd_rate)

    @property
    @abstractmethod
    def _network_interface_cls(self):
        raise NotImplementedError

    @property
    def _network_interface_cls_kwargs(self):
        return dict()

    @property
    def _display_name(self):
        return self.name

    @property
    def _staked(self):
        return str(self.staked_bool)
