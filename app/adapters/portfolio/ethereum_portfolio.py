from app.adapters.portfolio.base_portfolio import PortfolioCompositeBase, DefiWalletChildAdapter
from app.config.constants import WEI_TO_ETH_RATE
from app.external.ethereum_network import EthereumNetworkInterface


class EthereumPortfolioDataAdapter(PortfolioCompositeBase):

    def __init__(self, tracked_wallets):
        super().__init__()
        usd_sol_rate = self.binance_api.get_eth_usd_rate()
        self.child_adapters = self._build_child_adapters(tracked_wallets, usd_sol_rate)

    @property
    def _children(self):
        return self.child_adapters

    @property
    def _child_adapter_cls(self):
        return EthereumWalletDataAdapter


class EthereumWalletDataAdapter(DefiWalletChildAdapter):

    def __init__(self, wallet_data, *args):
        super().__init__(wallet_data, *args)
        self._wei_value = self.interface.get_account_balance(wallet_data.key)

    @property
    def _interface_cls(self):
        return EthereumNetworkInterface

    @property
    def _crypto_currency_value(self):
        return self._wei_value * WEI_TO_ETH_RATE
