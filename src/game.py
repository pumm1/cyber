import combat
import cyberdao as DAO
from collections import deque

def start():
    game_is_running = True
    while game_is_running:
        command = input("> ")
        if command == '/e' or command == '/q':
            print('exiting cyberpunk game')
            game_is_running = False
        if command.startswith('/aci'): #aci = advance combat initiative
            advanceCombatSeq()
        if command.startswith('/lci'): #lci = list combat initiative
            listCombatInitiative()
        if command.startswith('/nci'): #nci = new combat initiative
            match command.split(' '):
                case [_, character, initiative]:
                    addToCombat(character, int(initiative))
                case _:
                    print('/nci <character_name> <initiative>')
        if command.startswith('/cc'): #cc = clear combat
            clearCombat()
        if command.startswith('/char'):
            match command.split(' '):
                case [_, name]:
                    fetchCharacter(name)
                case _:
                    print('/char <name>')
        if command.startswith('/hit'):
            rollHitLocation()
        if command.startswith('/st'):
            match command.split(' '):
                case ['command']:
                    print('Need more values [/st <param>]')
                case ['command', a]:
                    print('..better')
                case _:
                    print('default')

def fetchCharacter(name):
    character = DAO.getCharacterByName(name)
    if character is None:
        print(f'Character not found by the name of {name}')
    else:
        character.info()

def rollHitLocation():
    location = combat.determineHitLocation()
    print(f'Hit the {location}')

def listCombatInitiative():
    rows = DAO.listCombatInitiative(ascending=False)
    infoRows = map(lambda c: (
        f"{c['character']}: initiative: {c['initiative']}, currenet: {c['current']}"
    ), rows)
    info = '\n'.join(infoRows)
    print(f"Turn order: \n{info}")

def advanceCombatSeq():
    rows = DAO.listCombatInitiative(ascending=True)
    queue = deque(rows)
    #print(f'type tof rows: {type(rows)} ... type of arrRows: {type(arr_rows)}')
    notInOrder = True
    print('... testing automated ordering')
    while notInOrder:
        print(f'... loop {queue}')
        c = queue.pop()
        if c['current'] == True:
            next = queue.pop()
            queue.appendleft(c)
            queue.appendleft(next)
            notInOrder = False

            DAO.resetCurrentOrder()
            DAO.setNextInOrder(next['character'])
            print(f"{next['character']}'s turn")
        else:
            queue.appendleft(c)
            print(f'{c} is not in turn')

def clearCombat():
    DAO.clearCombat()
def addToCombat(character, initiative):
    DAO.addCharacterToCombat(character, initiative)