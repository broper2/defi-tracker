from django import forms
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
        self.solana_network_interface = SolanaNetworkInterface.instance()
        self.valid_pubkeys = self.solana_network_interface.vote_account_keys

    def clean(self):
        super().clean()
        if not self.cleaned_data['validator_vote_pubkey'] in self.valid_pubkeys:
            raise ValidationError('Invalid vote account pubkey')
        return self.cleaned_data

    class Meta:
        model = DefiValidator
        fields = ['validator_vote_pubkey', 'display_name', 'user_id']


class SolanaValidatorForm(DefiValidatorForm):

    pass


def get_validator_form_cls(network):
    validator_form_map = {
        'SOLANA': SolanaValidatorForm,
    }
    return validator_form_map[network.upper()]


class DefiWalletForm(forms.ModelForm):

    wallet_pubkey = forms.CharField(max_length=100)
    display_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=50, widget=forms.HiddenInput())
    staked = forms.BooleanField(required=False) #TODO should be disabled on ethereum - use constants POS
    defi_network = forms.CharField(max_length=50, disabled=True)

    def __init__(self, user, network, *args, **kwargs):
        super(DefiWalletForm, self).__init__(*args, **kwargs)
        self.initial['user_id'] = user
        self.initial['defi_network'] = network
        self.interface = self.network_interface_cls.instance()

    @property
    def network_interface_cls(self):
        raise NotImplementedError

    def clean(self):
        super().clean()
        if not self.interface.is_valid_account_pubkey(self.cleaned_data['wallet_pubkey']):
            raise ValidationError('Invalid wallet pubkey')
        return self.cleaned_data

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
