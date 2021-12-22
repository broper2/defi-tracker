SOLANA_RPC_KEYS = {
    'activated_stake' : 'activatedStake',
    'commission' : 'commission',
    'epoch_credits' : 'epochCredits',
    'epoch_vote_account' : 'epochVoteAccount',
    'node_pubkey' : 'nodePubkey',
    'root_slot' : 'rootSlot',
    'vote_pubkey' : 'votePubkey',
    'value': 'value',
    'result': 'result',
    'current': 'current',
    'error': 'error',
    'epoch': 'epoch'
}

SOLANA_VALIDATOR_HISTORY_LENGTH = 5

BINANCE_API_KEYS = {
    'price': 'price'
}

LAMPORT_TO_SOL_RATE = 0.000000001

WEI_TO_ETH_RATE = (1/10**18)

BINANCE_SOL_PRICE_URL = 'https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDC'

BINANCE_ETH_PRICE_URL = 'https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDC' #TODO fix duplicates

DEFAULT_DEFI_NETWORK = 'solana'

SUPPORTED_DEFI_NETWORKS = ['solana', 'ethereum']