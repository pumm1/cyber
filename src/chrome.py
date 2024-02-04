import math

from colorama import Fore

import cyberdao as DAO
from dice import roll
from gameHelper import askInput, roll_str, askForRoll, safeCastToInt, EMP, printGreenLine, printRedLine, coloredText
from bonus import handleBonuses, AtrBonus, SkillBonus
from logger import Log, log_event, log_neutral, log_neg


class Chrome:
    def __init__(self, row):
        self.id = row['chrome_id']
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

    def asJson(self):
        skill_bonuses = map(lambda s: (
            s.asJson()
        ), self.skill_bonuses)
        resJson = {
            'item': self.item,
            'id': self.id,
            'description': self.description,
            'attributeBonuses': self.atr_bonuses.asJson(),
            'skillBonuses': list(skill_bonuses)
        }

        return resJson

def addChrome(character, name=None, descr=None) -> list[Log]:
    logs = []
    if character is not None:
        print('Give name of cybernetic:')
        item = askInput()
        print('Give description:')
        descr = askInput()

        addChromeWithHumanityCost(character, item, descr)
        printGreenLine(f'Chrome added for {character.name}')


def addChromeByCharacterId(id, item, descr, humanity_cost, atr_bonuses, skill_bonuses_dict):
    logs = []
    atr_dict = dict([])
    for atr_bonus in atr_bonuses:
        atr = atr_bonus['attribute']
        bonus = atr_bonus['bonus']
        t_a_bonus = atr_dict.get(atr)
        if t_a_bonus is None:
            atr_dict[atr] = bonus
        else:
            bonus = t_a_bonus + bonus
            atr_dict[atr] = bonus
    character = DAO.getCharacterById(id)
    skill_bonuses = []
    for s in skill_bonuses_dict:
        skill_bonus = SkillBonus(s['skillId'], s['bonus'], item_bonus_id=0)
        skill_bonuses.append(skill_bonus)

    if character is not None:
        chrome_logs = addChromeWithHumanityCost(character, item, descr, humanity_cost=humanity_cost, atr_bonuses=atr_dict, skill_bonuses=skill_bonuses)

    return logs + chrome_logs


def addChromeByName(name):
    character = DAO.getCharacterByName(name)
    addChrome(character)

def addChromeWithHumanityCost(
        character, item, descr, humanity_cost = None, item_bonus_id: int | None = None, atr_bonuses=None, skill_bonuses=None
) -> list[Log]:
    if atr_bonuses is None or skill_bonuses is None:
        (atr_bonuses, skill_bonuses) = handleBonuses()
    (humanity_cost, logs) = handleHumanity(character, humanity_cost)
    DAO.addChrome(character.id, item, humanity_cost, descr, item_bonus_id, atr_bonuses, skill_bonuses)

    return logs


def handleHumanity(char, humanity_cost=None) -> (int, list[Log]):
    if humanity_cost is None:
        print(f'Reduce humanity for chrome ({roll_str} or <amount>)')
        humanity_cost = 0
        while True:
            i = askInput()
            if i == roll_str:
                (dice, die, divide_by, bonus) = askForRoll()
                humanity_cost = roll(dice, die, divide_by) + bonus
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
    logs = log_event([], f'Curr emp: {char.attributes[EMP]} - new emp: {emp}', log_neutral)
    logs = log_event(logs, f'Current humanity: {curr_hum} - new humanity: {t_hum}', log_neg)
    DAO.changeHumanityAndEmp(char.id, t_hum, emp)
    logs = log_event(logs, f'Updated humanity and empathy', log_neutral
                     )
    return (humanity_cost, logs)


def removeChromeByCharacterId(chararacter_id, chrome_id) -> list[Log]:
    character = DAO.getCharacterById(chararacter_id)
    logs = []
    if character is not None:
        DAO.deleteCharacterChrome(chararacter_id, chrome_id)
        logs = log_event(logs, f'Chrome deleted from {character.name}', log_neutral)
    else:
        logs = log_event(logs, f'Character not found for chrome deletion', log_neg)
    return logs
