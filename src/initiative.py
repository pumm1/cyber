from src.gameHelper import woundStatePlain


class Initiative:
    def __init__(self, row):
        self.id = row['character_id']
        self.name = row['name']
        dmg_taken = row['dmg_taken']
        self.initiative = row['initiative']
        self.current = row['current']
        self.condition = woundStatePlain(dmg_taken)

    def asJson(self):
        resJson = {
            'charId': self.id,
            'name': self.name,
            'initiative': self.initiative,
            'current': self.current,
            'condition': self.condition
        }

        return resJson