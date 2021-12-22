import logging

from django.contrib.auth import authenticate, login
from app.forms import CustomUserCreationForm
from django.shortcuts import render

from app.adapters.validator.builder import get_validator_adapter
from app.adapters.portfolio.builder import get_portfolio_adapter
from app.basetypes import DefiWalletData, DefiValidatorData
from app.config.constants import DEFAULT_DEFI_NETWORK, PROOF_OF_STAKE_DEFI, SUPPORTED_DEFI_NETWORKS
from app.forms import get_wallet_form_cls, get_validator_form_cls
from app.models import DefiValidator, DefiWallet
from app.utils.ui_data import get_validator_chart_data

logger = logging.getLogger(__name__)


def create_user(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return defi_index(request)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/create_user.html', {'form': form, 'network': DEFAULT_DEFI_NETWORK})


def is_invalid_network(network):
    return network not in SUPPORTED_DEFI_NETWORKS


def defi_index(request):
    return render(request, 'defi_index.html')


def validators(request, network=None):
    if is_invalid_network(network):
        return defi_index(request)
    current_user_id = request.user.username
    form = None
    form_cls = get_validator_form_cls(network)
    if request.method == 'POST':
        form = form_cls(current_user_id, network, request.POST)
        if form.is_valid():
            form.save()
    tracked_validator_models = get_validator_records(current_user_id, network)
    tracked_validators_data = [DefiValidatorData(model.validator_vote_pubkey, model.display_name) for model in
                          tracked_validator_models]
    validator_adapter = get_validator_adapter(network, tracked_validators_data)
    chart_data = get_validator_chart_data(validator_adapter)
    modal_form_data = get_delete_modal_form_data(tracked_validators_data)
    if not form:
        form = form_cls(current_user_id, network)
    return render(request, 'validators.html', {'data': chart_data, 'form': form, 'network': network, 'modal_data': modal_form_data})


def get_validator_records(user_id, network):
    return DefiValidator.objects.filter(user_id=user_id, defi_network=network)


def wallets(request, network=None):
    if is_invalid_network(network):
        return defi_index(request)
    current_user_id = request.user.username
    form = None
    form_cls = get_wallet_form_cls(network)
    if request.method == 'POST':
        form = form_cls(current_user_id, network, request.POST)
        if form.is_valid():
            form.save()
    tracked_wallet_models = get_wallet_records(current_user_id, network)
    tracked_wallets_data = [DefiWalletData(model.wallet_pubkey, model.display_name, model.staked) for model in tracked_wallet_models]
    portfolio_adapter = get_portfolio_adapter(network, tracked_wallets_data)
    table_data = portfolio_adapter.composite_data
    modal_form_data = get_delete_modal_form_data(tracked_wallets_data)
    if not form:
        form = form_cls(current_user_id, network)
    return render(request, 'wallets.html', {'data': table_data, 'form': form, 'network': network, 'modal_data': modal_form_data})


def get_wallet_records(current_user_id, network):
    return DefiWallet.objects.filter(user_id=current_user_id, defi_network=network)


def get_delete_modal_form_data(tracked_data):
    return [{'key': data.key, 'display_name': data.display_name} for data in tracked_data]
