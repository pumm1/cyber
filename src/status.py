from gameHelper import  askInput
import cyberdao as DAO


status_pos = 'Positive'
status_neg = 'Negative'
status_neutral = 'Neutral'

valid_statuses = [status_neg, status_pos, status_neutral]

class Status:
    def __init__(self, row):
        self.id = row['id']
        self.status = row['status']
        self.effect = row['effect']
        self.statusType = row['status_type']

    def toStr(self):
        return f'(id: {self.id}) {self.status}: {self.effect} [{self.statusType}]'

    def asJson(self):
        json = {
            'id': self.id,
            'status': self.status,
            'effect': self.effect,
            'statusType': self.statusType
        }
        return json


def addStatus(character_id: int, status: str, effect: str, status_type: str):
    char = DAO.getCharacterById(character_id)
    if char is not None:
        DAO.addCharacterStatus(character_id, status, effect, status_type)


def addStatusManual(name):
    char = DAO.getCharacterByName(name)
    if char is not None:
        print(f'Give status: (e.g. drugged, stunned, psychosis, but can be anything else too)')
        status = askInput()
        print("Give brief description on status effect (e.g. can't move, -2 to some attribute etc.)")
        effect = askInput()
        print(f"Give statusType ({valid_statuses})")
        statusType = ''
        while True:
            statusType = askInput()
            if valid_statuses.__contains__(statusType):
                break
            else:
                print(f"Not valid status ({valid_statuses})")
        DAO.addCharacterStatus(char.id, status, effect, statusType)
        print('Status added')

def removeStatus(name, status_id):
    char = DAO.getCharacterByName(name)
    if char is not None:
        DAO.removeStatus(status_id, char.id)
