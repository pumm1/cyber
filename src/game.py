import combat
import cyberdao as DAO
from collections import deque
import roles
import dice
import bodytypes
from gameInput import askInput

# TODO: explain e.g. reputation (1D10 + COOL + reputation (negative = minus)
# reputation table:
# 1 = anyone who was there knows
# 2 = stories have gottern around to immediate friends
# 3 = all your co-workres and casual acquaintances know
# 4 = stories are all over the local area
# 5 = your name is recognized by others beyond your local area
# 6 = you are known on sight by others beyond your local area
# 7 = a new story or two has been written about your exploits
# 8 = your exploits regularly make the headlines and screamsheets
# 9 = your exploits always make the screamsheets and TV
# 10 = you are known worldwide

split_at = ' '
roll_str = '/roll'
list_str = '/list'

exit_commands = ['/e', '/q', '/exit', '/quit']
help_commands = ['/help', '/halp', '/h']
rep_roll_str = 'rep'
add_char_str = '/add_char'
add_char_help_str = f'{add_char_str} <name>'
explain_str = '/explain'
add_reputation_str = '/add_rep'


def checkRollCommand(cmnd: str) -> bool:
    return cmnd.lower().startswith(roll_str)


def checkListCommand(cmnd: str) -> bool:
    return cmnd.lower().startswith(list_str)


def start():
    game_is_running = True
    while game_is_running:
        command = askInput().lower()
        if exit_commands.__contains__(command):
            print('< Disconnect >')
            game_is_running = False
        if help_commands.__contains__(command):
            help()
        if command.startswith(roll_str):
            match command.split(split_at):
                case [_, rep_roll_str, character]:
                    characterRoll(character, rep_roll_str)
                case _:
                    print('That roll is unknown or not supported yet')
        if command.startswith(add_char_str):
            match command.split(split_at):
                case [_, name]:
                    createCharacter(name)
                case _:
                    print(f'{add_char_str} <name>')
        if command.startswith(explain_str):
            print('TODO: add explanations for things')
        if command.startswith(add_reputation_str):
            match command.split(split_at):
                case [_, character, 'pos']:
                    addReputation(character, 1)
                case [_, character, 'neg']:
                    addReputation(character, -1)
                case _:
                    print('/add_rep <character> pos/neg')

        if command.startswith('/aci'):  # aci = advance combat initiative
            advanceCombatSeq()
        if command.startswith('/lci'):  # lci = list combat initiative
            listCombatInitiative()
        if command.startswith('/nci'):  # nci = new combat initiative, add to combat sequence
            match command.split(' '):
                case [_, character, initiative]:
                    addToCombat(character, int(initiative))
                case _:
                    print('/nci <character_name> <initiative>')
        if command.startswith('/cc'):  # cc = clear combat
            clearCombat()
        if command.startswith('/char'):
            match command.split(split_at):
                case [_, name]:
                    fetchCharacter(name)
                case _:
                    print('/char <name>')
        if command.startswith('/hit'):
            rollHitLocation()
        if command.startswith('/st'):  # TODO:
            match command.split(split_at):
                case [_]:
                    print('Need more values [/st <param>]')
                case [_, a]:
                    print('..better')
                case _:
                    print('default')


def safeCastToInt(text):
    val = 0
    try:
        val = int(text)
    except (ValueError, TypeError):
        val = 0
    return val


def addAttribute(attribute: str) -> int:
    print(f'<give val> or {roll_str} attribute {attribute} [1-10]')
    atr = 0
    while True:
        ans = askInput()
        if checkRollCommand(ans):
            atr = dice.roll(1, 10)
            break
        else:
            atr = safeCastToInt(ans)
            if 0 < atr <= 10:
                break
            else:
                print('Invalid attribute value')
    print(f'{attribute} = {atr}')
    return atr


def rollRole():
    roll = dice.roll(1, 10)
    if roll == 1:
        return roles.solo
    elif roll == 2:
        return roles.cop
    elif roll == 3:
        return roles.corp
    elif roll == 4:
        return roles.fixer
    elif roll == 5:
        return roles.nomad
    elif roll == 6:
        return roles.techie
    elif roll == 7:
        return roles.netrunner
    elif roll == 8:
        return roles.meditechie
    elif roll == 9:
        return roles.rocker
    else:
        return roles.media


