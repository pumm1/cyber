import dice
from roles import roleSpecialAbility
import bodytypes
from gameHelper import woundState, body_part_head, body_part_body, \
    body_part_r_arm, body_part_l_arm, body_part_l_leg, body_part_r_leg, safeCastToInt, infoStr, fieldName
from colorama import Fore, Style

class Character:
    def __init__(self, row, skills, rep, sp_row, weapons, ev_total, armors, statuses, bodyTypeModifier, attributes, cybernetics):
        self.id = row['id']
        self.name = row['name']
        self.role = row['role']
        self.reputation = rep
        self.specialAbility = row['special_ability']
        self.skills = skills
        self.humanity = row['humanity']

        dmg_taken = row['dmg_taken']
        self.dmg_taken = dmg_taken
        self.cybernetics = cybernetics

        self.weapons = weapons
        self.armors = armors
        self.bodyTypeModifier = bodyTypeModifier

        self.attributes = attributes
        self.dmg_taken = row['dmg_taken']
        self.sp = {
            body_part_head: sp_row['head'],
            body_part_body: sp_row['body'],
            body_part_r_arm: sp_row['r_arm'],
            body_part_l_arm: sp_row['l_arm'],
            body_part_r_leg: sp_row['r_leg'],
            body_part_l_leg: sp_row['l_leg']
        }
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
            roll = dice.rollWithCrit()
        return roll + self.attributes['COOL'] + self.reputation



    def info(self):
        weapons_infos = map(lambda w: (
            w.toStr()
        ), self.weapons)

        w_list = list(weapons_infos)
        weapon_info = infoStr(f'{fieldName("Weapons")}', '\n'.join(w_list))
        atr_affected = ''
        wnd_state = woundState(self.dmg_taken)
        if wnd_state != 'No damage' and wnd_state != 'Light damage':
            atr_affected = f'{Fore.RED}(Stats affected by dmg){Style.RESET_ALL}'
        body_type = bodytypes.bodyTypeModifiersByValue(self.bodyTypeModifier)
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

        str = f"""************* {Fore.CYAN}{self.name}{Style.RESET_ALL} (id: {self.id}) *************
{fieldName('Role')}: {self.role}
{fieldName('Body type')}: {body_type} ({self.bodyTypeModifier})
{fieldName('Attributes')}: {self.attributes} {atr_affected}
{fieldName('Humanity')}: {self.humanity}
{fieldName('Encumbrance(Subtracted from REF)')}: {Fore.RED}{self.ev}{Style.RESET_ALL} 
{fieldName('Special ability')}({roleSpecialAbility(self.role)}): {self.specialAbility}
{fieldName('Reputation')}: {self.reputation}
{fieldName('Health')}: {40 - self.dmg_taken} ({woundState(self.dmg_taken)})
{fieldName('SP')}: {self.sp}
{weapon_info}
{armor_info}
{chrome_info}
{skill_info}
{status_info}
"""
        print(str)
