import requests

from app.config.constants import BINANCE_SOL_PRICE_URL
from app.exceptions.binance_external import BinanceApiException


class BinanceApiInterface(object):

    def __init__(self):
        self.sol_price_url = BINANCE_SOL_PRICE_URL

    def get_usd_from_sols(self, sols):
        usd_sol_rate = self._get_sol_to_usd_rate()
        return [round(sol * usd_sol_rate, 2) for sol in sols]

    def _get_sol_to_usd_rate(self):
        try:
            resp = requests.get(self.sol_price_url)
        except Exception:
            raise BinanceApiException('Error when fetching SOLUSD price from Binance')
        if resp.status_code != 200:
            raise BinanceApiException(f'Error from Binance api - received status_code {resp.status_code}')
        return float(resp.json()['price'])
