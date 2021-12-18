import os

from requests.exceptions import HTTPError

from solana.rpc.api import Client

from app.config.constants import SOLANA_RPC_KEYS, SOLANA_VALIDATOR_HISTORY_LENGTH
from app.exceptions.solana_external import SolanaExternalNetworkException
from app.utils.error_handling import handle_exceptions
from app.utils.timed_cache import timed_cache


class SolanaNetworkInterface(object):

    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self, initial_validator_data_cache=True):
        self.solana_rpc_url = os.environ['SOLANA_RPC_URL']
        self.solana_rpc_client = Client(self.solana_rpc_url)
        if initial_validator_data_cache:
            self._get_cluster_validator_data()

    @property
    def vote_account_keys(self):
        cluster_validator_data = self._get_cluster_validator_data()
        return [self.get_vote_pubkey(validator_data) for validator_data in cluster_validator_data]

    def get_cluster_validator_data(self):
        return self._get_cluster_validator_data()

    def get_account_balance(self, pubkey):
        return self._get_account_balance(pubkey)

    def is_valid_account_pubkey(self, pubkey):
        return self._is_connected() and self._is_active_pubkey(pubkey)

    def get_commission(self, validator_data):
        return self._get_commission(validator_data)

    def get_epoch_credits(self, validator_data):
        return self._get_epoch_credits(validator_data)

    def get_vote_pubkey(self, validator_data):
        return self._get_vote_pubkey(validator_data)

    @property
    def last_epoch(self):
        return self._get_last_epoch()

    @property
    def epoch_credit_count(self):
        return SOLANA_VALIDATOR_HISTORY_LENGTH

    @handle_exceptions(SolanaExternalNetworkException, HTTPError)
    def _get_cluster_validator_data(self):
        cluster_validator_data = self._get_current_validator_data()
        for validator_data in cluster_validator_data:
            validator_data[SOLANA_RPC_KEYS['epoch_credits']] = self._normalize_epoch_credits_length(
                validator_data[SOLANA_RPC_KEYS['epoch_credits']]
            )
        return cluster_validator_data

    @handle_exceptions(SolanaExternalNetworkException, KeyError)
    def _get_current_validator_data(self):
        data = self._fetch_and_cache_validator_data()
        return data[SOLANA_RPC_KEYS['result']][SOLANA_RPC_KEYS['current']]

    @timed_cache(hours=1)
    def _fetch_and_cache_validator_data(self):
        return self._fetch_validator_data()

    @handle_exceptions(SolanaExternalNetworkException, HTTPError)
    def _fetch_validator_data(self):
        return self.solana_rpc_client.get_vote_accounts()

    @handle_exceptions(SolanaExternalNetworkException, HTTPError, KeyError)
    def _get_account_balance(self, pubkey):
        return self.solana_rpc_client.get_balance(pubkey)[SOLANA_RPC_KEYS['result']][SOLANA_RPC_KEYS['value']]

    @handle_exceptions(SolanaExternalNetworkException, HTTPError)
    def _is_connected(self):
        return self.solana_rpc_client.is_connected()

    def _is_active_pubkey(self, pubkey):
        account_info = self._get_account_info(pubkey)
        return account_info and SOLANA_RPC_KEYS['error'] not in account_info

    @handle_exceptions(SolanaExternalNetworkException, HTTPError)
    def _get_account_info(self, pubkey):
        return self.solana_rpc_client.get_account_info(pubkey)

    @timed_cache(minutes=1)
    def _get_last_epoch(self):
        return self._request_last_epoch()

    @handle_exceptions(SolanaExternalNetworkException, HTTPError, KeyError)
    def _request_last_epoch(self):
        return self.solana_rpc_client.get_epoch_info()[SOLANA_RPC_KEYS['result']][SOLANA_RPC_KEYS['epoch']]

    @staticmethod
    def _normalize_epoch_credits_length(history):
        return [[0, 0, 0]] * (SOLANA_VALIDATOR_HISTORY_LENGTH - len(history)) + history

    @staticmethod
    @handle_exceptions(SolanaExternalNetworkException, KeyError)
    def _get_commission(validator_data):
        return validator_data[SOLANA_RPC_KEYS['commission']]

    @staticmethod
    @handle_exceptions(SolanaExternalNetworkException, KeyError)
    def _get_epoch_credits(validator_data):
        return validator_data[SOLANA_RPC_KEYS['epoch_credits']]

    @staticmethod
    @handle_exceptions(SolanaExternalNetworkException, KeyError)
    def _get_vote_pubkey(validator_data):
        return validator_data[SOLANA_RPC_KEYS['vote_pubkey']]
