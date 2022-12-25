import random

from src.gameHelper import safeCastToInt, askInput, roll_str


def roll(n, d_die):
    res = 0
    for i in range(n):
        roll = random.randint(1, d_die)
        #print(f'Rolled {roll} from {diceToStr(1, d_die, 0)}')
        res = res + roll
    return res

def diceToStr(n, d_die, bonus) -> str:
    str = f"{n}D{d_die}"
    suffix = ''
    if bonus > 0:
        suffix = f' + {bonus}'
    str = str + suffix

    return str

def resolveAutoOrManualRollWithCrit():
    print(f'{roll_str} or give roll:')
    roll = 0
    while roll <= 0:
        i = askInput()
        if i == roll_str:
            roll = rollWithCrit()
        else:
            roll = safeCastToInt(i)
    return roll

def rollWithCrit():
    res = roll(1, 10)
    if res == 10:
        print('Critical success roll!')
        res = res + rollWithCrit()
    elif res == 1:
        print('Fumble! For automatic weapons skip fumble table and roll jam')

    return res