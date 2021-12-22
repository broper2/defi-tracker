import logging

from django.contrib.auth import authenticate, login

from app.forms import CustomUserCreationForm
from django.shortcuts import render, redirect

from app.adapters.validator.builder import get_validator_adapter
from app.adapters.portfolio.builder import get_portfolio_adapter
from app.basetypes import DefiWalletData, DefiValidatorData
from app.config.constants import DEFAULT_DEFI_NETWORK, SUPPORTED_DEFI_NETWORKS
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


def defi_index(request, **kwargs):
    return render(request, 'defi_index.html')


def validators(request, network=None):
    if _is_invalid_network(network):
        return defi_index(request)
    current_user_id = request.user.username
    form = None
    form_cls = get_validator_form_cls(network)
    if request.method == 'POST':
        form = form_cls(current_user_id, network, request.POST)
        if form.is_valid():
            form.save()
    tracked_validator_models = _get_validator_records(current_user_id, network)
    tracked_validators_data = [DefiValidatorData(model.validator_vote_pubkey, model.display_name) for model in
                          tracked_validator_models]
    validator_adapter = get_validator_adapter(network, tracked_validators_data)
    chart_data = get_validator_chart_data(validator_adapter)
    modal_form_data = _get_delete_modal_form_data(tracked_validator_models)
    if not form:
        form = form_cls(current_user_id, network)
    return render(request, 'validators.html', {'data': chart_data, 'form': form, 'network': network, 'modal_data': modal_form_data})


def wallets(request, network=None):
    if _is_invalid_network(network):
        return defi_index(request)
    current_user_id = request.user.username
    form = None
    form_cls = get_wallet_form_cls(network)
    if request.method == 'POST':
        form = form_cls(current_user_id, network, request.POST)
        if form.is_valid():
            form.save()
    tracked_wallet_models = _get_wallet_records(current_user_id, network)
    tracked_wallets_data = [DefiWalletData(model.wallet_pubkey, model.display_name, model.staked) for model in tracked_wallet_models]
    portfolio_adapter = get_portfolio_adapter(network, tracked_wallets_data)
    table_data = portfolio_adapter.composite_data
    modal_form_data = _get_delete_modal_form_data(tracked_wallet_models)
    if not form:
        form = form_cls(current_user_id, network)
    return render(request, 'wallets.html', {'data': table_data, 'form': form, 'network': network, 'modal_data': modal_form_data})


def delete_validator(request, network=None):
    if not request.method == 'POST':
        return redirect('validators', network=network, permanent=True)
    pk = request.POST['modelpk']
    validator = _get_model_by_pk(DefiValidator, pk)
    if not _is_authenticated_to_delete(validator, request) or not _is_correct_network(validator, network):
        return redirect('validators', network=network, permanent=True)
    validator.delete()
    return redirect('validators', network=network, permanent=True)


def delete_wallet(request, network=None):
    if not request.method == 'POST':
        return redirect('wallets', network=network, permanent=True)
    pk = request.POST['modelpk']
    wallet = _get_model_by_pk(DefiWallet, pk)
    if not _is_authenticated_to_delete(wallet, request) or not _is_correct_network(wallet, network):
        return redirect('wallets', network=network, permanent=True)
    wallet.delete()
    return redirect('wallets', network=network, permanent=True)


def _is_invalid_network(network):
    return network not in SUPPORTED_DEFI_NETWORKS

def _get_validator_records(user_id, network):
    return DefiValidator.objects.filter(user_id=user_id, defi_network=network)


def _get_wallet_records(current_user_id, network):
    return DefiWallet.objects.filter(user_id=current_user_id, defi_network=network)


def _get_delete_modal_form_data(defi_models):
    return [{'key': model.pk, 'display_name': model.display_name} for model in defi_models]


def _is_authenticated_to_delete(model, request):
    current_user_id = request.user.username
    return model and model.user_id == current_user_id


def _is_correct_network(model, network):
    return model.defi_network == network.lower()


def _get_model_by_pk(model_cls, pk):
    model_query = model_cls.objects.filter(pk=pk)
    return model_query[0] if model_query else None
