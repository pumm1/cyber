from colorama import Fore

import cyberdao as DAO
from gameHelper import askInput, safeCastToInt, body_parts_armor_info, body_parts, body_part_head, body_part_body, \
    uniqueArr, INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, EMP, atr_info, modifier_list, BODY_TYPE_MOD, yes_no, \
    body_part_l_arm, body_part_r_arm, body_part_l_leg, body_part_r_leg, printGreenLine, coloredText
from chrome import addChromeWithHumanityCost
from bonus import addAttributeBonuses, handleBonuses, AtrBonus
from src.logger import log_event, log_pos, log_neg


class Armor:
    def __init__(self, row):
        self.id = row['id']
        self.item = row['item']
        self.sp = row['sp']
        self.body_parts = row['body_parts']
        self.ev = row['ev']
        self.character_id = row['character_id']
        attributes = AtrBonus(row)
        self.atr_bonuses = attributes

    def asJson(self):
        resJson = {
            'id': self.id,
            'item': self.item,
            'sp': self.sp,
            'bodyParts': self.body_parts
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

def addArmorForCharacter(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        print(f'Give armor name:')
        item = askInput()
        print(f'Is chrome? {yes_no}')
        is_chrome = False
        while True:
            t_chrome = askInput()
            if t_chrome == 'y':
                is_chrome = True
                break
            elif t_chrome == 'n':
                break
        print(f'Give SP:')
        sp = 0
        while True:
            sp_i = askInput()
            sp = safeCastToInt(sp_i)
            if sp > 0:
                break;
        (atr_bonuses, skill_bonuses) = handleBonuses()
        print('Give encumbrance (EV):')
        ev = -1
        while ev < 0:
            i = askInput()
            ev = safeCastToInt(i)
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

        item_bonus_id = DAO.addArmor(character.id, item, sp, covered_parts, ev, atr_bonuses, skill_bonuses)
        if is_chrome:
            addChromeWithHumanityCost(character, item, 'Added with armor', item_bonus_id=item_bonus_id)
        printGreenLine(f'Armor added!')


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


def removeArmor(name, armor_id):
    char = DAO.getCharacterByName(name)
    if char is not None:
        DAO.deleteCharacterArmor(char.id, armor_id)
