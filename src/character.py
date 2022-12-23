import dice
from roles import roleSpecialAbility
from src.gameHelper import woundState, INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, EMP, body_part_head, body_part_body, \
    body_part_r_arm, body_part_l_arm, body_part_l_leg, body_part_r_leg


class Character:
#character row e.g.: (2, 'Test', 'Solo', 6, 'average', 9, 9, 8, 8, 7, 8, 7, 5, 4)
    def __init__(self, row, skills, rep, sp_row):
        self.id = row['id']
        self.name = row['name']
        self.role = row['role']
        self.reputation = rep
        self.specialAbility = row['special_ability']
        self.skills = skills
        self.bodyTypeModifier = row['body_type_modifier']
        self.attributes = {
            INT: row['atr_int'],
            REF: row['atr_ref'],
            TECH: row['atr_tech'],
            COOL: row['atr_cool'],
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

    def rollFaceDown(self):
        roll = dice.roll(1, 10)
        return roll + self.attributes['COOL'] + self.reputation

    def info(self):
        str = f"""************* {self.name} *************
Role: {self.role}
Attributes: {self.attributes}
Special ability ({roleSpecialAbility(self.role)}): {self.specialAbility}
Reputation: {self.reputation}
Health: {40 - self.dmg_taken} ({woundState(self.dmg_taken)})
SP: {self.sp}
"""
        print(str)