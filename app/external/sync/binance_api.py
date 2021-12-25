import requests

from app.config.constants import BINANCE_PRICE_URL, BINANCE_ETH_PARAMS, BINANCE_SOL_PARAMS, BINANCE_API_KEYS
from app.exceptions.binance_external import BinanceApiException
from app.utils.error_handling import handle_exceptions

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

    def get_eth_usd_rate(self):
        return float(self._get_eth_price())

    @timed_cache(seconds=5)
    def _get_sol_price(self):
        return self._request_price(BINANCE_SOL_PARAMS)

    @timed_cache(seconds=5)
    def _get_eth_price(self):
        return self._request_price(BINANCE_ETH_PARAMS)

    @handle_exceptions(BinanceApiException, requests.exceptions.HTTPError, KeyError)
    def _request_price(self, params):
        resp = requests.get(BINANCE_PRICE_URL, params)
        resp.raise_for_status()
        return resp.json()[BINANCE_API_KEYS['price']]
