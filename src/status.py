from src.gameHelper import askInput
import src.cyberdao as DAO
from src.logger import Log, log_neutral, log_event, log_neg, log_pos


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
