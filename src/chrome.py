import math

from colorama import Fore

import cyberdao as DAO
from dice import roll
from gameHelper import askInput, roll_str, askForRoll, safeCastToInt, EMP, printGreenLine, printRedLine, coloredText
from bonus import handleBonuses, AtrBonus, SkillBonus


class Chrome:
    def __init__(self, row):
        self.item = row['item']
        self.description = row['description']
        atr_bonuses = AtrBonus(row)
        skill_bonus_rows = DAO.getItemSkillBonuses(row['item_bonus_id'])
        skill_bonuses = []
        for bonus_row in skill_bonus_rows:
            skill_bonus = SkillBonus(bonus_row['skill_id'], bonus_row['skill_bonus'], row['item_bonus_id'])
            skill_bonuses.append(skill_bonus)
        self.atr_bonuses = atr_bonuses
        self.skill_bonuses = skill_bonuses

    def toStr(self):
        return f"{coloredText(Fore.LIGHTCYAN_EX, self.item)} ({self.description})"


def addChrome(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        print('Give name of cybernetic:')
        item = askInput()
        print('Give description:')
        descr = askInput()

        addChromeWithHumanityCost(character, item, descr)
        printGreenLine(f'Chrome added for {character.name}')


def addChromeWithHumanityCost(character, item, descr, item_bonus_id: int | None = None):
    (atr_bonuses, skill_bonuses) = ({}, [])
    if item_bonus_id is None:
        (atr_bonuses, skill_bonuses) = handleBonuses()
    humanity_cost = handleHumanity(character)
    DAO.addChrome(character.id, item, humanity_cost, descr, item_bonus_id, atr_bonuses, skill_bonuses)


def handleHumanity(char):
    print(f'Reduce humanity for chrome ({roll_str} or <amount>)')
    humanity_cost = 0
    while True:
        i = askInput()
        if i == roll_str:
            (dice, die, bonus) = askForRoll()
            humanity_cost = roll(dice, die) + bonus
            print(f'Rolled {humanity_cost}')
            break
        else:
            cost = safeCastToInt(i)
            if cost > 0:
                humanity_cost = cost
                break

    curr_hum = char.humanity
    t_hum = curr_hum - humanity_cost
    emp = math.ceil(t_hum / 10)
    print(f'Curr emp: {char.attributes[EMP]} - new emp: {emp}')
    printRedLine(f'Current humanity: {curr_hum} - new humanity: {t_hum}')
    DAO.reduceHumanity(char.id, t_hum, emp)
    print(f'Updated humanity and empathy')
    return humanity_cost
