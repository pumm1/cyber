from src.gameHelper import woundStatePlain


class Initiative:
    def __init__(self, row):
        self.id = row['character_id']
        self.name = row['name']
        dmg_taken = row['dmg_taken']
        self.initiative = row['initiative']
        self.current = row['current']
        self.condition = woundStatePlain(dmg_taken)
        self.bonus_turns = row['bonus_turns']
        self.bonus_initiative = row['bonus_initiative']

    def asJson(self):
        resJson = {
            'charId': self.id,
            'name': self.name,
            'initiative': self.initiative,
            'current': self.current,
            'condition': self.condition,
            'bonusInitiative': self.bonus_initiative,
            'bonusTurns': self.bonus_turns
        }

        return resJson
