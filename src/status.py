from gameHelper import  askInput
import cyberdao as DAO

class Status:
    def __init__(self, row):
        self.id = row['id']
        self.status = row['status']
        self.effect = row['effect']

    def toStr(self):
        return f'(id: {self.id}) {self.status}: {self.effect}'


def addStatus(name):
    char = DAO.getCharacterByName(name)
    if char is not None:
        print(f'Give status: (e.g. drugged, stunned, psychosis, but can be anything else too)')
        status = askInput()
        print("Give brief description on status effect (e.g. can't move, -2 to some attribute etc.)")
        effect = askInput()
        DAO.addCharacterStatus(char.id, status, effect)
