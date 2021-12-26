from unittest.mock import patch, AsyncMock
from django.test import TestCase
from django.contrib.auth.models import User
from app.models import DefiWallet


def mock_is_active_pubkey(interface, pubkey):
    return pubkey != 'invalid_pubkey'


@patch('app.external.sync_interfaces.binance_api.BinanceApiInterface._get_sol_price', new=lambda *args, **kwargs: 1.545454)
@patch('app.external.async_interfaces.solana_network_async.AsyncSolanaNetworkInterface._get_account_balance')
@patch('app.external.sync_interfaces.solana_network.SolanaNetworkInterface._is_connected', new=lambda *args, **kwargs: True)
@patch('app.external.sync_interfaces.solana_network.SolanaNetworkInterface._is_active_pubkey', new=mock_is_active_pubkey)
class SolanaWalletTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1', password='pswd1')
        cls.user3 = User.objects.create(username='user3', password='pswd3')
        cls.wallet1 = DefiWallet.objects.create(wallet_pubkey='pubkey1', display_name='name1', user_id='user1', staked=True, defi_network='solana')
        cls.wallet2 = DefiWallet.objects.create(wallet_pubkey='pubkey2', display_name='name2', user_id='user2', staked=False, defi_network='solana')
        cls.wallet2 = DefiWallet.objects.create(wallet_pubkey='pubkey21', display_name='name21', user_id='user1', staked=False, defi_network='ethereum')

    def test_get_user_with_wallets(self, mock_balance):
        mock_balance.side_effect = AsyncMock(return_value=2000000000)
        self.client.force_login(self.user1)
        response = self.client.get('/solana/wallets')
        expected_data = [
            {'display_name': self.wallet1.display_name, 'token': 2.0, 'usd': 3.09, 'staked': 'True'},
            {'display_name': 'Portfolio Total', 'token': 2.0, 'usd': 3.09, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)

    def test_get_user_without_wallets(self, mock_balance):
        mock_balance.side_effect = AsyncMock(return_value=2000000000)
        self.client.force_login(self.user3)
        response = self.client.get('/solana/wallets')
        self.assertEquals([{'display_name': 'Portfolio Total', 'token': 0, 'usd': 0, 'staked': 'N/A'}], response.context['data'])
        self.assertIn('form', response.context)

    def test_post_valid_wallet_pubkey(self, mock_balance):
        mock_balance.side_effect = AsyncMock(return_value=2000000000)
        self.client.force_login(self.user1)
        response = self.client.post('/solana/wallets',
                                    {'wallet_pubkey': 'pubkey3', 'display_name': 'name3', 'user_id': 'user1',
                                     'staked': False, 'defi_network': 'solana'})
        expected_data = [
            {'display_name': self.wallet1.display_name, 'token': 2.0, 'usd': 3.09, 'staked': 'True'},
            {'display_name': 'name3', 'token': 2.0, 'usd': 3.09, 'staked': 'False'},
            {'display_name': 'Portfolio Total', 'token': 4, 'usd': 6.18, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)
        self.assertFalse(response.context['error'])

    def test_post_invalid_wallet_pubkey(self, mock_balance):
        mock_balance.side_effect = AsyncMock(return_value=2000000000)
        self.client.force_login(self.user1)
        response = self.client.post('/solana/wallets', {'wallet_pubkey': 'invalid_pubkey', 'display_name': 'name4', 'user_id': 'user1'})
        expected_data = [
            {'display_name': self.wallet1.display_name, 'token': 2.0, 'usd': 3.09, 'staked': 'True'},
            {'display_name': 'Portfolio Total', 'token': 2.0, 'usd': 3.09, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)
        self.assertTrue('Invalid wallet pubkey', response.context['error'])

    def test_post_delete_wallet(self, mock_balance):
        self.client.force_login(self.user1)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/solana/wallets/delete', {'modelpk': self.wallet1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(1, len(DefiWallet.objects.filter(user_id=self.user1.username)))

    def test_post_delete_missing_wallet(self, mock_balance):
        self.client.force_login(self.user1)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/solana/wallets/delete', {'modelpk': 1234567})
        self.assertEqual(301, response.status_code)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))

    def test_post_delete_wallet_unauthenticated(self, mock_balance):
        self.client.force_login(self.user3)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        self.assertEquals(0, len(DefiWallet.objects.filter(user_id=self.user3.username)))
        response = self.client.post('/solana/wallets/delete', {'modelpk': self.wallet1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        self.assertEquals(0, len(DefiWallet.objects.filter(user_id=self.user3.username)))

    def test_post_delete_wallet_incorrect_network(self, mock_balance):
        self.client.force_login(self.user1)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/ethereum/wallets/delete', {'modelpk': self.wallet1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))


@patch('app.external.sync_interfaces.binance_api.BinanceApiInterface._get_eth_price', new=lambda *args, **kwargs: 1.545454)
@patch('app.external.sync_interfaces.ethereum_network.EthereumNetworkInterface.get_account_balance', new=lambda *args, **kwargs: 2 * (10**18))
@patch('app.external.sync_interfaces.ethereum_network.EthereumNetworkInterface.is_valid_account_pubkey', new=mock_is_active_pubkey)
class EthereumWalletTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1', password='pswd1')
        cls.user3 = User.objects.create(username='user3', password='pswd3')
        cls.wallet1 = DefiWallet.objects.create(wallet_pubkey='pubkey1', display_name='name1', user_id='user1', staked=False, defi_network='ethereum')
        cls.wallet2 = DefiWallet.objects.create(wallet_pubkey='pubkey2', display_name='name2', user_id='user2', staked=False, defi_network='ethereum')
        cls.wallet2 = DefiWallet.objects.create(wallet_pubkey='pubkey21', display_name='name21', user_id='user1', staked=True, defi_network='solana')

    def test_get_user_with_wallets(self):
        self.client.force_login(self.user1)
        response = self.client.get('/ethereum/wallets')
        expected_data = [
            {'display_name': self.wallet1.display_name, 'token': 2.0, 'usd': 3.09, 'staked': 'False'},
            {'display_name': 'Portfolio Total', 'token': 2.0, 'usd': 3.09, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)

    def test_get_user_without_wallets(self):
        self.client.force_login(self.user3)
        response = self.client.get('/ethereum/wallets')
        self.assertEquals([{'display_name': 'Portfolio Total', 'token': 0, 'usd': 0, 'staked': 'N/A'}], response.context['data'])
        self.assertIn('form', response.context)

    def test_post_valid_wallet_pubkey(self):
        self.client.force_login(self.user1)
        response = self.client.post('/ethereum/wallets',
                                    {'wallet_pubkey': 'pubkey3', 'display_name': 'name3', 'user_id': 'user1',
                                     'staked': False, 'defi_network': 'ethereum'})
        expected_data = [
            {'display_name': self.wallet1.display_name, 'token': 2.0, 'usd': 3.09, 'staked': 'False'},
            {'display_name': 'name3', 'token': 2.0, 'usd': 3.09, 'staked': 'False'},
            {'display_name': 'Portfolio Total', 'token': 4, 'usd': 6.18, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)
        self.assertFalse(response.context['error'])

    def test_post_invalid_wallet_pubkey(self):
        self.client.force_login(self.user1)
        response = self.client.post('/ethereum/wallets',
                                    {'wallet_pubkey': 'invalid_pubkey', 'display_name': 'name4', 'user_id': 'user1',
                                     'staked': False, 'defi_network': 'ethereum'})
        expected_data = [
            {'display_name': self.wallet1.display_name, 'token': 2.0, 'usd': 3.09, 'staked': 'False'},
            {'display_name': 'Portfolio Total', 'token': 2.0, 'usd': 3.09, 'staked': 'N/A'},
        ]
        self.assertEquals(expected_data, response.context['data'])
        self.assertIn('form', response.context)
        self.assertTrue('Invalid wallet pubkey', response.context['error'])

    def test_post_delete_wallet(self):
        self.client.force_login(self.user1)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/ethereum/wallets/delete', {'modelpk': self.wallet1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(1, len(DefiWallet.objects.filter(user_id=self.user1.username)))

    def test_post_delete_missing_wallet(self):
        self.client.force_login(self.user1)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/ethereum/wallets/delete', {'modelpk': 1234567})
        self.assertEqual(301, response.status_code)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))

    def test_post_delete_wallet_unauthenticated(self):
        self.client.force_login(self.user3)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        self.assertEquals(0, len(DefiWallet.objects.filter(user_id=self.user3.username)))
        response = self.client.post('/ethereum/wallets/delete', {'modelpk': self.wallet1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        self.assertEquals(0, len(DefiWallet.objects.filter(user_id=self.user3.username)))

    def test_post_delete_wallet_incorrect_network(self):
        self.client.force_login(self.user1)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/solana/wallets/delete', {'modelpk': self.wallet1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(2, len(DefiWallet.objects.filter(user_id=self.user1.username)))
