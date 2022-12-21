import combat
import cyberdao as DAO
from collections import deque

#TODO: explain e.g. reputation (1D10 + COOL + reputation (negative = minus)
#reputation table:
#1 = anyone who was there knows
#2 = stories have gottern around to immediate friends
#3 = all your co-workres and casual acquaintances know
#4 = stories are all over the local area
#5 = your name is recognized by others beyond your local area
#6 = you are known on sight by others beyond your local area
#7 = a new story or two has been written about your exploits
#8 = your exploits regularly make the headlines and screamsheets
#9 = your exploits always make the screamsheets and TV
#10 = you are known worldwide

split_at = ' '
def start():
    game_is_running = True
    while game_is_running:
        command = input("> ")
        if command == '/e' or command == '/q':
            print('< Disconnect >')
            game_is_running = False
        if command.startswith('/roll'):
            match command.split(split_at):
                case [_, 'rep', character]:
                    characterRoll(character, 'rep')
                case _:
                    print('That roll is unknown or not supported yet')
        if command.startswith('/explain'):
            print('TODO: add epxlanations for things')
        if command.startswith('/add_rep'):
            match command.split(split_at):
                case [_, character, 'pos']:
                    addReputation(character, 1)
                case [_, character, 'neg']:
                    addReputation(character, -1)
                case _:
                    print('/add_rep <character> pos/neg')

        if command.startswith('/aci'): #aci = advance combat initiative
            advanceCombatSeq()
        if command.startswith('/lci'): #lci = list combat initiative
            listCombatInitiative()
        if command.startswith('/nci'): #nci = new combat initiative, add to combat sequence
            match command.split(' '):
                case [_, character, initiative]:
                    addToCombat(character, int(initiative))
                case _:
                    print('/nci <character_name> <initiative>')
        if command.startswith('/cc'): #cc = clear combat
            clearCombat()
        if command.startswith('/char'):
            match command.split(split_at):
                case [_, name]:
                    fetchCharacter(name)
                case _:
                    print('/char <name>')
        if command.startswith('/hit'):
            rollHitLocation()
        if command.startswith('/st'): #TODO:
            match command.split(split_at):
                case [_]:
                    print('Need more values [/st <param>]')
                case [_, a]:
                    print('..better')
                case _:
                    print('default')

def characterRoll(name, roll):
    character = DAO.getCharacterByName(name)
    if character is None:
        print(f'Character not found by the name of {name}')
    else:
        match roll:
            case 'rep':
                print(f'{character.name} face off result: {character.rollFaceDown()}')
            case unknown:
                print(f'Command {unknown} is not known or not yet supported')

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

def addReputation(char, rep):
    character = DAO.getCharacterByName(char)
    rep_type = 'positive'
    if rep < 0:
        rep_type = 'negative'
    if character is not None:
        tries = 0
        rep_rows = DAO.getReputationRows(character.id)
        if len(rep_rows) >= 10:
            print('Max rep of 10 reached already')
        else:
            print(f"Add {rep_type} reputation for {character.name}? [y/n]")
            while tries < 3:
                command = input("> ")
                if command.lower() == 'y':
                    print(f'What is {character.name} gaining reputation for?')
                    info = input("> ")
                    DAO.addReputation(character.id, info, rep)
                    print(f'Reputation added for {character.name}')
                    break
                elif command.lower() == 'n':
                    print(f'Cancelling reputation add for {character.name}')
                    break
                tries = tries + 1
    else:
        print(f'Character not found by name {char}')


def advanceCombatSeq():
    def printTurn(character):
        print(f"{character}'s turn!")

    rows = DAO.listCombatInitiative(ascending=True)
    queue = deque(rows)
    notInOrder = True
    notStarted = all(v['current'] == False for v in rows)
    if notStarted:
        notInOrder = False
        print('Starting combat sequence!')
        c = queue.pop()
        DAO.setNextInOrder(c['character'])
        printTurn(c['character'])

    while notInOrder:
        c = queue.pop()
        if c['current'] == True:
            next = queue.pop()
            queue.appendleft(c)
            queue.appendleft(next)
            notInOrder = False

            DAO.resetCurrentOrder()
            DAO.setNextInOrder(next['character'])
            printTurn(next['character'])
        else:
            queue.appendleft(c)

def clearCombat():
    DAO.clearCombat()
def addToCombat(character, initiative):
    DAO.addCharacterToCombat(character, initiative)