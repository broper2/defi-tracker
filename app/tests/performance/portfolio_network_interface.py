from time import perf_counter

from contextlib import contextmanager

from app.adapters.portfolio.async_adapters.solana_portfolio_async import AsyncSolanaPortfolioDataAdapter
from app.adapters.portfolio.sync_adapters.solana_portfolio import SolanaPortfolioDataAdapter
from app.basetypes import DefiWalletData


@contextmanager
def catchtime() -> float:
    start = perf_counter()
    yield lambda: perf_counter() - start


SAMPLE_SOLANA_ACCOUNT_KEY = '4DfKXjLB5f2zJJ65pxt7zjyfHjR92zDFi6nEy2DFmF95'


def build_wallet_data(num_wallets):
    return [DefiWalletData(SAMPLE_SOLANA_ACCOUNT_KEY, f'wallet{i}', False) for i in range(num_wallets)]


def time_solana_portfolio_composite_data_sync(num_wallets):
    wallet_data = build_wallet_data(num_wallets)
    with catchtime() as timed:
        portfolio_adapter = SolanaPortfolioDataAdapter(wallet_data)
        print(portfolio_adapter.composite_data)
    return timed


def time_solana_portfolio_composite_data_async(num_wallets):
    wallet_data = build_wallet_data(num_wallets)
    with catchtime() as timed:
        portfolio_adapter = AsyncSolanaPortfolioDataAdapter(wallet_data)
        print(portfolio_adapter.composite_data)
    return timed


if __name__ == '__main__':
    print('sync')
    print(time_solana_portfolio_composite_data_sync(10)())
    print('async')
    print(time_solana_portfolio_composite_data_async(10)())