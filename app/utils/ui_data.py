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
        table_data.append({
            'display_name': adapter.display_name,
            'sol': adapter.sol_value,
            'usd': adapter.usd_value,
        })
    table_data.append(get_wallet_total_row_data(wallet_adapters))
    return table_data


def get_wallet_total_row_data(wallet_adapters):
    return {
        'display_name': 'Total',
        'sol': round_sol(sum([adapter.sol_value for adapter in wallet_adapters])),
        'usd': round_usd(sum([adapter.usd_value for adapter in wallet_adapters])),
    }