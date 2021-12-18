from app.adapters.portfolio.base_portfolio import PortfolioCompositeBase
from app.config.constants import LAMPORT_TO_SOL_RATE
from app.external.binance_api import BinanceApiInterface
from app.external.solana_network import SolanaNetworkInterface


class SolanaPortfolioDataAdapter(PortfolioCompositeBase):

    def __init__(self, tracked_wallets):
        self.binance_api = BinanceApiInterface.instance()
        usd_sol_rate = self.binance_api.get_sol_usd_rate()
        self.child_adapters = []
        for tracked_wallet in tracked_wallets:
            self.child_adapters.append(SolanaWalletDataAdapter(tracked_wallet, usd_sol_rate))

    @property
    def _children(self):
        return self.child_adapters

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


class SolanaWalletDataAdapter(PortfolioCompositeBase):

    def __init__(self, wallet_data, usd_sol_rate):
        interface = SolanaNetworkInterface.instance()
        self._lamport_value = interface.get_account_balance(wallet_data.key)
        self.usd_sol_rate = usd_sol_rate
        self.staked_bool = wallet_data.is_staked
        self.name = wallet_data.display_name

    @property
    def _children(self):
        return []

    @property
    def _crypto_currency_value(self):
        return self._lamport_value * LAMPORT_TO_SOL_RATE

    @property
    def _usd_value(self):
        return self._crypto_currency_value * self.usd_sol_rate

    @property
    def _display_name(self):
        return self.name

    @property
    def _staked(self):
        return str(self.staked_bool)
