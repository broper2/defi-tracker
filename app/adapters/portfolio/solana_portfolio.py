from app.adapters.portfolio.base_portfolio import PortfolioCompositeBase, DefiWalletChildAdapter
from app.config.constants import LAMPORT_TO_SOL_RATE
from app.external.solana_network import SolanaNetworkInterface


class SolanaPortfolioDataAdapter(PortfolioCompositeBase):

    def __init__(self, tracked_wallets):
        super().__init__()
        usd_sol_rate = self.binance_api.get_sol_usd_rate()
        self.child_adapters = self._build_child_adapters(tracked_wallets, usd_sol_rate)

    @property
    def _children(self):
        return self.child_adapters

    @property
    def _child_adapter_cls(self):
        return SolanaWalletDataAdapter

    @property
    def _crypto_currency_value(self):
        return sum([child._crypto_currency_value for child in self._children])

    @property
    def _usd_value(self):
        return sum([child._usd_value for child in self._children])

    @property
    def _display_name(self):
        return 'Portfolio Total'

    @property
    def _staked(self):
        return 'N/A'


class SolanaWalletDataAdapter(DefiWalletChildAdapter):

    def __init__(self, wallet_data, *args):
        super().__init__(wallet_data, *args)
        self._lamport_value = self.interface.get_account_balance(wallet_data.key)

    @property
    def _interface_cls(self):
        return SolanaNetworkInterface

    @property
    def _crypto_currency_value(self):
        return self._lamport_value * LAMPORT_TO_SOL_RATE
