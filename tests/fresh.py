import random, string

def password():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))

def bs(n):
    return bytes(random.getrandbits(8) for _ in range(n))
