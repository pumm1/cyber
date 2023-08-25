from colorama import Fore

import cyberdao as DAO
from gameHelper import askInput, safeCastToInt, body_parts_armor_info, body_parts, body_part_head, body_part_body, \
    uniqueArr, INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, EMP, atr_info, modifier_list, BODY_TYPE_MOD, yes_no, \
    body_part_l_arm, body_part_r_arm, body_part_l_leg, body_part_r_leg, printGreenLine, coloredText
from chrome import addChromeWithHumanityCost
from bonus import addAttributeBonuses, handleBonuses, AtrBonus, SkillBonus
from logger import log_event, log_pos, log_neg, Log, log_neutral


class Armor:
    def __init__(self, row):
        self.id = row['armor_id']
        self.item = row['item']
        self.sp = row['sp']
        self.body_parts = row['body_parts']
        self.ev = row['ev']
        self.character_id = row['character_id']
        atr_bonuses = AtrBonus(row)
        self.atr_bonuses = atr_bonuses

    def asJson(self):
        resJson = {
            'id': self.id,
            'item': self.item,
            'sp': self.sp,
            'bodyParts': self.body_parts,
            'attributeBonuses': self.atr_bonuses.asJson()
        }

        return resJson


    def toStr(self) -> str:
        return f'(id: {self.id}) {coloredText(Fore.LIGHTCYAN_EX, self.item)} ({self.sp} SP) - {self.body_parts}'



def checkBodyPartNum(i):
    num = safeCastToInt(i)
    body_part = None
    if num == 1:
        body_part = body_part_head
    elif num == 2:
        body_part = body_part_body
    elif num == 3:
        body_part = body_part_l_arm
    elif num == 4:
        body_part = body_part_r_arm
    elif num == 5:
        body_part = body_part_r_leg
    elif num == 6:
        body_part = body_part_l_leg
    return body_part

def addArmorForCharacter(character, item=None, ev=None, humanity_cost=None, sp=None, covered_parts=None, atr_bonuses=None, skill_bonuses_dict=None) -> list[Log]:
    logs = []
    """
        small HAX: 
        armor could use all bonuses, but it's not fetched now for armor (would be easy fix..),
        but skill improvements feel more like chrome thing
    """
    if character is not None:
        if item is None:
            print(f'Give armor name:')
            item = askInput()

        is_chrome = False
        if humanity_cost is not None:
            if len(skill_bonuses_dict) > 0:
                is_chrome = True
            elif humanity_cost is not None:
                if humanity_cost > 0:
                    is_chrome = True
        else:
            print(f'Is chrome? {yes_no}')
            while True:
                t_chrome = askInput()
                if t_chrome == 'y':
                    is_chrome = True
                    break
                elif t_chrome == 'n':
                    break
        if sp is None:
            print(f'Give SP:')
            sp = 0
            while True:
                sp_i = askInput()
                sp = safeCastToInt(sp_i)
                if sp > 0:
                    break
        if atr_bonuses is None or skill_bonuses_dict is None:
            (atr_bonuses, skill_bonuses) = handleBonuses()
        if ev is None:
            print('Give encumbrance (EV):')
            ev = -1
            while ev < 0:
                i = askInput()
                ev = safeCastToInt(i)

        if covered_parts is None:
            print(f'Give covered body parts: (end with -1 if there is at least one body part)')
            print(body_parts_armor_info)
            covered_parts = []
            while len(covered_parts) < 6:
                input = askInput()
                if (body_parts.__contains__(input)):
                    covered_parts = uniqueArr(covered_parts.append(input))
                elif input == '-1' and len(covered_parts) > 0:
                    break
                else:
                    input = checkBodyPartNum(input)
                    if input is not None:
                        covered_parts.append(input)
                        covered_parts = uniqueArr(covered_parts)

        skill_bonuses = []
        for s in skill_bonuses_dict:
            skill_bonus = SkillBonus(s['skillId'], s['bonus'], item_bonus_id=0)
            skill_bonuses.append(skill_bonus)

        item_bonus_id = DAO.addArmor(character.id, item, sp, covered_parts, ev, atr_bonuses, skill_bonuses)
        chrome_logs = []
        print(f'... is chrome: {is_chrome} ... humanity cost: {humanity_cost}')
        if is_chrome:
            chrome_logs = addChromeWithHumanityCost(
                character, item, 'Added with armor', item_bonus_id=item_bonus_id, humanity_cost=humanity_cost,
                atr_bonuses={}, skill_bonuses=skill_bonuses
            )
        logs = logs + chrome_logs
        logs = log_event(logs, f'Armor added!', log_pos)
    else:
        logs = log_event(logs, 'Character not found for armor adding', log_neg)
    return logs


def addArmorForCharacterById(id, item, ev, sp, body_parts, humanity_cost, atr_bonuses_arr, skill_bonuses_dict):
    character = DAO.getCharacterById(id)
    atr_bonuses = {}
    for a in atr_bonuses_arr:
        atr = a.pop('attribute')
        atr_bonuses[atr] = a['bonus']
    return addArmorForCharacter(character, item, ev, humanity_cost, sp, body_parts, atr_bonuses, skill_bonuses_dict)

def addArmorForCharacterByName(name):
    character = DAO.getCharacterByName(name)
    return addArmorForCharacter(character)


def repairCharSP(char) -> bool:
    logs = []
    if char is not None:
        DAO.repairCharacterSP(char.id)
        logs = log_event(logs, f'Armor repaired for {char.name}', log_pos)
        return logs
    else:
        logs = log_event(logs, f'Character not found for armor repair', log_neg)
    return logs

def repairSPById(char_id) -> bool:
    char = DAO.getCharacterById(char_id)
    return repairCharSP(char)


def repairSPByName(name) -> bool:
    char = DAO.getCharacterByName(name)
    return repairCharSP(char)


def removeArmor(character, armor_id) -> list[Log]:
    logs = []
    if character is not None:
        DAO.deleteCharacterArmor(character.id, armor_id)
        logs = log_event(logs, f'Character armor removed', log_neutral)
    else:
        logs = log_event(logs, f'Character not found for armor removal', log_neg)
    return logs


def removeArmorByCharacterId(id, armor_id) -> list[Log]:
    char = DAO.getCharacterById(id)
    return removeArmor(char, armor_id)


def removeArmorByName(name, armor_id):
    char = DAO.getCharacterByName(name)
    removeArmor(char, armor_id)
