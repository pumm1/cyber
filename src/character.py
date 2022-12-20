import dice
import json

class Character:
    def __init__(self, file):
        f = open(file)
        data = json.load(f)
        print(data)
        f.close()
        self.name = data['name']
        self.role = data['role']
        self.attributes = data['attributes']
        self.skills = data['skills']
        self.bodyTypeModifier = data['bodyTypeModifier']
        self.dmg_taken = 0

#character row e.g.: (2, 'Test', 'Solo', 6, 'average', 9, 9, 8, 8, 7, 8, 7, 5, 4)
    def __init__(self, row, skills):
        self.name = row['name']
        self.role = row['role']
        self.skills = skills
        self.attributes = {
            'INT': row['atr_int'],
            'REF': row['atr_ref'],
            'TECH': row['atr_tech'],
            'COOL': row['atr_cool'],
            'ATTR': row['atr_attr'],
            'MA': row['atr_ma'],
            'BODY': row['atr_body'],
            'LUCK': row['atr_luck'],
            'EMP': row['atr_emp']
        }
        self.dmg_taken = 0

    def rollSkill(self, skill, bonus):
        s = self.findSkill(skill)
        roll = 0
        if s is not None:
            atr = s['attribute']
            atr_bonus = self.attributes[atr]
            roll = dice.roll(1, 10)
            skill_bonus = s['value']
            result = roll + atr_bonus + skill_bonus

            return result


    def findSkill(self, skill):
        for s in self.skills:
            if s["skill"] == skill:
                return s
        return None

    def takeDmg(self, dmg: int):
        self.dmg_taken = self.dmg_taken + dmg
