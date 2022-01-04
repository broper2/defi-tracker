from abc import abstractmethod

from app.adapters.wallet.base_composite import CompositeWalletBase


class DefiWalletAdapterBase(CompositeWalletBase):

    def __init__(self, wallet_data, usd_rate):
        super().__init__()
        self._interface = self._network_interface_cls.instance(**self._network_interface_cls_kwargs)
        self._usd_rate = usd_rate
        self._staked_bool = wallet_data.is_staked
        self._name = wallet_data.display_name
        self._wallet_key = wallet_data.key

    @abstractmethod
    def get_component_data(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def _network_interface_cls(self):
        raise NotImplementedError

    @property
    def _network_interface_cls_kwargs(self):
        return dict()

    @property
    def _display_name(self):
        return self._name

    @property
    def _staked(self):
        return str(self._staked_bool)
