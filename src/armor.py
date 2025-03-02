from colorama import Fore

from src.gameHelper import coloredText
from src.bonus import AtrBonus


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
            'ev': self.ev,
            'sp': self.sp,
            'bodyParts': self.body_parts,
            'attributeBonuses': self.atr_bonuses.asJson()
        }

        return resJson


    def toStr(self) -> str:
        return f'(id: {self.id}) {coloredText(Fore.LIGHTCYAN_EX, self.item)} ({self.sp} SP) - {self.body_parts}'
