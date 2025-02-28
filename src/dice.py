import math
import random

from src.gameHelper import safeCastToInt, askInput, roll_str, printGreenLine, printRedLine
from src.logger import Log, log_event, log_pos, log_neg


def roll(n, d_die, divide_by=1, bonus=0, skip_log=False) -> int:
    if divide_by == 0:
        divide_by = 1
    res = 0
    for i in range(n):
        die_roll = random.randint(1, d_die)
        res = res + die_roll
    dice_roll_res = math.ceil(res / divide_by) + bonus
    if not skip_log:
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

def resolveAutoOrManualRollWithCrit(auto_roll=False, skip_luck=False):
    roll_res = 0
    i = ''
    while roll_res <= 0:
        if auto_roll is False:
            print(f'{roll_str} or give roll:')
            i = askInput()
        else:
            i = roll_str
        if i == roll_str:
            (roll_res, _) = rollWithCrit(skip_luck)
        else:
            roll_res = safeCastToInt(i)
    return roll_res


def handleLuck(skip_luck=False):
    added_luck = 0
    if skip_luck == False:
        print('Add luck? [0-10]')
        while True:
            i = askInput()
            t_lck = safeCastToInt(i)
            if 0 <= t_lck <= 10:
                added_luck = t_lck
                break
    return added_luck

def rollWithCritAndGivenLuck(added_luck=0) -> (int, list[Log]):
    (res, added_logs) = rollWithCrit(skip_luck=True)
    logs = added_logs
    if res == 10:
        logs = log_event(logs, 'Critical success roll!', log_pos)
        res = res + rollWithCrit(skip_luck=True)

    return (res + added_luck, logs)


def rollWithCrit(skip_luck=False) -> (int, list[Log]):
    logs = []
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
        logs = log_event(logs, 'Critical success roll!', log_pos)
        (t_res, added_logs) = rollWithCrit(skip_luck=True)
        res = t_res + res
        logs = logs + added_logs
    elif res == 1:
        logs = log_event(logs, 'Fumble or Critical failure! For automatic weapons skip fumble table and roll jam', log_neg)

    return (res, logs)