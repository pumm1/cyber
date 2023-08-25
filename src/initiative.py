class Initiative:
    def __init__(self, row):
        self.id = row['character_id']
        self.name = row['name']
        self.initiative = row['initiative']
        self.current = row['current']

    def asJson(self):
        resJson = {
            'charId': self.id,
            'name': self.name,
            'initiative': self.initiative,
            'current': self.current
        }

        return resJson