from app.adapters.wallet.base_portfolio import DefiPortfolioAdapterBase


class DefiPortfolioAdapterSyncBase(DefiPortfolioAdapterBase):

    def _build_child_data(self):
        return self._get_child_composite_data()

    def _get_child_composite_data(self):
        return [child.get_component_data() for child in self._children]
