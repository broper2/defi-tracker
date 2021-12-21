from app.adapters.portfolio import solana_portfolio, ethereum_portfolio


def get_portfolio_adapter(network_name, *args, **kwargs):
    portfolio_adapter_cls_map = {
        'SOLANA': solana_portfolio.SolanaPortfolioDataAdapter,
        'ETHEREUM': ethereum_portfolio.EthereumPortfolioDataAdapter,
    }
    adapter_cls = portfolio_adapter_cls_map[network_name.upper()]
    return adapter_cls(*args, **kwargs)
