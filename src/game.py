import combat
from db import cyberdao as DAO
from collections import deque
import skills
from gameHelper import askInput, roll_str, split_at, add_char_str, rep_roll_str, exit_commands, help_commands, \
    explain_str, add_reputation_str, add_char_help_str, advance_combat_initiative_str, list_combat_initiative_str, \
    new_combat_initiative_str, new_combat_initiative_help_str, clear_combat_str, character_str, \
    character_helper_str, roll_help_str, stun_check_str, stun_check_help_str, dmg_str, safeCastToInt, dmg_helper_str, \
    roll_all_str, roll_atr_str, list_skills_str, list_skills_helpeer_str, add_char_skill_str, add_char_skill_help_str, \
    fumble_str, fumble_help_str, jam_str, jam_help_str, add_armor_str, add_armor_help_str, add_reputation_help_str, \
    list_rep_str, l_rep_help_str, add_event_str, add_weapon_str, add_weapon_help_str, attack_str, attack_help_str, \
    reload_str, reload_help_str, attack_type_single, attack_type_burst, attack_type_full_auto
from characterBuilder import createCharacter
from src import fumble, armor, events, weapon


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
    print('< Connected to the NET >')
    game_is_running = True
    while game_is_running:
        print('< Main >')
        command = askInput().lower()
        command_parts = command.split(split_at)
        if exit_commands.__contains__(command):
            print('< Disconnect >')
            game_is_running = False
        elif help_commands.__contains__(command):
            help()
        elif command.startswith(roll_str):
            match command_parts:
                case [_, 'face_off', character]:
                    faceOffRoll(character, rep_roll_str)
                case [_, 'hit_loc']:
                    location = combat.determineHitLocation()
                    print(f'Hit {location}')
                case [_, 'char', name, skill]:
                    skills.rollCharacterSkill(name, skill, modifier=0)
                case [_, 'char', name, skill, modifier]:
                    skills.rollCharacterSkill(name, skill, modifier=modifier)
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
                    createCharacter(name, roll_all=False, roll_atr=False)
                case [_, name, roll_param]:
                    if roll_param == roll_all_str:
                        createCharacter(name, roll_all=True)
                    elif roll_param == roll_atr_str:
                        createCharacter(name, roll_atr=True)
                case _:
                    print(add_char_help_str)
        elif command.startswith(add_armor_str):
            match command_parts:
                case [_, name]:
                    armor.addArmorForCharacter(name)
                case _:
                    print(f'{add_armor_help_str}')
        elif command.startswith(fumble_str):
            match command_parts:
                case [_, area]:
                    fumble.rollFumble(area)
                case _:
                    print(fumble_help_str)
        elif command.startswith(jam_str):
            match command_parts:
                case [_, reliability]:
                    fumble.rollWeaponJam(reliability)
                case _:
                    print(jam_help_str)
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
                case [_, character, amount]:
                    addReputation(character, amount)
                case _:
                    print(f'{add_reputation_help_str}')
        elif command.startswith(list_rep_str):
            match command_parts:
                case [_, name]:
                    listCharacterRep(name)
                case _:
                    print(f'{l_rep_help_str}')
        elif command.startswith(advance_combat_initiative_str):
            advanceCombatSeq()
        elif command.startswith(list_combat_initiative_str):
            listCombatInitiative()
        elif command.startswith(new_combat_initiative_str):  # nci = new combat initiative, add to combat sequence
            match command_parts:
                case [_, name, initiative]:
                    addToCombat(name, int(initiative))
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
                case [_, name, body_part, dmg]:
                    combat.hitCharacter(name, body_part, dmg)
                case _:
                    print(dmg_helper_str)
        elif command.startswith(add_event_str):
            events.addEvent()
        elif command.startswith(add_weapon_str):
            match command_parts:
                case [_, name]:
                    weapon.addChracterWeapon(name)
                case _:
                    print(add_weapon_help_str)
        elif command.startswith(attack_str):
            match command_parts:
                case [_, name, 'burst', range]:
                    combat.characterAttack(name, attack_type_burst, range, given_roll=0)
                case [_, name, 'burst', range, roll]:
                    combat.characterAttack(name, attack_type_burst, range, given_roll=roll)
                case [_, name, 'single', range]:
                    combat.characterAttack(name, attack_type_single, range, given_roll=0)
                case [_, name, 'single', range, roll]:
                    combat.characterAttack(name, attack_type_single, range, given_roll=roll)
                case [_, name, 'fa']:
                    combat.characterAttack(name, attack_type_full_auto, range_str='99', given_roll=0)
                case _:
                    print(f'{attack_help_str}')
        elif command.startswith(reload_str):
            match command_parts:
                case [_, weapon_id, shots]:
                    combat.reloadWeapon(weapon_id, shots)
                case _:
                    print(f'{reload_help_str}')


def faceOffRoll(name, roll):
    character = DAO.getCharacterByName(name)
    if character is None:
        print(f'Character not found by the name of {name}')
    else:
        print(f'{character.name} face off result: {character.rollFaceDown()}')


def fetchCharacter(name):
    character = DAO.getCharacterByName(name)
    if character is None:
        print(f'Character not found by the name of {name}')
    else:
        character.info()


def listCombatInitiative():
    rows = DAO.listCombatInitiative(ascending=False)
    infoRows = map(lambda c: (
        f"{c['name']}: initiative: {c['initiative']}, current: {c['current']}"
    ), rows)
    info = '\n'.join(infoRows)
    print(f"Turn order: \n{info}")


def addReputation(char, rep_amount):
    rep = safeCastToInt(rep_amount)
    character = DAO.getCharacterByName(char)
    rep_type = 'positive'
    if rep < 0:
        rep_type = 'negative'
    if character is not None:
        tries = 0
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


def listCharacterRep(name):
    c = DAO.getCharacterByName(name)
    if c is not None:
        rep_rows = DAO.getReputationRows(c.id)
        print(f'{c.name} is known for:')
        for rep in rep_rows:
            print(f"{rep['known_for']} (level: {rep['rep_level']})")


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


def addToCombat(name, initiative):
    character = DAO.getCharacterByName(name)
    if character is not None:
        DAO.addCharacterToCombat(character.id, initiative)
        print(f'{character.name} added to combat session')

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
-See fumble effect:
{fumble_help_str}
- See character info:
{character_helper_str}
- Add new character:
{add_char_help_str}
- Add armor for character:
{add_armor_help_str}
- List skills (all | by attribute | by fuzzy logic | by character)
{list_skills_helpeer_str}
- Add character skill:
{add_char_skill_help_str}
- Explain something:
{explain_str} <term>
- Add reputation for character:
{add_reputation_help_str}
- List character reputation:
{l_rep_help_str}
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
- New event log:
{add_event_str}
- Add weapon for character:
{add_weapon_help_str}
- Reload weapon:
{reload_help_str}
"""
          )


