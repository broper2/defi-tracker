from app.adapters.wallet.base_wallet import DefiWalletAdapterBase


class DefiWalletAdapterSyncBase(DefiWalletAdapterBase):

    def get_component_data(self):
        token_value = self._crypto_currency_value()
        usd_rate = self._usd_rate
        return self._build_component_data(token_value, usd_rate)
