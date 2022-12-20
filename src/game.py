import dice
import combat
import cyberdao as DAO

def start():
    game_is_running = True
    while game_is_running:
        command = input("> ")
        if command == '/e' or command == '/q':
            print('exiting cyberpunk game')
            game_is_running = False
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
    rows = DAO.listCombatInitiative()
    cleaned_rows = map(lambda c: (
        c['character'], {'i': c['initiative'], 'is_next': c['current']}
    ), rows)
    combat_order = dict(cleaned_rows)

    print(f'Combat order: \n{combat_order}')
def clearCombat():
    DAO.clearCombat()
def addToCombat(character, initiative):
    DAO.addCharacterToCombat(character, initiative)