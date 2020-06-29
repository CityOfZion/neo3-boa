import string

chars = string.digits + string.ascii_letters
base = len(chars)


def encode_base62(num: int):
    """Encode number in base62, returns a string."""
    if num < 0:
        raise ValueError('cannot encode negative numbers')

    if num == 0:
        return chars[0]

    digits = []
    while num:
        rem = num % base
        num = num // base
        digits.append(chars[rem])
    return ''.join(reversed(digits))
