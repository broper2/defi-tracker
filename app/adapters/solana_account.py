from app.config.constants import SOLANA_RPC_KEYS, LAMPORT_TO_SOL_RATE
from app.external.binance_api import BinanceApiInterface


class SolanaAccountDataAdapter(object):

    def __init__(self, display_name, **data):
        self.display_name = display_name
        self.lamport_value = data.get(SOLANA_RPC_KEYS['value'])
        self.binance_api = BinanceApiInterface()

    @property
    def sol_value(self):
        return self.lamport_value * LAMPORT_TO_SOL_RATE

    @property
    def usd_value(self):
        return self.binance_api.get_usd_from_sol(self.sol_value)
