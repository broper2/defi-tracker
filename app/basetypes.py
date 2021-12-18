import collections


SolanaValidatorData = collections.namedtuple('SolanaValidatorData', ['key', 'display_name'])
SolanaWalletData = collections.namedtuple('SolanaWalletData', ['key', 'display_name', 'is_staked'])