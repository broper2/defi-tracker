from app.adapters.wallet.async_adapters.base_portfolio_async import DefiPortfolioAdapterAsyncBase
from app.adapters.wallet.async_adapters.base_wallet_async import DefiWalletAdapterAsyncBase
from app.config.constants import LAMPORT_TO_SOL_RATE
from app.external.async_interfaces.solana_network_async import AsyncSolanaNetworkInterface


class AsyncSolanaPortfolioDataAdapter(DefiPortfolioAdapterAsyncBase):

    def _get_portfolio_usd_rate(self):
        return self._binance_api.get_sol_usd_rate()

    @property
    def _child_adapter_cls(self):
        return AsyncSolanaWalletDataAdapter


class AsyncSolanaWalletDataAdapter(DefiWalletAdapterAsyncBase):

    @property
    def _network_interface_cls(self):
        return AsyncSolanaNetworkInterface

    @property
    def _network_interface_cls_kwargs(self):
        return dict(initial_validator_data_cache=False)

    async def _crypto_currency_value(self):
        lamports = await self._interface.get_account_balance(self._wallet_key)
        return lamports * LAMPORT_TO_SOL_RATE
