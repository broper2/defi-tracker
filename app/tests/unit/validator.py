from unittest.mock import patch
from django.test import TestCase
from django.contrib.auth.models import User
from app.models import DefiValidator
from .constants import MOCK_VALIDATOR_DATA

@patch('app.external.solana_network.SolanaNetworkInterface._fetch_and_cache_validator_data', new=lambda *args, **kwargs: MOCK_VALIDATOR_DATA)
@patch('app.external.solana_network.SolanaNetworkInterface._request_last_epoch', new=lambda *args, **kwargs: 258)
class SolanaValidatorTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user1 = User.objects.create(username='user1', password='pswd1')
        cls.user3 = User.objects.create(username='user3', password='pswd3')
        cls.validator1 = DefiValidator.objects.create(validator_vote_pubkey='pubkey1', display_name='name1', user_id='user1')
        cls.validator2 = DefiValidator.objects.create(validator_vote_pubkey='pubkey2', display_name='name2', user_id='user2')

    def test_get_user_with_validators(self):
        self.client.force_login(self.user1)
        response = self.client.get('/solana/validators')
        self.assertEqual([0.0, 0.0, 2.076923, 2.7, 1.421053], response.context['data']['datasets'][0]['data'])
        self.assertEqual('name1', response.context['data']['datasets'][0]['label'])
        self.assertEqual([254, 255, 256, 257, 258], response.context['data']['labels'])
        self.assertIn('form', response.context)

    def test_get_user_with_no_validators(self):
        self.client.force_login(self.user3)
        response = self.client.get('/solana/validators')
        self.assertEqual({'datasets': [], 'labels': []}, response.context['data'])
        self.assertIn('form', response.context)

    def test_post_user_valid_validator(self):
        self.client.force_login(self.user1)
        response = self.client.post('/solana/validators', {'validator_vote_pubkey': 'pubkey3', 'display_name':'name3', 'user_id':'user1'})
        self.assertEqual([0.0, 0.0, 2.076923, 2.7, 1.421053], response.context['data']['datasets'][0]['data'])
        self.assertEqual('name1', response.context['data']['datasets'][0]['label'])
        self.assertEquals([3.0, 0.857143, 0.461538, -0.3, 1.263158], response.context['data']['datasets'][1]['data'])
        self.assertEquals('name3', response.context['data']['datasets'][1]['label'])
        self.assertEqual([254, 255, 256, 257, 258], response.context['data']['labels'])
        self.assertIn('form', response.context)
        self.assertFalse(response.context['form'].errors)

    def test_post_user_invalid_validator(self):
        self.client.force_login(self.user1)
        response = self.client.post('/solana/validators', {'validator_vote_pubkey': 'invalid_pubkey', 'display_name':'name4', 'user_id':'user1'})
        self.assertEqual([0.0, 0.0, 2.076923, 2.7, 1.421053], response.context['data']['datasets'][0]['data'])
        self.assertEqual('name1', response.context['data']['datasets'][0]['label'])
        self.assertEqual([254, 255, 256, 257, 258], response.context['data']['labels'])
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

    def test_post_delete_validator(self):
        self.client.force_login(self.user1)
        self.assertEquals(1, len(DefiValidator.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/solana/validators/delete', {'modelpk': self.validator1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(0, len(DefiValidator.objects.filter(user_id=self.user1.username)))

    def test_post_delete_missing_validator(self):
        self.client.force_login(self.user1)
        self.assertEquals(1, len(DefiValidator.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/solana/validators/delete', {'modelpk': 1234567})
        self.assertEqual(301, response.status_code)
        self.assertEquals(1, len(DefiValidator.objects.filter(user_id=self.user1.username)))

    def test_post_delete_validator_unauthenticated(self):
        self.client.force_login(self.user3)
        self.assertEquals(1, len(DefiValidator.objects.filter(user_id=self.user1.username)))
        self.assertEquals(0, len(DefiValidator.objects.filter(user_id=self.user3.username)))
        response = self.client.post('/solana/validators/delete', {'modelpk': self.validator1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(1, len(DefiValidator.objects.filter(user_id=self.user1.username)))
        self.assertEquals(0, len(DefiValidator.objects.filter(user_id=self.user3.username)))

    def test_post_delete_validator_incorrect_network(self):
        self.client.force_login(self.user1)
        self.assertEquals(1, len(DefiValidator.objects.filter(user_id=self.user1.username)))
        response = self.client.post('/ethereum/validators/delete', {'modelpk': self.validator1.pk})
        self.assertEqual(301, response.status_code)
        self.assertEquals(1, len(DefiValidator.objects.filter(user_id=self.user1.username)))
