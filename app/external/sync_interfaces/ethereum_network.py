import os

from web3 import Web3
from web3.exceptions import InvalidAddress

from app.exceptions.ethereum_external import EthereumExternalNetworkException
from app.external.defi_network_base import DefiNetworkInterfaceBase
from app.utils.error_handling import handle_exceptions


class EthereumNetworkInterface(DefiNetworkInterfaceBase):

    def __init__(self, *args, **kwargs):
        ethereum_rpc_url = os.environ['ETHEREUM_NODE_URL']
        self.eth = Web3(Web3.HTTPProvider(ethereum_rpc_url)).eth

    def is_valid_account_pubkey(self, pubkey):
        try:
            return self.eth.get_balance(pubkey) is not None
        except InvalidAddress:
            return False

    @handle_exceptions(EthereumExternalNetworkException, InvalidAddress)
    def get_account_balance(self, pubkey):
        return self.eth.get_balance(pubkey)