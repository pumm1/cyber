import cyberdao as DAO
from gameHelper import askInput

def addEvent():
    print(f'Describe event:')
    event = askInput()
    DAO.addEvent(event)

def listEvents():
    events = DAO.listEvents()
    for row in events:
        print(f" - {row['event']}")

