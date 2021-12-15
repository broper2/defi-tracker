import collections
from requests.exceptions import RequestException

from app.adapters.solana_account import SolanaAccountDataAdapter
from app.adapters.solana_validator import SolanaValidatorDataAdapter
from app.config.constants import SOLANA_PRODUCTION_API_URL, SOLANA_RPC_KEYS
from app.exceptions.solana_external import SolanaExternalNetworkException
from app.utils.timed_cache import timed_cache
from solana.rpc.api import Client


SolanaQueryData = collections.namedtuple('SolanaQueryData', ['key', 'display_name'])


class SolanaNetworkInterface(object):

    def __init__(self, initial_validator_data_cache=True):
        self.solana_rpc_client = Client(SOLANA_PRODUCTION_API_URL)
        if initial_validator_data_cache:
            self._request_validator_data()

    @property
    def vote_account_keys(self):
        solana_validator_data = self._request_validator_data()
        return [account[SOLANA_RPC_KEYS['vote_pubkey']] for account in solana_validator_data]

    def get_wrapped_validator_data(self, validator_query_data):
        solana_validator_data = self._request_validator_data()
        zipped_data = self._zip_query_and_validator_data(validator_query_data, solana_validator_data)
        adapter_data = [(query_data.display_name, validator_data) for query_data, validator_data in zipped_data]
        return [SolanaValidatorDataAdapter(*data) for data in adapter_data] #TODO avoid explicit class name

    def get_wrapped_account_data(self, query_data):
        account_balance = self._get_account_balance(query_data.key)
        return SolanaAccountDataAdapter(query_data.display_name, **account_balance['result']) #TODO avoid explicit class name

    def is_valid_account_pubkey(self, pubkey):
        return self._is_connected() and self._is_active_pubkey(pubkey)

    def _request_validator_data(self):
        try:
            return self._fetch_and_cache_validator_data()
        except RequestException:
            raise SolanaExternalNetworkException('Error in fetching validator data from Solana network')

    @timed_cache(hours=1)
    def _fetch_and_cache_validator_data(self):
        return self.solana_rpc_client.get_vote_accounts()[SOLANA_RPC_KEYS['result']][SOLANA_RPC_KEYS['current']]

    @staticmethod
    def _zip_query_and_validator_data(validator_query_data, solana_validator_data):
        zipped_data = []
        validator_query_pubkeys = [query_data.key for query_data in validator_query_data]
        for validator_data in solana_validator_data:
            vote_pubkey = validator_data[SOLANA_RPC_KEYS['vote_pubkey']]
            if vote_pubkey in validator_query_pubkeys:
                zipped_data.append((validator_query_data[validator_query_pubkeys.index(vote_pubkey)], validator_data))
        return zipped_data

    def _get_account_balance(self, pubkey):
        try:
            return self.solana_rpc_client.get_balance(pubkey)
        except RequestException:
            raise SolanaExternalNetworkException('Error in fetching account balance from Solana network')

    def _is_connected(self):
        try:
            return self.solana_rpc_client.is_connected()
        except RequestException:
            return False

    def _is_active_pubkey(self, pubkey):
        account_info = self._get_account_info(pubkey)
        return account_info and SOLANA_RPC_KEYS['error'] not in account_info

    def _get_account_info(self, pubkey):
        try:
            return self.solana_rpc_client.get_account_info(pubkey)
        except RequestException:
            raise SolanaExternalNetworkException('Error in fetching account information from Solana network')
