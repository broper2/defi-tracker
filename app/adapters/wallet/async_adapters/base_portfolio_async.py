import asyncio
import time

from app.adapters.wallet.base_portfolio import DefiPortfolioAdapterBase
from app.config.constants import SOLANA_SINGLE_RPC_RATE_LIMIT, SOLANA_RATE_LIMIT_TIMEOUT


class DefiPortfolioAdapterAsyncBase(DefiPortfolioAdapterBase):

    def _build_child_data(self):
        return asyncio.run(self._get_child_composite_data())

    async def _get_child_composite_data(self):
        child_composite_data = []
        child_batches = self._get_child_batches()
        timeout_required = False
        for batch in child_batches:
            if timeout_required:
                time.sleep(SOLANA_RATE_LIMIT_TIMEOUT)
            data = await asyncio.gather(*(child.get_component_data() for child in batch))
            child_composite_data += data
            timeout_required = True
        return child_composite_data

    def _get_child_batches(self):
        num_children = len(self._children)
        for index in range(0, num_children, SOLANA_SINGLE_RPC_RATE_LIMIT):
            yield self._children[index:min(index + SOLANA_SINGLE_RPC_RATE_LIMIT, num_children)]