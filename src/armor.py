import cyberdao as DAO
from gameHelper import askInput, safeCastToInt, body_parts_armor_info, body_parts, body_part_head, body_part_body, \
    uniqueArr, INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, EMP, atr_info, modifier_list, BODY_TYPE_MOD, yes_no, \
    body_part_l_arm, body_part_r_arm, body_part_l_leg, body_part_r_leg
from chrome import addChromeWithHumanityCost


class Armor:
    def __init__(self, row):
        self.id = row['id']
        self.item = row['item']
        self.sp = row['sp']
        self.body_parts = row['body_parts']
        self.ev = row['ev']
        self.character_id = row['character_id']
        self.attributes = {
            INT: row['atr_int'],
            REF: row['atr_ref'],
            TECH: row['atr_tech'],
            COOL: row['atr_ref'],
            ATTR: row['atr_attr'],
            MA: row['atr_ma'],
            BODY: row['atr_body'],
            LUCK: row['atr_luck'],
            EMP: row['atr_emp'],
            BODY_TYPE_MOD: row['body_type_modifier']
        }

    def toStr(self) -> str:
        return f'(id: {self.id}) {self.item} ({self.sp} SP) - {self.body_parts}'


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
        bonuses_dict = addAttributeBonuses()
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

        DAO.addArmor(character.id, item, sp, covered_parts, ev, bonuses_dict)
        if is_chrome:
            addChromeWithHumanityCost(character, item, 'Added with armor')
        print(f'Armor added!')



def handleAttributeBonuses():
    print(f'Modify attributes? {yes_no}')
    i = askInput()
    bonuses = []
    while True:
        if i == 'y':
            bonuses = addAttributeBonuses()
            break
        elif i == 'n':
            break
    return bonuses


def addAttributeBonuses():
    bonuses_dict = {}
    array_limit = len(modifier_list)
    bonus = 0
    while True:
        print(f'Give attributes: (end with -1)')
        print(atr_info)
        input = askInput()
        i = safeCastToInt(input)
        if len(bonuses_dict) >= array_limit:
            break
        elif i == -1:
            break
        elif 0 < i <= array_limit:
            atr = modifier_list[i - 1]
            print(f'Attribute ({atr}) modified by:')
            inp = askInput()
            bonus = safeCastToInt(inp)
            bonuses_dict.update({atr: bonus})
        print(f'Current bonuses: {bonuses_dict}')
    return bonuses_dict



def repairSP(name):
    char = DAO.getCharacterByName(name)
    if char is not None:
        DAO.repairCharacterSP(char.id)
        print(f'Armor repaired for {char.name}')


def removeArmor(name, armor_id):
    char = DAO.getCharacterByName(name)
    if char is not None:
        DAO.deleteCharacterArmor(char.id, armor_id)
