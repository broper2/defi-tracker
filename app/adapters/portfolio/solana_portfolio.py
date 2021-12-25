from app.adapters.portfolio.base_portfolio import DefiPortfolioAdapterBase, DefiWalletAdapterBase
from app.config.constants import LAMPORT_TO_SOL_RATE
from app.external.solana_network import SolanaNetworkInterface


class SolanaPortfolioDataAdapter(DefiPortfolioAdapterBase):

    @property
    def _usd_rate(self):
        return self.binance_api.get_sol_usd_rate()

    @property
    def _child_adapter_cls(self):
        return SolanaWalletDataAdapter


class SolanaWalletDataAdapter(DefiWalletAdapterBase):

    def __init__(self, wallet_data, *args):
        super().__init__(wallet_data, *args)
        self._lamport_value = self.interface.get_account_balance(wallet_data.key)

    @property
    def _network_interface_cls(self):
        return SolanaNetworkInterface

    @property
    def _network_interface_cls_kwargs(self):
        return dict(initial_validator_data_cache=False)

    @property
    def crypto_currency_value(self):
        return self._lamport_value * LAMPORT_TO_SOL_RATE
