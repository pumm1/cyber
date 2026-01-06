from src.gameHelper import woundStatePlain


class Initiative:
    def __init__(self, row):
        self.id = row['character_id']
        self.temp_character = row['temp_character']
        self.initiative = row['initiative']
        self.current = row['current']
        self.name = None
        self.condition = None
        self.bonus_initiative = 0
        self.bonus_turns = 0
        if self.id is not None:
            self.name = row['name']
            dmg_taken = row['dmg_taken']
            self.condition = woundStatePlain(dmg_taken)
            self.bonus_initiative = row['bonus_initiative']
            self.bonus_turns = row['bonus_turns']

    def asJson(self):
        name = self.name
        if  self.temp_character is not None:
            name = self.temp_character
        resJson = {
            'charId': self.id,
            'tempCharacter': self.temp_character,
            'name': name,
            'initiative': self.initiative,
            'current': self.current,
            'condition': self.condition,
            'bonusInitiative': self.bonus_initiative,
            'bonusTurns': self.bonus_turns
        }

        return resJson
