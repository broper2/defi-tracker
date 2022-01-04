import asyncio

from app.adapters.wallet.base_portfolio import DefiPortfolioAdapterBase


class DefiPortfolioAdapterAsyncBase(DefiPortfolioAdapterBase):

    def _build_child_data(self):
        return asyncio.run(self._get_child_composite_data())

    async def _get_child_composite_data(self):
        return await asyncio.gather(*(child.get_component_data() for child in self._children))
