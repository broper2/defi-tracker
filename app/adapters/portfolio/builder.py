from app.adapters.portfolio import solana_portfolio


def get_portfolio_adapter(network_name, *args, **kwargs):
    portfolio_adapter_cls_map = {
        'SOLANA': solana_portfolio.SolanaPortfolioDataAdapter
    }
    adapter_cls = portfolio_adapter_cls_map[network_name.upper()]
    return adapter_cls(*args, **kwargs)
