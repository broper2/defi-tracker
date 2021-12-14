import collections

from app.adapters.solana_account import SolanaAccountDataAdapter
from app.adapters.solana_validator import SolanaValidatorDataAdapter
from app.config.constants import SOLANA_PRODUCTION_API_URL
from app.config.constants import SOLANA_RPC_KEYS
from app.exceptions.solana_external import SolanaExternalNetworkException
from app.utils.timed_cache import timed_cache
from solana.rpc.api import Client


SolanaQueryData = collections.namedtuple('SolanaQueryData', ['key', 'display_name'])


class SolanaNetworkInterface(object):

    def __init__(self, cache_validator_data=True):
        self.solana_rpc_client = Client(SOLANA_PRODUCTION_API_URL)
        self._vote_account_keys = []
        if cache_validator_data:
            self._cache_vote_account_data()

    @property
    def vote_account_keys(self):
        return self._vote_account_keys

    @vote_account_keys.setter
    def vote_account_keys(self, keys):
        self._vote_account_keys = keys

    def _cache_vote_account_data(self):
        try:
            data = self._fetch_validator_data()
            self.vote_account_keys = [account[SOLANA_RPC_KEYS['vote_pubkey']] for account in data]
        except Exception:
            raise SolanaExternalNetworkException('Error in initial load of validator data from Solana network')

    def _is_connected(self):
        return self.solana_rpc_client.is_connected()

    def _get_validator_data(self):
        try:
            return self._fetch_validator_data()
        except Exception:
            raise SolanaExternalNetworkException('Error in fetching validator data from Solana network')

    @timed_cache(hours=1)
    def _fetch_validator_data(self):
        return self.solana_rpc_client.get_vote_accounts()['result']['current']

    def get_wrapped_validator_data(self, validator_query_data):
        validator_data = self._get_validator_data()
        adapter_data = []
        for query_data in validator_query_data:
            record_data = self._get_validator_data_by_votekey(query_data.key, validator_data)
            adapter_data.append((query_data.display_name, record_data))
        return [SolanaValidatorDataAdapter(*data) for data in adapter_data]

    @staticmethod
    def _get_validator_data_by_votekey(vote_pubkey, validator_data):
        for data in validator_data:
            if data['votePubkey'] == vote_pubkey:
                return data

    def _get_account_balance(self, pubkey):
        return self.solana_rpc_client.get_balance(pubkey)

    def get_wrapped_account_data(self, query_data):
        try:
            account_balance = self._get_account_balance(query_data.key)
        except Exception:
            raise SolanaExternalNetworkException('Error in fetching account balance from Solana network')
        return SolanaAccountDataAdapter(query_data.display_name, **account_balance['result'])

    def _is_active_pubkey(self, pubkey):
        account_info = self.solana_rpc_client.get_account_info(pubkey)
        return account_info and 'error' not in account_info

    def is_valid_account_pubkey(self, pubkey):
        try:
            return self._is_connected() and self._is_active_pubkey(pubkey)
        except Exception:
            return False
