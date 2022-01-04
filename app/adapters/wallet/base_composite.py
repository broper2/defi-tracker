from abc import ABC, abstractmethod

from app.utils.rounding import round_crypto, round_usd


class CompositeWalletBase(ABC):

    def __init__(self):
        self.display_name_str = 'display_name'
        self.token_str = 'token'
        self.usd_str = 'usd'
        self.staked_str = 'staked'

    @abstractmethod
    def get_component_data(self):
        raise NotImplementedError

    @abstractmethod
    def _crypto_currency_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _display_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _staked(self):
        raise NotImplementedError

    def _get_usd_value(self, tokens, usd_rate):
        return tokens * usd_rate

    def _build_component_data(self, token_value, usd_rate):
        return {
            self.display_name_str: self._display_name,
            self.token_str: round_crypto(token_value),
            self.usd_str: round_usd(self._get_usd_value(token_value, usd_rate)),
            self.staked_str: self._staked,
        }
