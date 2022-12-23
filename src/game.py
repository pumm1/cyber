import combat
import cyberdao as DAO
from collections import deque
import skills
from gameHelper import askInput, roll_str, split_at, add_char_str, rep_roll_str, exit_commands, help_commands, \
    explain_str, add_reputation_str, add_char_help_str, advance_combat_initiative_str, list_combat_initiative_str, \
    new_combat_initiative_str, new_combat_initiative_help_str, clear_combat_str, character_str, \
    character_helper_str, roll_help_str, stun_check_str, stun_check_help_str, dmg_str, safeCastToInt, dmg_helper_str, \
    roll_all_str, roll_atr_str, list_skills_str, list_skills_helpeer_str, add_char_skill_str, add_char_skill_help_str
from characterBuilder import createCharacter


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

def start():
    game_is_running = True
    while game_is_running:
        command = askInput().lower()
        command_parts = command.split(split_at)
        if exit_commands.__contains__(command):
            print('< Disconnect >')
            game_is_running = False
        elif help_commands.__contains__(command):
            help()
        elif command.startswith(roll_str):
            match command_parts:
                case [_, 'rep', character]:
                    characterRoll(character, rep_roll_str)
                case [_, 'hit_loc']:
                    rollHitLocation()
                case [_, 'char', name, skill]:
                    skills.rollCharacterSkill(name, skill)
                case _:
                    print(roll_help_str)
        elif command.startswith(add_char_skill_str):
            match command_parts:
                case [_, name, skill_id, skill_level]:
                    skills.addCharacterSkill(name, skill_id, skill_level)
                case _:
                    print(add_char_skill_help_str)
        elif command.startswith(add_char_str):
            match command_parts:
                case [_, name]:
                    createCharacter(name)
                case [_, name, roll_param]:
                    if roll_param == roll_all_str:
                        createCharacter(name, roll_all=True)
                    elif roll_param == roll_atr_str:
                        createCharacter(name, roll_atr=True)
                case _:
                    print(add_char_help_str)
        elif command.startswith(list_skills_str):
            match command_parts:
                case [_]:
                    skills.listAllSkills()
                case [_, 'atr', atr]:
                    skills.listSkillsByAttribute(atr)
                case [_, 'fuzzy', str]:
                    skills.findSkillsByString(str)
                case [_, 'char', name]:
                    skills.printCharacterSkills(name)
        elif command.startswith(explain_str):
            print('TODO: add explanations for things')
        elif command.startswith(add_reputation_str):
            match command_parts:
                case [_, character, 'pos']:
                    addReputation(character, 1)
                case [_, character, 'neg']:
                    addReputation(character, -1)
                case _:
                    print('/add_rep <character> pos/neg')

        elif command.startswith(advance_combat_initiative_str):
            advanceCombatSeq()
        elif command.startswith(list_combat_initiative_str):
            listCombatInitiative()
        elif command.startswith(new_combat_initiative_str):  # nci = new combat initiative, add to combat sequence
            match command_parts:
                case [_, character, initiative]:
                    addToCombat(character, int(initiative))
                case _:
                    print(new_combat_initiative_help_str)
        elif command.startswith(clear_combat_str):  # cc = clear combat
            clearCombat()
        elif command.startswith(stun_check_str):
            match command_parts:
                case [_, name]:
                    stunCheckCharacter(name)
                case _:
                    print(stun_check_help_str)
        elif command.startswith(character_str):
            match command_parts:
                case [_, name]:
                    fetchCharacter(name)
                case _:
                    print(character_helper_str)
        elif command.startswith(dmg_str):
            match command_parts:
                case [_, name, dmg]:
                    dmgCharacter(name, dmg)
                case _:
                    print(dmg_helper_str)



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
        f"{c['character']}: initiative: {c['initiative']}, current: {c['current']}"
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

def dmgCharacter(name, dmg_str):
    dmg = safeCastToInt(dmg_str)
    character = DAO.getCharacterByName(name)
    if character is not None:
        combat.damageCharacter(character, dmg)
def stunCheckCharacter(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        combat.stunCheck(character)

def help():
    list_str = ', '
    print(f"""************ list of commands ************
- Help:
{list_str.join(help_commands)}
- Quit/Exit:
{list_str.join(exit_commands)}
- Roll for something:
{roll_help_str}
- See character info:
{character_helper_str}
- Add new character:
{add_char_help_str}
- List skills (all | by attribute | by fuzzy logic | by character)
{list_skills_helpeer_str}
- Explain something:
{explain_str} <term>
- Add reputation for character:
{add_reputation_str} <character_name> pos / neg
- See current stun check for character:
{stun_check_help_str}
- Add new character to initiative sequence:
{new_combat_initiative_help_str}
- List combat initiative:
{list_combat_initiative_str}
- Advance combat initiative or start combat once initiatives have been added:
{advance_combat_initiative_str}
- Clear combat sequence:
{clear_combat_str}

"""
          )


