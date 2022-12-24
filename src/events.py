import db.cyberdao as DAO
from gameHelper import askInput

def addEvent():
    print(f'Describe event:')
    event = askInput()
    DAO.addEvent(event)

