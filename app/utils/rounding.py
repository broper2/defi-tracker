

def round_credit_rate(rate):
    return _round(rate, 6)

def round_usd(usd):
    return _round(usd, 2)

def round_sol(sol):
    return _round(sol, 5)

def _round(rate, decimals):
    return round(rate, decimals)