import math
import random

from gameHelper import safeCastToInt, askInput, roll_str, printGreenLine, printRedLine


def roll(n, d_die, divide_by=1, bonus=0):
    if divide_by == 0:
        divide_by = 1
    res = 0
    for i in range(n):
        die_roll = random.randint(1, d_die)
        res = res + die_roll
    dice_roll_res = math.ceil(res / divide_by) + bonus
    print(f'Rolled {dice_roll_res} (before possible div: {res}) from {diceToStr(n, d_die, divide_by, bonus)}')
    return dice_roll_res

def diceToStr(n, d_die, divide_by, bonus) -> str:
    div_str = ''
    if divide_by == 0:
        divide_by = 1
    if divide_by > 1:
        div_str = f'/{divide_by}'
    str = f"{n}D{d_die}{div_str}"
    suffix = ''
    if bonus > 0:
        str = f'{str} + {bonus}'

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


def rollWithCrit(skip_luck=False):
    added_luck = 0
    if skip_luck == False:
        print('Add luck? [0-10]')
        while True:
            i = askInput()
            t_lck = safeCastToInt(i)
            if 0 <= t_lck <= 10:
                added_luck = t_lck
                break
    res = roll(1, 10) + added_luck
    if res == 10:
        printGreenLine('Critical success roll!')
        res = res + rollWithCrit(skip_luck=True)
    elif res == 1:
        printRedLine('Fumble! For automatic weapons skip fumble table and roll jam')

    return res