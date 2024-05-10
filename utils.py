
import random

def generate_6_digit_id():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])

