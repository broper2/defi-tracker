import os

from web3 import Web3
from web3.exceptions import InvalidAddress

from app.external.defi_network_base import DefiNetworkInterfaceBase


class EthereumNetworkInterface(DefiNetworkInterfaceBase):

    def __init__(self):
        ethereum_rpc_url = os.environ['ETHEREUM_NODE_URL']
        self.eth = Web3(Web3.HTTPProvider(ethereum_rpc_url)).eth

    def is_valid_account_pubkey(self, pubkey):
        try:
            self.eth.get_balance(pubkey)
        except InvalidAddress:
            return False
        return True

    def get_account_balance(self, pubkey):
        return self.eth.get_balance(pubkey)