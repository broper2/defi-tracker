from abc import ABC, abstractmethod

from app.utils.rounding import round_crypto, round_usd


class PortfolioCompositeBase(ABC):

    @property
    def composite_data(self):
        data = []
        for child in self._children:
            data.append(child._get_composite_data())
        data.append(self._get_composite_data())
        return data

    def _get_composite_data(self):
        return {
            'display_name': self._display_name,
            'sol': round_crypto(self._crypto_currency_value),
            'usd': round_usd(self._usd_value),
            'staked': self._staked,
        }

    @property
    @abstractmethod
    def _children(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _crypto_currency_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _usd_value(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _display_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _staked(self):
        raise NotImplementedError
