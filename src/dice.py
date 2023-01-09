import random

from gameHelper import safeCastToInt, askInput, roll_str


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


def rollWithCrit(skip_luck=False, std=None):
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
        crit_str = 'Critical success roll!'
        if std is not None:
            std.append(crit_str)
        else:
            print(crit_str)
        res = res + rollWithCrit(skip_luck=True)
    elif res == 1:
        fumble_str = 'Fumble! For automatic weapons skip fumble table and roll jam'
        if std is not None:
            std.append(fumble_str)
        else:
            print(fumble_str)

    return res