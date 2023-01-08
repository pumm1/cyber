import math

import dice
from roles import roleSpecialAbility
import bodytypes
from gameHelper import woundState, INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, EMP, body_part_head, body_part_body, \
    body_part_r_arm, body_part_l_arm, body_part_l_leg, body_part_r_leg, safeCastToInt, infoStr


def woundEffect(dmg_taken, ref, int, cool):
    r = ref
    i = int
    c = cool
    def divBy(val, div):
        return math.ceil(val / div)

    match woundState(dmg_taken):
        case 'No damage':
            r = ref
            i = int
            c = cool
        case 'Light damage':
            r = ref
            i = int
            c = cool
        case 'Serious damage':
            r = ref - 2
            if r < 0:
                r = 0
            i = int
            c = cool
        case 'Critical damage':
            r = divBy(ref, 2)
            i = divBy(int, 2)
            c = divBy(cool, 2)
        case 'Mortally wounded':
            r = divBy(ref, 3)
            i = divBy(int, 3)
            c = divBy(cool, 3)
        case _:
            r = 0
            i = 0
            c = 0

    return (r, i, c)


class Character:
    def __init__(self, row, skills, rep, sp_row, weapons, ev_total, armors, statuses):
        self.id = row['id']
        self.name = row['name']
        self.role = row['role']
        self.reputation = rep
        self.specialAbility = row['special_ability']
        self.skills = skills
        self.bodyTypeModifier = row['body_type_modifier']
        self.humanity = row['humanity']

        dmg_taken = row['dmg_taken']
        self.dmg_taken = dmg_taken

        (ref, int, cool) = woundEffect(dmg_taken, row['atr_ref'], row['atr_int'], row['atr_cool'])

        self.attributes = {
            INT: int,
            REF: ref - ev_total,
            TECH: row['atr_tech'],
            COOL: cool,
            ATTR: row['atr_attr'],
            MA: row['atr_ma'],
            BODY: row['atr_body'],
            LUCK: row['atr_luck'],
            EMP: row['atr_emp']
        }
        self.dmg_taken = row['dmg_taken']
        self.sp = {
            body_part_head: sp_row['head'],
            body_part_body: sp_row['body'],
            body_part_r_arm: sp_row['r_arm'],
            body_part_l_arm: sp_row['l_arm'],
            body_part_r_leg: sp_row['r_leg'],
            body_part_l_leg: sp_row['l_leg']
        }
        self.weapons = weapons
        self.armors = armors
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
        weapon_info = infoStr('Weapons', '\n'.join(w_list))
        atr_affected = ''
        wnd_state = woundState(self.dmg_taken)
        if wnd_state != 'No damage' and wnd_state != 'Light damage':
            atr_affected = '(Stats affected by dmg)'
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
        skill_info = infoStr('Skills', '\n'.join(skill_infos))
        armor_info = infoStr('Armor gear', '\n'.join(armor_infos))
        status_info = infoStr('Statuses', '\n'.join(status_infos))

        str = f"""************* {self.name} *************
Role: {self.role}
Body type: {body_type} ({self.bodyTypeModifier})
Attributes: {self.attributes} {atr_affected}
Humanity: {self.humanity}
Encumbrance (Subtracted from REF): {self.ev} 
Special ability ({roleSpecialAbility(self.role)}): {self.specialAbility}
Reputation: {self.reputation}
Health: {40 - self.dmg_taken} ({woundState(self.dmg_taken)})
SP: {self.sp}

{weapon_info}
{armor_info}
{skill_info}
{status_info}
"""
        print(str)
