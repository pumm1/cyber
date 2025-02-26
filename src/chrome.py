from colorama import Fore

from src.gameHelper import coloredText
from src.bonus import AtrBonus, SkillBonus


class Chrome:
    def __init__(self, row, skill_bonus_rows):
        self.id = row['chrome_id']
        self.item = row['item']
        self.description = row['description']
        atr_bonuses = AtrBonus(row)
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

