from app.config.constants import SOLANA_RPC_KEYS, LAMPORT_TO_SOL_RATE
from app.external.binance_api import BinanceApiInterface
from app.external.solana_network import SolanaNetworkInterface


class SolanaAccountDataAdapter(object):

    def __init__(self, tracked_account):
        self.account_pubkey = tracked_account.key
        self.display_name = tracked_account.display_name
        self.binance_api = BinanceApiInterface.instance()
        self.solana_network_interface = SolanaNetworkInterface.instance()
        self.lamport_value = self._get_lamport_value()

    @property
    def sol_value(self):
        return self.lamport_value * LAMPORT_TO_SOL_RATE

    @property
    def usd_value(self):
        return self.binance_api.get_usd_from_sol(self.sol_value)

    def _get_lamport_value(self):
        rpc_json = self.solana_network_interface.get_account_balance(self.account_pubkey)
        return rpc_json[SOLANA_RPC_KEYS['value']] #TODO key error, need to generalize all error catching for RPC
