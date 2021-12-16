from app.adapters.account import solana_account


def get_account_adapter(network_name, *args, **kwargs):
    account_adapter_cls_map = {
        'SOLANA': solana_account.SolanaAccountDataAdapter
    }
    adapter_cls = account_adapter_cls_map[network_name.upper()]
    return adapter_cls(*args, **kwargs)
