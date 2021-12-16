import requests

from app.config.constants import BINANCE_SOL_PRICE_URL, BINANCE_API_KEYS
from app.exceptions.binance_external import BinanceApiException

from app.utils.timed_cache import timed_cache


class BinanceApiInterface(object):

    _instance = None

    @classmethod
    def instance(cls):
        if not cls._instance:
            cls._instance = cls()
        return cls._instance

    def get_sol_usd_rate(self):
        return float(self._get_sol_price())

    @timed_cache(seconds=5)
    def _get_sol_price(self):
        try:
            resp = requests.get(BINANCE_SOL_PRICE_URL)
        except requests.exceptions.RequestException:
            raise BinanceApiException('Error when requesting SOLUSD price from Binance')
        if resp.status_code != 200:
            raise BinanceApiException(f'Error from Binance api - received status_code {resp.status_code}')
        return resp.json()[BINANCE_API_KEYS['price']]
