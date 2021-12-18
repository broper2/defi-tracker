import collections


SolanaValidatorData = collections.namedtuple('SolanaValidatorData', ['key', 'display_name'])
SolanaAccountData = collections.namedtuple('SolanaAccountData', ['key', 'display_name', 'is_staked'])