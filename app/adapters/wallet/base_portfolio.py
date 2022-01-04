from abc import abstractmethod

from app.adapters.wallet.base_composite import CompositeWalletBase
from app.external.sync_interfaces.binance_api import BinanceApiInterface


class DefiPortfolioAdapterBase(CompositeWalletBase):

    def __init__(self, tracked_wallets):
        super().__init__()
        self._usd_rate = self._get_portfolio_usd_rate()
        self._children = self._build_child_adapters(tracked_wallets)
        self._child_data = self._build_child_data()

    @property
    def composite_data(self):
        return self._child_data + [self.get_component_data()]

    def get_component_data(self):
        token_value = self._crypto_currency_value()
        usd_rate = self._usd_rate
        return self._build_component_data(token_value, usd_rate)

    @property
    @abstractmethod
    def _child_adapter_cls(self):
        raise NotImplementedError

    @abstractmethod
    def _get_portfolio_usd_rate(self):
        raise NotImplementedError

    @abstractmethod
    def _get_child_composite_data(self):
        raise NotImplementedError

    @abstractmethod
    def _build_child_data(self):
        raise NotImplementedError

    @property
    def _binance_api(self):
        return BinanceApiInterface.instance()

    def _crypto_currency_value(self):
        return sum([data[self.token_str] for data in self._child_data])

    def _build_child_adapters(self, tracked_wallets):
        children = []
        for tracked_wallet in tracked_wallets:
            children.append(self._child_adapter_cls(tracked_wallet, self._usd_rate))
        return children

    @property
    def _display_name(self):
        return 'Portfolio Total'

    @property
    def _staked(self):
        return 'N/A'
