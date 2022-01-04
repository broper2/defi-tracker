from app.adapters.wallet.sync_adapters.base_portfolio_sync import DefiPortfolioAdapterSyncBase
from app.adapters.wallet.sync_adapters.base_wallet_sync import DefiWalletAdapterSyncBase
from app.config.constants import LAMPORT_TO_SOL_RATE
from app.external.sync_interfaces.solana_network import SolanaNetworkInterface


class SolanaPortfolioDataAdapter(DefiPortfolioAdapterSyncBase):

    def _get_portfolio_usd_rate(self):
        return self._binance_api.get_sol_usd_rate()

    @property
    def _child_adapter_cls(self):
        return SolanaWalletDataAdapter


class SolanaWalletDataAdapter(DefiWalletAdapterSyncBase):

    @property
    def _network_interface_cls(self):
        return SolanaNetworkInterface

    @property
    def _network_interface_cls_kwargs(self):
        return dict(initial_validator_data_cache=False)

    def _crypto_currency_value(self):
        lamports = self._interface.get_account_balance(self._wallet_key)
        return lamports * LAMPORT_TO_SOL_RATE
