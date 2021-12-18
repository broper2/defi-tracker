from django.db import models


class SolanaValidator(models.Model):

    validator_vote_pubkey = models.CharField(max_length=100)
    display_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.user_id} tracking validator {self.display_name}'


class SolanaWallet(models.Model):

    wallet_pubkey = models.CharField(max_length=100)
    display_name = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    staked = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user_id} tracking wallet {self.display_name}'