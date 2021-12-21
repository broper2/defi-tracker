import collections


DefiValidatorData = collections.namedtuple('DefiValidatorData', ['key', 'display_name'])
DefiWalletData = collections.namedtuple('DefiWalletData', ['key', 'display_name', 'is_staked'])