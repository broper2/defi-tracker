from app.adapters.wallet.sync_adapters import ethereum_sync
from app.adapters.wallet.async_adapters import solana_async


def get_portfolio_adapter(network_name, *args, **kwargs):
    portfolio_adapter_cls_map = {
        'SOLANA': solana_async.AsyncSolanaPortfolioDataAdapter,
        'ETHEREUM': ethereum_sync.EthereumPortfolioDataAdapter,
    }
    adapter_cls = portfolio_adapter_cls_map[network_name.upper()]
    return adapter_cls(*args, **kwargs)
