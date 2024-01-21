from gameHelper import askInput
import cyberdao as DAO
from logger import Log, log_neutral, log_event, log_neg, log_pos


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
        l_type = log_neg
        if status_type == status_pos:
            l_type = log_pos
        elif status_type == status_neutral:
            l_type = log_neutral
        logs = log_event(list(), f'Status {status} added for {char.name}', l_type)
        return logs



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


def removeStatusByCharId(charcter_id, status_id):
    char = DAO.getCharacterById(charcter_id)
    logs = []
    if char is not None:
        status_row = DAO.getCharacterStatusById(status_id, charcter_id)
        if status_row is not None:
            status = status_row['status']
            DAO.removeStatus(status_id, char.id)
            logs = log_event(logs, f'Status {status} removed from {char.name}', log_neutral)
        else:
            logs = log_event(logs, f'Status not found', log_neg)

    return logs

def removeStatusByCharName(name, status_id):
    char = DAO.getCharacterByName(name)
    if char is not None:
        DAO.removeStatus(status_id, char.id)
        print('Status removed')
