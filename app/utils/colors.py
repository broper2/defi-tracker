import random

def get_random_hex_code():
    r = lambda: random.randint(0,255)
    return '#%02X%02X%02X' % (r(),r(),r())