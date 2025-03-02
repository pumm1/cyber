import pytest

from src.dice import diceToStr, roll

def testDiceToStrFormatting():
    diceStr = diceToStr(1, 10, 1, 0)
    assert diceStr == '1D10'
    diceStr = diceToStr(1, 6, 1, 0)
    assert diceStr == '1D6'
    diceStr = diceToStr(1, 6, 1, 2)
    assert diceStr == '1D6 + 2'
    diceStr = diceToStr(1, 6, 2, 0)
    assert diceStr == '1D6/2'

def run100DiceRolls(d: int):
    above_limit = False
    for i in range(100):
        roll_res = roll(1, d, skip_log=True)
        if roll_res > d:
            above_limit = True

    return above_limit

def testDiceValueRange():
    value_above_10 = run100DiceRolls(10)

    assert value_above_10 == False

    value_above_6 = run100DiceRolls(6)
    assert value_above_6 == False

