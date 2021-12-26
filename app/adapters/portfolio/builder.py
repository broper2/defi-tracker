from app.adapters.portfolio.sync_adapters import ethereum_portfolio
from app.adapters.portfolio.async_adapters import solana_portfolio_async


def get_portfolio_adapter(network_name, *args, **kwargs):
    portfolio_adapter_cls_map = {
        'SOLANA': solana_portfolio_async.AsyncSolanaPortfolioDataAdapter,
        'ETHEREUM': ethereum_portfolio.EthereumPortfolioDataAdapter,
    }
    adapter_cls = portfolio_adapter_cls_map[network_name.upper()]
    return adapter_cls(*args, **kwargs)
