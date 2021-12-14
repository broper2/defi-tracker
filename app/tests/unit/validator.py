from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from app.models import SolanaValidator
from .constants import MOCK_VALIDATOR_DATA

@patch('app.external.solana_network.SolanaNetworkInterface._fetch_validator_data', new=lambda *args, **kwargs: MOCK_VALIDATOR_DATA)
@patch('app.external.solana_network.SolanaNetworkInterface.vote_account_keys', ['pubkey1', 'pubkey2', 'pubkey3'])
class ValidatorTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1', password='pswd1')
        cls.user3 = User.objects.create(username='user3', password='pswd3')
        cls.validator1 = SolanaValidator.objects.create(validator_vote_pubkey='pubkey1', display_name='name1', user_id='user1')
        cls.validator1 = SolanaValidator.objects.create(validator_vote_pubkey='pubkey2', display_name='name2', user_id='user2')

    def test_get_user_with_validators(self):
        self.client.force_login(self.user1)
        response = self.client.get('/validators')
        self.assertEqual([1.01041, 1.01081, 1.01064, 1.01008, 1.00141], response.context['data']['datasets'][0]['data'])
        self.assertEqual('name1', response.context['data']['datasets'][0]['label'])
        self.assertEqual([254, 255, 256, 257, 258], response.context['data']['labels'])
        self.assertIn('form', response.context)

    def test_get_user_with_no_validators(self):
        self.client.force_login(self.user3)
        response = self.client.get('/validators')
        self.assertEqual({}, response.context['data'])
        self.assertIn('form', response.context)

    def test_post_user_valid_validator(self):
        self.client.force_login(self.user1)
        response = self.client.post('/validators', {'validator_vote_pubkey': 'pubkey3', 'display_name':'name3', 'user_id':'user1'})
        self.assertEqual([1.01041, 1.01081, 1.01064, 1.01008, 1.00141], response.context['data']['datasets'][0]['data'])
        self.assertEqual('name1', response.context['data']['datasets'][0]['label'])
        self.assertEquals([1.01755, 1.018, 1.01764, 1.01654, 1.00232], response.context['data']['datasets'][1]['data'])
        self.assertEquals('name3', response.context['data']['datasets'][1]['label'])
        self.assertEqual([254, 255, 256, 257, 258], response.context['data']['labels'])
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].errors)

    def test_post_user_invalid_validator(self):
        self.client.force_login(self.user1)
        response = self.client.post('/validators', {'validator_vote_pubkey': 'invalid_pubkey', 'display_name':'name4', 'user_id':'user1'})
        self.assertEqual([1.01041, 1.01081, 1.01064, 1.01008, 1.00141], response.context['data']['datasets'][0]['data'])
        self.assertEqual('name1', response.context['data']['datasets'][0]['label'])
        self.assertEqual([254, 255, 256, 257, 258], response.context['data']['labels'])
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)
