from app.utils.colors import get_random_hex_code
from app.utils.rounding import round_validator_performance


def get_validator_chart_data(validator_adapter):
    datasets = []
    labels = []
    for display_name, epoch_performances in zip(
            validator_adapter.get_display_names(), validator_adapter.get_chart_data()
    ):
        color_code = get_random_hex_code()
        datasets.append({
            'label': display_name,
            'data': [round_validator_performance(performance) for performance in epoch_performances],
            'fill': 'false',
            'borderColor': color_code,
            'backgroundColor': color_code,

        })
        labels = validator_adapter.get_x_axis_labels()
    return {
        'labels': labels,
        'datasets': datasets
    }