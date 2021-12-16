

def round_credit_rate(rate):
    return _round(rate, 6)

def round_usd(usd):
    return _round(usd, 2)

def round_crypto(crypto):
    return _round(crypto, 5)

def round_validator_performance(performance):
    return _round(performance, 6)

def _round(rate, decimals):
    return round(rate, decimals)