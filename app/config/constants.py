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

BINANCE_PRICE_URL = 'https://api.binance.com/api/v3/ticker/price'

BINANCE_SOL_PARAMS = {'symbol': 'SOLUSDC'}

BINANCE_ETH_PARAMS = {'symbol': 'ETHUSDC'}

SUPPORTED_DEFI_NETWORKS = ['solana', 'ethereum']

SOLANA_SINGLE_RPC_RATE_LIMIT = 40

SOLANA_RATE_LIMIT_TIMEOUT = 10