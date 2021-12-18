import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render

from app.adapters.validator.builder import get_validator_adapter
from app.adapters.portfolio.builder import get_portfolio_adapter
from app.basetypes import SolanaAccountData, SolanaValidatorData
from app.forms import SolanaValidatorForm, SolanaWalletForm
from app.models import SolanaValidator, SolanaWallet
from app.utils.ui_data import get_validator_chart_data

logger = logging.getLogger(__name__)


NETWORK = 'SOLANA'  # If extended to other blockchain networks, this could be param in request - hardcoding for now

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
        form = SolanaValidatorForm(current_user_id, request.POST)
        if form.is_valid():
            form.save()
    tracked_validator_models = get_validator_records(current_user_id)
    tracked_validators = [SolanaValidatorData(model.validator_vote_pubkey, model.display_name) for model in
                          tracked_validator_models]
    validator_adapter = get_validator_adapter(NETWORK, tracked_validators)
    chart_data = get_validator_chart_data(validator_adapter)
    if not form:
        form = SolanaValidatorForm(current_user_id)
    return render(request, 'validators.html', {'data': chart_data, 'form': form})


def get_validator_records(user_id):
    return SolanaValidator.objects.filter(user_id=user_id)


def wallets(request): #TODO cleanup usages of wallet/account/portfolio
    current_user_id = request.user.username
    form = None
    if request.method == 'POST':
        form = SolanaWalletForm(current_user_id, request.POST)
        if form.is_valid():
            form.save()
    account_models = get_wallet_records(current_user_id)
    accounts = [SolanaAccountData(model.wallet_pubkey, model.display_name, model.staked) for model in account_models]
    portfolio_adapter = get_portfolio_adapter(NETWORK, accounts)
    table_data = portfolio_adapter.composite_data
    if not form:
        form = SolanaWalletForm(current_user_id)
    return render(request, 'wallets.html', {'data': table_data, 'form': form})


def get_wallet_records(user_id):
    return SolanaWallet.objects.filter(user_id=user_id)
