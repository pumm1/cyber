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