from app.adapters.portfolio.base_portfolio import DefiPortfolioAdapterBase, DefiWalletAdapterBase
from app.config.constants import WEI_TO_ETH_RATE
from app.external.ethereum_network import EthereumNetworkInterface


class EthereumPortfolioDataAdapter(DefiPortfolioAdapterBase):

    @property
    def _usd_rate(self):
        return self.binance_api.get_eth_usd_rate()

    @property
    def _child_adapter_cls(self):
        return EthereumWalletDataAdapter


class EthereumWalletDataAdapter(DefiWalletAdapterBase):

    def __init__(self, wallet_data, *args):
        super().__init__(wallet_data, *args)
        self._wei_value = self.interface.get_account_balance(wallet_data.key)

    @property
    def _network_interface_cls(self):
        return EthereumNetworkInterface

    @property
    def crypto_currency_value(self):
        return self._wei_value * WEI_TO_ETH_RATE
