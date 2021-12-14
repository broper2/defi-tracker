from django import forms
from django.core.exceptions import ValidationError

from .external.solana_network import SolanaNetworkInterface
from .models import SolanaValidator, SolanaWallet


class SolanaValidatorForm(forms.ModelForm):

    validator_vote_pubkey = forms.CharField(max_length=100)
    display_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=50, widget=forms.HiddenInput())

    def __init__(self, user, valid_pubkeys, *args, **kwargs):
        super(SolanaValidatorForm, self).__init__(*args, **kwargs)
        self.initial['user_id'] = user
        self.valid_pubkeys = valid_pubkeys

    def clean(self):
        super().clean()
        if not self.cleaned_data['validator_vote_pubkey'] in self.valid_pubkeys:
            raise ValidationError('Invalid vote account pubkey')
        return self.cleaned_data

    class Meta:
        model = SolanaValidator
        fields = ['validator_vote_pubkey', 'display_name', 'user_id']

class SolanaWalletForm(forms.ModelForm):

    wallet_pubkey = forms.CharField(max_length=100)
    display_name = forms.CharField(max_length=50)
    user_id = forms.CharField(max_length=50, widget=forms.HiddenInput())

    def __init__(self, user, *args, **kwargs):
        super(SolanaWalletForm, self).__init__(*args, **kwargs)
        self.initial['user_id'] = user
        self.solana_network_interface = SolanaNetworkInterface(cache_validator_data=False)

    def clean(self):
        super().clean()
        if not self.solana_network_interface.is_valid_account_pubkey(self.cleaned_data['wallet_pubkey']):
            raise ValidationError('Invalid account pubkey')
        return self.cleaned_data

    class Meta:
        model = SolanaWallet
        fields = ['wallet_pubkey', 'display_name', 'user_id']