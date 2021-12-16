from requests.exceptions import RequestException

from app.config.constants import SOLANA_PRODUCTION_API_URL, SOLANA_RPC_KEYS
from app.exceptions.solana_external import SolanaExternalNetworkException
from app.utils.timed_cache import timed_cache
from solana.rpc.api import Client


class SolanaNetworkInterface(object):

    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def __init__(self, initial_validator_data_cache=True):
        self.solana_rpc_client = Client(SOLANA_PRODUCTION_API_URL)
        if initial_validator_data_cache:
            self._request_validator_data()

    @property
    def vote_account_keys(self):
        solana_validator_data = self._request_validator_data()
        return [account[SOLANA_RPC_KEYS['vote_pubkey']] for account in solana_validator_data]

    def get_validator_data(self):
        return self._request_validator_data()

    def get_account_balance(self, pubkey):
        return self._get_account_balance(pubkey)

    def is_valid_account_pubkey(self, pubkey):
        return self._is_connected() and self._is_active_pubkey(pubkey)

    @property
    def last_epoch(self):
        return self._get_last_epoch()

    def _request_validator_data(self):
        try:
            return self._fetch_and_cache_validator_data()
        except RequestException:
            raise SolanaExternalNetworkException('Error in fetching validator data from Solana network')

    @timed_cache(hours=1)
    def _fetch_and_cache_validator_data(self):
        return self.solana_rpc_client.get_vote_accounts()[SOLANA_RPC_KEYS['result']][SOLANA_RPC_KEYS['current']]

    def _get_account_balance(self, pubkey):
        try:
            return self.solana_rpc_client.get_balance(pubkey)[SOLANA_RPC_KEYS['result']]
        except RequestException:
            raise SolanaExternalNetworkException(f'Error in fetching account balance from Solana network - {pubkey}')
        except KeyError:
            raise SolanaExternalNetworkException(f'Error received from Solana network fetching account balance - {pubkey}')

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

    @timed_cache(minutes=1)
    def _get_last_epoch(self):
        try:
            return self.solana_rpc_client.get_epoch_info()[SOLANA_RPC_KEYS['result']][SOLANA_RPC_KEYS['epoch']]
        except RequestException:
            raise SolanaExternalNetworkException('RPC exception from Solana network fetching last epoch')
        except KeyError:
            raise SolanaExternalNetworkException('Error received from Solana network fetching last epoch')
