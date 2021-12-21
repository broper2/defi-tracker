from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from app.models import DefiWallet


def mock_is_active_pubkey(interface, pubkey):
    return pubkey != 'invalid_pubkey'


@patch('app.external.binance_api.BinanceApiInterface._get_sol_price', new=lambda *args, **kwargs: 1.545454)
@patch('app.external.solana_network.SolanaNetworkInterface._get_account_balance', new=lambda *args, **kwargs: 2000000000)
@patch('app.external.solana_network.SolanaNetworkInterface._is_connected', new=lambda *args, **kwargs: True)
class WalletTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1', password='pswd1')
        cls.user3 = User.objects.create(username='user3', password='pswd3')
        cls.wallet1 = DefiWallet.objects.create(wallet_pubkey='pubkey1', display_name='name1', user_id='user1', staked=True)
        cls.wallet2 = DefiWallet.objects.create(wallet_pubkey='pubkey2', display_name='name2', user_id='user2', staked=False)

    @patch('app.external.solana_network.SolanaNetworkInterface._is_active_pubkey', new=mock_is_active_pubkey)
    def test_get_user_with_wallets(self):
        self.client.force_login(self.user1)
        response = self.client.get('/wallets')
        expected_data = [
            {'display_name': self.wallet1.display_name, 'sol': 2.0, 'usd': 3.09, 'staked': 'True'},
            {'display_name': 'Portfolio Total', 'sol': 2.0, 'usd': 3.09, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)

    @patch('app.external.solana_network.SolanaNetworkInterface._is_active_pubkey', new=mock_is_active_pubkey)
    def test_get_user_without_wallets(self):
        self.client.force_login(self.user3)
        response = self.client.get('/wallets')
        self.assertEquals([{'display_name': 'Portfolio Total', 'sol': 0, 'usd': 0, 'staked': 'N/A'}], response.context['data'])
        self.assertIn('form', response.context)

    @patch('app.external.solana_network.SolanaNetworkInterface._is_active_pubkey', new=mock_is_active_pubkey)
    def test_post_valid_wallet_pubkey(self):
        self.client.force_login(self.user1)
        response = self.client.post('/wallets', {'wallet_pubkey': 'pubkey3', 'display_name': 'name3', 'user_id': 'user1', 'staked': False})
        expected_data = [
            {'display_name': self.wallet1.display_name, 'sol': 2.0, 'usd': 3.09, 'staked': 'True'},
            {'display_name': 'name3', 'sol': 2.0, 'usd': 3.09, 'staked': 'False'},
            {'display_name': 'Portfolio Total', 'sol': 4, 'usd': 6.18, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].errors)

    @patch('app.external.solana_network.SolanaNetworkInterface._is_active_pubkey', new=mock_is_active_pubkey)
    def test_post_invalid_wallet_pubkey(self):
        self.client.force_login(self.user1)
        response = self.client.post('/wallets', {'wallet_pubkey': 'invalid_pubkey', 'display_name': 'name4', 'user_id': 'user1'})
        expected_data = [
            {'display_name': self.wallet1.display_name, 'sol': 2.0, 'usd': 3.09, 'staked': 'True'},
            {'display_name': 'Portfolio Total', 'sol': 2.0, 'usd': 3.09, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
