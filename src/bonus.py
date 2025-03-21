from colorama import Fore

from src import cyberService
from src.gameHelper import INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, EMP, BODY_TYPE_MOD, askInput, yes_no, modifier_list, \
    atr_info, safeCastToInt, list_skills_helper_str, list_skills_str, split_at, coloredText, body_type_mod, atr_int, \
    atr_emp, atr_luck, atr_body, atr_ma, atr_attr, atr_ref, atr_tech, atr_cool, init_bonus, INIT_BONUS
import src.skills
import src.cyberdao as DAO


class AtrBonus:
    def __init__(self, atr_row):
        self.id = atr_row['id']
        self.attributes = {
            INT: atr_row[atr_int],
            REF: atr_row[atr_ref],
            TECH: atr_row[atr_tech],
            COOL: atr_row[atr_cool],
            ATTR: atr_row[atr_attr],
            MA: atr_row[atr_ma],
            BODY: atr_row[atr_body],
            LUCK: atr_row[atr_luck],
            EMP: atr_row[atr_emp],
            BODY_TYPE_MOD: atr_row[body_type_mod],
            INIT_BONUS: atr_row[init_bonus]
        }

    def asJson(self):
        resJson = {
            'INT': self.attributes[INT],
            'REF': self.attributes[REF],
            'TECH': self.attributes[TECH],
            'COOL': self.attributes[COOL],
            'ATTR': self.attributes[ATTR],
            'MA': self.attributes[MA],
            'BODY': self.attributes[BODY],
            'LUCK': self.attributes[LUCK],
            'EMP': self.attributes[INT],
            'BTM': self.attributes[BODY_TYPE_MOD],
            'INIT': self.attributes[INIT_BONUS]
        }

        return resJson


class SkillBonus:
    def __init__(self, skill_id, bonus, item_bonus_id):
        self.skill_id = skill_id
        self.bonus = bonus
        self.item_bonus_id = item_bonus_id

    def asJson(self):
        resJson = {
            'skillId': self.skill_id,
            'bonus': self.bonus,
            'itemBonusId': self.item_bonus_id
        }

        return resJson


def handleBonuses():
    print(f'Modify attributes? {yes_no}')
    i = askInput()
    atr_bonuses: dict[str, int] = {}
    while True:
        if i == 'y':
            atr_bonuses = addAttributeBonuses()
            break
        elif i == 'n':
            break
    print(f'Modify skills? {yes_no}')
    skill_bonuses = []
    i = askInput()
    while True:
        if i == 'y':
            skill_bonuses = addSkillBonuses()
            break
        elif i == 'n':
            break

    return (atr_bonuses, skill_bonuses)


def addSkillBonuses() -> [SkillBonus]:
    print(f"Give skill id for bonus or {list_skills_str} to list skills")
    print("(end with -1)")
    skill_bonuses = []
    while True:
        i = askInput()
        command_parts = i.split(split_at)
        skill_id = safeCastToInt(i)
        if i == '-1':
            break
        elif i.startswith(list_skills_str):
            cyberService.listSkills(command_parts)
        elif skill_id > 0:
            skill = DAO.getSkillById(skill_id)
            if skill is not None:
                skill_name = coloredText(Fore.GREEN, skill['skill'])
                print(f"Give bonus for skill {skill_name}:")
                i = askInput()
                bonus = safeCastToInt(i)
                bonus_str = coloredText(Fore.GREEN, f'+{bonus}')
                skill_bonus = SkillBonus(skill_id, bonus, item_bonus_id=0)
                skill_bonuses.append(skill_bonus)
                print(f"Skill {skill_name} ({bonus_str}) added")

    return skill_bonuses



def addAttributeBonuses() -> dict[str, int]:
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
