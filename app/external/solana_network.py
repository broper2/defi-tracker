from app.config.constants import SOLANA_PRODUCTION_API_URL
from app.config.constants import SOLANA_RPC_KEYS, LAMPORT_TO_SOL_RATE
from app.exceptions.solana_external import SolanaExternalNetworkException
from app.utils.rounding import round_sol
from app.utils.timed_cache import timed_cache
from app.wrappers.solana_validator import SolanaValidatorWrapper
from solana.rpc.api import Client


class SolanaNetworkInterface(object):

    def __init__(self, cache_validator_data=True):
        self.solana_rpc_client = Client(SOLANA_PRODUCTION_API_URL)
        self.vote_account_keys = []
        if cache_validator_data:
            self._cache_vote_account_data()

    def _cache_vote_account_data(self):
        try:
            data = self._fetch_validator_data()
            self.vote_account_keys = [account[SOLANA_RPC_KEYS['vote_pubkey']] for account in data]
        except Exception:
            raise SolanaExternalNetworkException('Error in initial load of validator data from Solana network')

    def _get_validator_data(self):
        try:
            return self._fetch_validator_data()
        except Exception:
            raise SolanaExternalNetworkException('Error in fetching validator data from Solana network')

    @timed_cache(hours=1)
    def _fetch_validator_data(self):
        return self.solana_rpc_client.get_vote_accounts()['result']['current']

    def get_wrapped_validator_data(self, pubkeys):
        validator_data = self._get_validator_data()
        validator_data = [data for data in validator_data if data['votePubkey'] in pubkeys]
        return [SolanaValidatorWrapper(v_data) for v_data in validator_data]

    def _get_account_data(self, pubkey):
        return self.solana_rpc_client.get_balance(pubkey)

    def get_account_sol_balance(self, pubkey):
        try:
            account_data = self._get_account_data(pubkey)
        except Exception:
            raise SolanaExternalNetworkException('Error in fetching account balance from Solana network')
        return round_sol(account_data['result']['value'] * LAMPORT_TO_SOL_RATE)

    def is_valid_account_pubkey(self, pubkey):
        if not self._is_connected():
            return False
        try:
            account_data = self._get_account_data(pubkey)
            return 'error' not in account_data
        except Exception:
            return False

    def _is_connected(self):
        return self.solana_rpc_client.is_connected()
