import random
import string


def get_random_str(length: int = 30) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
