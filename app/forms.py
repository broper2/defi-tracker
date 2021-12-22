from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .external.ethereum_network import EthereumNetworkInterface
from .external.solana_network import SolanaNetworkInterface
from .models import DefiValidator, DefiWallet


class DefiValidatorForm(forms.ModelForm):

    validator_vote_pubkey = forms.CharField(max_length=100)
    display_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=50, widget=forms.HiddenInput())
    defi_network = forms.CharField(max_length=50, disabled=True)

    def __init__(self, user, network, *args, **kwargs):
        super(DefiValidatorForm, self).__init__(*args, **kwargs)
        self.initial['user_id'] = user
        self.initial['defi_network'] = network
        self.interface = self.network_interface_cls.instance()
        self.valid_pubkeys = self.interface.vote_account_keys
        self.initial['user_id'] = user
        self.initial['defi_network'] = network
        self.fields['validator_vote_pubkey'].widget.attrs['class'] = 'form-control'
        self.fields['display_name'].widget.attrs['class'] = 'form-control'
        self.fields['user_id'].widget.attrs['class'] = 'form-control'
        self.fields['defi_network'].widget.attrs['class'] = 'form-control'

    def clean(self):
        super().clean()
        if not self.cleaned_data['validator_vote_pubkey'] in self.valid_pubkeys:
            raise ValidationError('Invalid vote account pubkey')
        return self.cleaned_data

    @property
    def network_interface_cls(self):
        raise NotImplementedError

    class Meta:
        model = DefiValidator
        fields = ['validator_vote_pubkey', 'display_name', 'user_id']


class SolanaValidatorForm(DefiValidatorForm):

    @property
    def network_interface_cls(self):
        return SolanaNetworkInterface


def get_validator_form_cls(network):
    validator_form_map = {
        'SOLANA': SolanaValidatorForm,
    }
    return validator_form_map[network.upper()]


class DefiWalletForm(forms.ModelForm):

    wallet_pubkey = forms.CharField(max_length=100)
    display_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=50, widget=forms.HiddenInput())
    staked = forms.BooleanField(required=False)
    defi_network = forms.CharField(max_length=50, disabled=True)

    def __init__(self, user, network, *args, **kwargs):
        super(DefiWalletForm, self).__init__(*args, **kwargs)
        self.initial['user_id'] = user
        self.initial['defi_network'] = network
        self.interface = self.network_interface_cls.instance(initial_validator_data_cache=False)
        self.fields['wallet_pubkey'].widget.attrs['class'] = 'form-control'
        self.fields['display_name'].widget.attrs['class'] = 'form-control'
        self.fields['user_id'].widget.attrs['class'] = 'form-control'
        self.fields['staked'].widget.attrs['class'] = 'mt-2'
        self.fields['defi_network'].widget.attrs['class'] = 'form-control'

    @property
    def network_interface_cls(self):
        raise NotImplementedError

    def clean(self):
        super().clean()
        if self._is_invalid_pubkey(self.cleaned_data['wallet_pubkey']):
            raise ValidationError('Invalid wallet pubkey')
        return self.cleaned_data

    def _is_invalid_pubkey(self, pubkey):
        return not self.interface.is_valid_account_pubkey(pubkey)


    class Meta:
        model = DefiWallet
        fields = ['wallet_pubkey', 'display_name', 'staked', 'user_id', 'defi_network']


class SolanaWalletForm(DefiWalletForm):

    @property
    def network_interface_cls(self):
        return SolanaNetworkInterface


class EthereumWalletForm(DefiWalletForm):

    staked = forms.BooleanField(required=False, disabled=True)

    @property
    def network_interface_cls(self):
        return EthereumNetworkInterface


def get_wallet_form_cls(network):
    validator_form_map = {
        'SOLANA': SolanaWalletForm,
        'ETHEREUM': EthereumWalletForm,
    }
    return validator_form_map[network.upper()]


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