def addRole():
    print(f'<give role> or {roll_str} random role. {list_str} to see info on roles')
    role = ''
    while True:
        ans = askInput()
        if checkListCommand(ans):
            print(*roles.allRoles, sep='\n')
        elif roles.allRoles.__contains__(ans):
            role = ans
            print(f'Selected {role}')
            break
        elif checkRollCommand(ans):
            role = rollRole()
            print(f'Rolled {role}')
            break
    return role


def addSpecial(role):
    specialAbility = roles.roleDict[role][roles.ability]
    specialDescr = roles.roleDict[role][roles.abilityDesc]
    skill = 0

    print(f'<give skill level> or {roll_str} random level for special ability {specialAbility} ({specialDescr})')
    while True:
        ans = askInput()
        if checkRollCommand(ans):
            skill = dice.roll(1, 10)
            print(f'Rolled {specialAbility} = {skill}')
            break
        else:
            res = safeCastToInt(ans)
            if 0 < res <= 10:
                skill = res
                print(f'Set {specialAbility} = {skill}')
                break
    return skill


def rollBodyType():
    body_type = ''
    roll = dice.roll(1, 6)
    if roll == 1:
        body_type = bodytypes.very_weak
    elif roll == 2:
        body_type == bodytypes.weak
    elif roll == 3:
        body_type = bodytypes.average
    elif roll == 4:
        body_type = bodytypes.strong
    elif roll == 5:
        body_type = bodytypes.very_strong
    else:  # superhuman only achievable by cybernetics
        body_type = rollBodyType()
    return body_type


def addBodyType():
    print(f'<give body type> or {roll_str} random body type ({list_str} to show all)')
    body_type = ''
    while True:
        ans = askInput()
        if checkListCommand(ans):
            bodytypes.listAvailableModifiers()
        elif checkRollCommand(ans):
            body_type = rollBodyType()
            break
        else:
            t_bod_type = bodytypes.checkBodyTypeFromStr(ans.lower())
            if t_bod_type is None:
                print(f'Invalid body type, see possible ones with {list_str}')
            elif t_bod_type == bodytypes.superhuman:
                print(print(f'Body type {bodytypes.superhuman} is only achievable through cybernetics'))
            else:
                body_type = t_bod_type
                break

    print(f'Body type modifier = {body_type}')
    return body_type


def createCharacter(name: str):
    role = addRole()
    special = addSpecial(role)
    body_Type = addBodyType()
    atr_int = addAttribute('INT')
    atr_ref = addAttribute('REF')
    atr_tech = addAttribute('TECH')
    atr_cool = addAttribute('COOL')
    atr_attr = addAttribute('ATTR')
    atr_luck = addAttribute('LUCK')
    atr_ma = addAttribute('MA')
    atr_body = addAttribute('BODY')
    atr_emp = addAttribute('EMP')
    DAO.addCharacter(
        name,
        role,
        special,
        body_Type,
        atr_int=atr_int,
        atr_ref=atr_ref,
        atr_tech=atr_tech,
        atr_cool=atr_cool,
        atr_attr=atr_attr,
        atr_luck=atr_luck,
        atr_ma=atr_ma,
        atr_body=atr_body,
        atr_emp=atr_emp
    )
    # TODO: next body type modifier


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
                command = askInput()
                if command.lower() == 'y':
                    print(f'What is {character.name} gaining reputation for?')
                    info = askInput()
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

def help():
    print('************ list of commands ************')
    list_str = ', '
    print('- Help:')
    print(list_str.join(help_commands))
    print('- Quit/Exit:')
    print(list_str.join(exit_commands))
    print('- Roll for something:')
    print(f'{roll_str} <{rep_roll_str}>')
    print('- Add new character:')
    print(add_char_help_str)
    print('- Explain something:')
    print(f'{explain_str} <term>')
    print('- Add reputation for character:')
    print(f'{add_reputation_str} <character_name> pos / neg')
