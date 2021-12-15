from app.utils.colors import get_random_hex_code
from app.utils.rounding import round_sol, round_usd


def get_validator_chart_data(validator_adapters):
    if not validator_adapters:
        return {}
    datasets = []
    labels = []
    for adapter in validator_adapters:
        color_code = get_random_hex_code()
        datasets.append({
            'label': adapter.display_name,
            'data': adapter.get_epoch_credit_history(),
            'fill': 'false',
            'borderColor': color_code,
            'backgroundColor': color_code,

        })
        labels = adapter.get_epoch_labels()
    return {
        'labels': labels,
        'datasets': datasets
    }


def get_wallet_table_data(wallet_adapters):
    if not wallet_adapters:
        return {}
    table_data = []
    for adapter in wallet_adapters:
        table_data.append(_build_table_row(adapter.display_name, adapter.sol_value, adapter.usd_value))
    table_data.append(_get_wallet_total_row_data(wallet_adapters))
    return table_data


def _get_wallet_total_row_data(wallet_adapters):
    return _build_table_row(
        'Total',
        sum([adapter.sol_value for adapter in wallet_adapters]),
        sum([adapter.usd_value for adapter in wallet_adapters]),
    )

def _build_table_row(name, sol, usd):
    return {
        'display_name': name,
        'sol': round_sol(sol),
        'usd': round_usd(usd),
    }
