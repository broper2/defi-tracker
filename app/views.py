import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from app.adapters.validator.builder import get_validator_adapter
from app.adapters.portfolio.builder import get_portfolio_adapter
from app.basetypes import SolanaWalletData, SolanaValidatorData
from app.config.constants import DEFAULT_DEFI_NETWORK, PROOF_OF_STAKE_DEFI
from app.forms import SolanaValidatorForm, SolanaWalletForm
from app.models import SolanaValidator, SolanaWallet
from app.utils.ui_data import get_validator_chart_data

logger = logging.getLogger(__name__)


def create_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'defi_index.html', {'network': DEFAULT_DEFI_NETWORK})
    else:
        form = UserCreationForm()
    return render(request, 'registration/create_user.html', {'form': form, 'network': DEFAULT_DEFI_NETWORK})


def defi_index(request, network=None):
    return render(request, 'defi_index.html', {'network': network})


def validators(request, network=None):
    if network not in PROOF_OF_STAKE_DEFI:
        return render(request, 'validators.html', {'network': network})
    current_user_id = request.user.username
    form = None
    if request.method == 'POST':
        form = SolanaValidatorForm(current_user_id, request.POST)
        if form.is_valid():
            form.save()
    tracked_validator_models = get_validator_records(current_user_id)
    tracked_validators = [SolanaValidatorData(model.validator_vote_pubkey, model.display_name) for model in
                          tracked_validator_models]
    validator_adapter = get_validator_adapter(network, tracked_validators)
    chart_data = get_validator_chart_data(validator_adapter)
    if not form:
        form = SolanaValidatorForm(current_user_id)
    return render(request, 'validators.html', {'data': chart_data, 'form': form, 'network': network})


def get_validator_records(user_id):
    return SolanaValidator.objects.filter(user_id=user_id)


def wallets(request, network=None):
    current_user_id = request.user.username
    form = None
    if request.method == 'POST':
        form = SolanaWalletForm(current_user_id, request.POST)
        if form.is_valid():
            form.save()
    wallet_models = get_wallet_records(current_user_id)
    wallets = [SolanaWalletData(model.wallet_pubkey, model.display_name, model.staked) for model in wallet_models]
    portfolio_adapter = get_portfolio_adapter(network, wallets)
    table_data = portfolio_adapter.composite_data
    if not form:
        form = SolanaWalletForm(current_user_id)
    return render(request, 'wallets.html', {'data': table_data, 'form': form, 'network': network})


def get_wallet_records(user_id):
    return SolanaWallet.objects.filter(user_id=user_id)
