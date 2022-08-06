from hashlib import sha256


def create_token(seed: str):
    res = sha256(seed.encode('utf-8')).hexdigest()[:10]
    return res