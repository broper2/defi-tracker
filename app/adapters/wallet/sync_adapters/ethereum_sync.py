from app.adapters.wallet.sync_adapters.base_portfolio_sync import DefiPortfolioAdapterSyncBase
from app.adapters.wallet.sync_adapters.base_wallet_sync import DefiWalletAdapterSyncBase
from app.config.constants import WEI_TO_ETH_RATE
from app.external.sync_interfaces.ethereum_network import EthereumNetworkInterface


class EthereumPortfolioDataAdapter(DefiPortfolioAdapterSyncBase):

    def _get_portfolio_usd_rate(self):
        return self._binance_api.get_eth_usd_rate()

    @property
    def _child_adapter_cls(self):
        return EthereumWalletDataAdapter


class EthereumWalletDataAdapter(DefiWalletAdapterSyncBase):

    @property
    def _network_interface_cls(self):
        return EthereumNetworkInterface

    def _crypto_currency_value(self):
        wei_value = self._interface.get_account_balance(self._wallet_key)
        return wei_value * WEI_TO_ETH_RATE

