import random

def roll(n, d_die):
    res = 0
    for i in range(n):
        roll = random.randint(1, d_die)
        res = res + roll
    return res