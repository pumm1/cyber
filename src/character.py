import src.dice as dice
from src.roles import roleSpecialAbility
import src.bodytypes as bodytypes
from src.gameHelper import woundState, woundStatePlain, body_part_head, body_part_body, \
    body_part_r_arm, body_part_l_arm, body_part_l_leg, body_part_r_leg, safeCastToInt, infoStr, fieldName, coloredText, \
    no_dmg, light_dmg, BODY
from colorama import Fore

from src.skill import SkillInfo


class CharacterShort:
    def __init__(self, row):
        self.id = row['id']
        self.name = row['name']
        self.role = row['role']

    def asJson(self):
        res = {
            "id": self.id,
            "name": self.name,
            "role": self.role
        }

        return res

class Character:
    def __init__(self, row, skills: list[SkillInfo], rep, sp_row, weapons, ev_total, armors, statuses, bodyTypeModifier, initiativeBonus, attributes, cybernetics):
        self.id = row['id']
        self.name = row['name']
        self.role = row['role']
        self.reputation = rep
        self.specialAbility = row['special_ability']
        self.skills: list[SkillInfo] = skills
        self.humanity = row['humanity']
        self.money = row['money']
        self.background = row['background']

        dmg_taken = row['dmg_taken']
        self.dmg_taken = dmg_taken
        self.cybernetics = cybernetics

        self.weapons = weapons
        self.armors = armors
        self.bodyTypeModifier = bodyTypeModifier
        self.initiativeBonus = initiativeBonus

        self.attributes = attributes
        self.max_emp = row['emp_max']
        self.dmg_taken = row['dmg_taken']
        self.sp = {
            body_part_head: sp_row['head'],
            body_part_body: sp_row['body'],
            body_part_r_arm: sp_row['r_arm'],
            body_part_l_arm: sp_row['l_arm'],
            body_part_r_leg: sp_row['r_leg'],
            body_part_l_leg: sp_row['l_leg']
        }
        self.ip = row['ip']
        self.ev = ev_total
        self.statuses = statuses

    def rollSkill(self, skill, bonus = 0):
        s = self.findSkill(skill)
        roll = 0
        if s is not None:
            atr = s['attribute']
            atr_bonus = self.attributes[atr]
            roll = dice.roll(1, 10)
            skill_bonus = s['value']
            result = roll + atr_bonus + skill_bonus + bonus

            return result

    def findSkill(self, skill):
        for s in self.skills:
            if s["skill"] == skill:
                return s
        return None

    def rollFaceDown(self, r):
        roll = safeCastToInt(r)
        if roll <= 0:
            (roll, _) = dice.rollWithCrit(skip_luck=True)
        return roll + self.attributes['COOL'] + self.reputation

    def asJson(self):
        skills = map(lambda skill: (
            skill.asJson()
        ), self.skills)
        armor = map(lambda a: (
            a.asJson()
        ), self.armors)
        weapons = map(lambda w: (
            w.asJson()
        ), self.weapons)
        chrome = map(lambda c: (
            c.asJson()
        ), self.cybernetics)

        statuses = map(lambda s: (
            s.asJson()
        ), self.statuses)

        resJson = {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "background": self.background,
            "specialAbilityLvl": self.specialAbility,
            "specialAbility": roleSpecialAbility(self.role),
            "attributes": self.attributes,
            "bodyType": bodytypes.bodyTypeByValue(self.attributes[BODY]),
            "btm": self.bodyTypeModifier,
            "initiativeBonus": self.initiativeBonus,
            "woundState": woundStatePlain(self.dmg_taken),
            "dmgTaken": self.dmg_taken,
            "reputation": self.reputation,
            "humanity": self.humanity,
            "skills": list(skills),
            "chrome": list(chrome),
            'weapons': list(weapons),
            "armor": list(armor),
            "sp": self.sp,
            "ip": self.ip,
            "money": self.money,
            'statuses': list(statuses)
        }

        return resJson

    def info(self):
        weapons_infos = map(lambda w: (
            w.toStr()
        ), self.weapons)

        w_list = list(weapons_infos)
        weapon_info = infoStr(f'{fieldName("Weapons")}', '\n'.join(w_list))
        atr_affected = ''
        wnd_state = woundState(self.dmg_taken)
        if wnd_state != no_dmg and wnd_state != light_dmg:
            atr_affected = f'{coloredText(Fore.RED, "(Stats affected by dmg)")}'
        body_type = bodytypes.bodyTypeByValue(self.attributes[BODY])
        body_type_mod = bodytypes.bodyTypeModifiersByValue(self.bodyTypeModifier)
        skill_infos = map(lambda skill: (
            skill.toStr()
        ), self.skills)
        armor_infos = map(lambda a: (
            a.toStr()
        ), self.armors)
        status_infos = map(lambda s: (
            s.toStr()
        ), self.statuses)
        chrome_infos = map(lambda c: (
            c.toStr()
        ), self.cybernetics)
        skill_info = infoStr(f'{fieldName("Skills")}', '\n'.join(skill_infos))
        armor_info = infoStr(f'{fieldName("Armor gear")}', '\n'.join(armor_infos))
        chrome_info = infoStr(f'{fieldName("Chrome")}', '\n'.join(chrome_infos))
        status_info = infoStr(f'{fieldName("Statuses")}', '\n'.join(status_infos))

        str = f"""************* {coloredText(Fore.GREEN, self.name)} (id: {self.id}) *************
{fieldName('Role')}: {self.role}
{fieldName('Body type')}: {body_type} (Save {self.attributes[BODY]})
{fieldName('Body type modifier')}: {body_type_mod} (-{self.bodyTypeModifier} to dmg)
{fieldName('Attributes')}: {self.attributes} {atr_affected}
{fieldName('Humanity')}: {self.humanity}
{fieldName('Encumbrance (Subtracted from REF)')}: {coloredText(Fore.RED, f"{self.ev}")} 
{fieldName('Special ability')} ({roleSpecialAbility(self.role)}): {self.specialAbility}
{fieldName('Reputation')}: {self.reputation}
{fieldName('Health')}: 40 / {40 - self.dmg_taken} ({woundState(self.dmg_taken)})
{fieldName('SP')}: {self.sp}
{weapon_info}
{armor_info}
{chrome_info}
{skill_info}
{status_info}
"""
        print(str)
