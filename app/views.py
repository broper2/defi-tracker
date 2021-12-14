import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from app.external.solana_network import SolanaNetworkInterface, SolanaQueryData
from app.forms import SolanaValidatorForm, SolanaWalletForm
from app.models import SolanaValidator, SolanaWallet
from app.utils.ui_data import get_validator_chart_data, get_wallet_table_data

logger = logging.getLogger(__name__)


solana_network_interface = SolanaNetworkInterface()


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
    validator_query_data = [SolanaQueryData(record.validator_vote_pubkey, record.display_name) for record in validator_records]
    validator_adapters = solana_network_interface.get_wrapped_validator_data(validator_query_data)
    chart_data = get_validator_chart_data(validator_adapters)
    if not form:
        form = SolanaValidatorForm(current_user_id, solana_network_interface.vote_account_keys)
    return render(request, 'validators.html', {'data': chart_data, 'form': form})


def get_validator_records(user_id):
    return SolanaValidator.objects.filter(user_id=user_id)


def wallets(request):
    current_user_id = request.user.username
    form = None
    if request.method == 'POST':
        form = SolanaWalletForm(current_user_id, request.POST)
        if form.is_valid():
            form.save()
    wallet_records = get_wallet_records(current_user_id)
    wallet_query_data = [SolanaQueryData(record.wallet_pubkey, record.display_name) for record in wallet_records]
    wallet_adapters = [solana_network_interface.get_wrapped_account_data(query_data) for query_data in wallet_query_data]
    data = get_wallet_table_data(wallet_adapters)
    if not form:
        form = SolanaWalletForm(current_user_id)
    return render(request, 'wallets.html', {'data': data, 'form': form})


def get_wallet_records(user_id):
    return SolanaWallet.objects.filter(user_id=user_id)
