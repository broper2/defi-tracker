from app.utils.colors import get_random_hex_code
from app.utils.rounding import round_sol, round_usd, round_validator_performance


def get_validator_chart_data(validator_adapter):
    if not validator_adapter or not validator_adapter.get_display_names():
        return {}
    datasets = []
    labels = []
    for display_name, epoch_performances in zip(
            validator_adapter.get_display_names(), validator_adapter.get_validator_performances()
    ):
        color_code = get_random_hex_code()
        datasets.append({
            'label': display_name,
            'data': [round_validator_performance(performance) for performance in epoch_performances],
            'fill': 'false',
            'borderColor': color_code,
            'backgroundColor': color_code,

        })
        labels = validator_adapter.get_epochs()
    return {
        'labels': labels,
        'datasets': datasets
    }


def get_wallet_table_data(wallet_adapters):
    if not wallet_adapters:
        return {}
    account_data = [(adapter.display_name, adapter.sol_value, adapter.usd_value) for adapter in wallet_adapters]
    table_data = []
    for name, sol, usd in account_data:
        table_data.append(_build_table_row(name, sol, usd))
    table_data.append(_get_wallet_total_row_data(account_data))
    return table_data


def _get_wallet_total_row_data(table_data):
    return _build_table_row(
        'Total',
        sum([account[1] for account in table_data]),
        sum([account[2] for account in table_data]),
    )

def _build_table_row(name, sol, usd):
    return {
        'display_name': name,
        'sol': round_sol(sol),
        'usd': round_usd(usd),
    }
