import os

from requests.exceptions import HTTPError

from solana.rpc.async_api import AsyncClient

from app.config.constants import SOLANA_RPC_KEYS
from app.exceptions.solana_external import SolanaExternalNetworkException
from app.external.defi_network_base import DefiNetworkInterfaceBase
from app.utils.error_handling import handle_exceptions


class AsyncSolanaNetworkInterface(DefiNetworkInterfaceBase):

    def __init__(self, *args, **kwargs):
        self.solana_rpc_url = os.environ['SOLANA_RPC_URL']

    async def get_account_balance(self, pubkey):
        return await self._get_account_balance(pubkey)

    async def is_valid_account_pubkey(self, pubkey):
        connected = await self._is_connected()
        valid = await self._is_active_pubkey(pubkey)
        return connected and valid

    @handle_exceptions(SolanaExternalNetworkException, HTTPError, KeyError)
    async def _get_account_balance(self, pubkey):
        async with AsyncClient(self.solana_rpc_url) as client:
            balance = await client.get_balance(pubkey)
        return balance[SOLANA_RPC_KEYS['result']][SOLANA_RPC_KEYS['value']]

    @handle_exceptions(SolanaExternalNetworkException, HTTPError)
    async def _is_connected(self):
        async with AsyncClient(self.solana_rpc_url) as client:
            return await client.is_connected()

    async def _is_active_pubkey(self, pubkey):
        account_info = await self._get_account_info(pubkey)
        return account_info and SOLANA_RPC_KEYS['error'] not in account_info

    @handle_exceptions(SolanaExternalNetworkException, HTTPError)
    async def _get_account_info(self, pubkey):
        async with AsyncClient(self.solana_rpc_url) as client:
            return await client.get_account_info(pubkey)
