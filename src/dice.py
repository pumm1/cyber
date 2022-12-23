import random

def roll(n, d_die):
    res = 0
    for i in range(n):
        roll = random.randint(1, d_die)
        res = res + roll
    return res

def rollWithCrit():
    res = roll(1, 10)
    if res == 10:
        print('Critical success roll!')
        res = res + rollWithCrit()
    elif res == 1:
        print('Fumble!')

    return res