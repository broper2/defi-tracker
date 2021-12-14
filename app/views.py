import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from .external.binance_api import BinanceApiInterface
from .external.solana_network import SolanaNetworkInterface
from .forms import SolanaValidatorForm, SolanaWalletForm
from .models import SolanaValidator, SolanaWallet
from .utils.colors import get_random_hex_code
from .utils.rounding import round_sol, round_usd

logger = logging.getLogger(__name__)

solana_network_interface = SolanaNetworkInterface()
binance_api = BinanceApiInterface()


def index(request):
    return render(request, 'index.html')


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'index.html')
    else:
        form = UserCreationForm()
    return render(request, 'registration/create_user.html', {'form': form})


def validators(request):
    current_user_id = request.user.username
    form = None
    if request.method == 'POST':
        form = SolanaValidatorForm(current_user_id, solana_network_interface.vote_account_keys, request.POST)
        if form.is_valid():
            form.save()
    validator_records = get_validator_records(current_user_id)
    data = get_validator_chart_data(validator_records) if validator_records else {}
    if not form:
        form = SolanaValidatorForm(current_user_id, solana_network_interface.vote_account_keys)
    return render(request, 'validators.html', {'data': data, 'form': form})


def get_validator_records(user_id):
    return SolanaValidator.objects.filter(user_id=user_id)


def get_validator_chart_data(validator_records):
    wrappers = solana_network_interface.get_wrapped_validator_data([v.validator_vote_pubkey for v in validator_records])
    datasets = []
    for record, solana_data_wrapper in zip(validator_records, wrappers):
        color_code = get_random_hex_code()
        datasets.append({
            'label': record.display_name,
            'data': solana_data_wrapper.get_epoch_credit_history(),
            'fill': 'false',
            'borderColor': color_code,
            'backgroundColor': color_code,

        })
    labels = wrappers[0].get_epoch_labels() if wrappers else []
    data = {
        'labels': labels,
        'datasets': datasets
    }
    return data


def wallets(request):
    current_user_id = request.user.username
    form = None
    if request.method == 'POST':
        form = SolanaWalletForm(current_user_id, request.POST)
        if form.is_valid():
            form.save()
    wallet_records = get_wallet_records(current_user_id)
    data = get_wallet_table_data(wallet_records) if wallet_records else {}
    if not form:
        form = SolanaWalletForm(current_user_id)
    return render(request, 'wallets.html', {'data': data, 'form': form})


def get_wallet_records(user_id):
    return SolanaWallet.objects.filter(user_id=user_id)


def get_wallet_table_data(wallet_records):
    table_data = []
    wallet_pubkeys = [record.wallet_pubkey for record in wallet_records]
    wallet_sol_tokens = [solana_network_interface.get_account_sol_balance(pubkey) for pubkey in wallet_pubkeys]
    wallet_usd_values = binance_api.get_usd_from_sols(wallet_sol_tokens)
    for record, sol, usd in zip(wallet_records, wallet_sol_tokens, wallet_usd_values):
        table_data.append({
            'display_name': record.display_name,
            'sol': sol,
            'usd': usd,
        })
    table_data.append(get_wallet_sum_row_data(wallet_sol_tokens, wallet_usd_values))
    return table_data


def get_wallet_sum_row_data(sol, usd):
    return {
        'display_name': 'Total',
        'sol': round_sol(sum(sol)),
        'usd': round_usd(sum(usd)),
    }
