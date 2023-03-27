from colorama import Fore

import combat
from collections import deque
import skills
from gameHelper import askInput, roll_str, split_at, add_char_str, exit_commands, help_commands, \
    explain_str, add_reputation_str, add_char_help_str, advance_combat_initiative_str, list_combat_initiative_str, \
    new_combat_initiative_str, new_combat_initiative_help_str, clear_combat_str, character_str, \
    character_helper_str, roll_help_str, stun_check_str, stun_check_help_str, dmg_str, safeCastToInt, dmg_helper_str, \
    roll_all_str, roll_atr_str, list_skills_str, list_skills_helper_str, lvl_up_skill_str, lvl_up_skill_help_str, \
    fumble_str, fumble_help_str, jam_str, jam_help_str, add_armor_str, add_armor_help_str, add_reputation_help_str, \
    list_rep_str, l_rep_help_str, add_event_str, add_weapon_str, add_weapon_help_str, attack_str, attack_help_str, \
    reload_str, reload_help_str, attack_type_single, attack_type_burst, attack_type_full_auto, list_event_str, \
    add_chrome_str, add_chrome_help_str, attack_type_melee, melee_dmg_str, melee_dmg_help_str, \
    suppressive_fire_def_help_str, suppressive_fire_def_str, askForRoll, medical_check_str, medical_check_help_str, \
    repair_sp_str, repair_sp_help_str, remove_armor_str, remove_armor_help_str, add_status_str, add_status_help_str, \
    help_info, heal_help_str, yes_no, heal_str, heal_calc_str, heal_calc_help_str, askInputCaseSensitive, \
    remove_status_help_str, remove_status_str, printGreenLine, fieldName, difficulty_check_str, coloredText, \
    notice_roll_str, notice_roll_help_str, add_character_for_notice_str, add_character_for_notice_help_str, \
    clear_notice_str
from characterBuilder import createCharacter
import fumble, armor, events, weapon, chrome, dice, cyberdao as DAO
import healing
import status
import notice


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
    printGreenLine('< Connected to the NET >')
    game_is_running = True
    while game_is_running:
        print('< Main >')
        command = askInput()
        command_parts = command.split(split_at)
        if exit_commands.__contains__(command):
            print('< Disconnect >')
            game_is_running = False
        elif help_commands.__contains__(command_parts[0]):
            match command_parts:
                case [_, 'combat']:
                    help('combat')
                case [_, 'modify']:
                    help('modify')
                case [_, 'info']:
                    help('info')
                case _:
                    help('all')

        elif command.startswith(roll_str):
            match command_parts:
                case [_, 'dice']:
                    (dice_num, die, bonus) = askForRoll()
                    res = dice.roll(dice_num, die) + bonus
                    print(f'Rolled {res}')
                case [_, 'face_off', character]:
                    faceOffRoll(character, roll=0)
                case [_, 'face_off', character, roll]:
                    faceOffRoll(character, roll)
                case [_, 'melee_def', name]:
                    skills.rollCharacterMeleeDef(name, roll=0)
                case [_, 'melee_def', name, roll]:
                    skills.rollCharacterMeleeDef(name, roll)
                case [_, 'hit_loc']:
                    location = combat.determineHitLocation()
                    print(f'Hit {location}')
                case [_, 'skill', name, skill]:
                    skills.rollCharacterSkill(name, skill, roll=0, modifier=0)
                case [_, 'skill', name, skill, roll]:
                    skills.rollCharacterSkill(name, skill, roll=roll, modifier=0)
                case[_, 'skill', name, skill, roll, modifier]:
                    skills.rollCharacterSkill(name, skill, roll=roll, modifier=modifier)
                case _:
                    print(roll_help_str)
        elif command.startswith(notice_roll_str):
            match command_parts:
                case [_, roll_to_beat]:
                    notice.quickNoticeCheckForCharacters(roll_to_beat)
                case _:
                    print(notice_roll_help_str)
        elif command.startswith(add_character_for_notice_str):
            match command_parts:
                case [_, name]:
                    notice.addCharacterToQuickNotice(name)
                case _:
                    print(add_character_for_notice_help_str)
        elif command.startswith(clear_notice_str):
            notice.clearQuickNotices()
        elif command.startswith(difficulty_check_str):
            print(skills.difficultyCheckInfo())
        elif command.startswith(lvl_up_skill_str):
            match command_parts:
                case [_, name, skill_id, update_amount]:
                    skills.updateCharSkill(name, skill_id, update_amount)
                case [_, name, skill_id]:
                    skills.updateCharSkill(name, skill_id, lvl_up_amount=1)
                case _:
                    print(lvl_up_skill_help_str)
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
            skills.listSkills(command_parts)
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
                    combat.stunCheck(name)
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
                case[_, name, dmg, 'fire']:
                    combat.hitCharacter(name, body_part='body', dmg_str=dmg, pass_sp=True)
                case [_, name, body_part, dmg]:
                    combat.hitCharacter(name, body_part, dmg)
                case [_, name, body_part, dmg, 'ap']:
                    combat.hitCharacter(name, body_part, dmg, is_ap=True)
                case _:
                    print(dmg_helper_str)
        elif command.startswith(melee_dmg_str):
            match command_parts:
                case [_, attacker_name]:
                    combat.handleMeleeDmg(attacker_name, 0)
                case [_, attacker_name, dmg]:
                    combat.handleMeleeDmg(attacker_name, dmg)
                case _:
                    print(f'{melee_dmg_help_str}')
        elif command.startswith(add_event_str):
            events.addEvent()
        elif command.startswith(list_event_str):
            events.listEvents()
        elif command.startswith(add_weapon_str):
            match command_parts:
                case [_, name]:
                    weapon.addChracterWeapon(name)
                case _:
                    print(add_weapon_help_str)
        elif command.startswith(add_chrome_str):
            match command_parts:
                case [_, name]:
                    chrome.addChrome(name)
                case _:
                    print(add_chrome_help_str)
        elif command.startswith(attack_str):
            match command_parts:
                case [_, name, 'melee']:
                    combat.characterAttack(name, attack_type_melee, range_str='1', given_roll=0)
                case [_, name, 'melee', roll]:
                    combat.characterAttack(name, attack_type_melee, range_str='1', given_roll=roll)
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
        elif command.startswith(suppressive_fire_def_str):
            match command_parts:
                case [_, name, rounds, area]:
                    combat.suppressiveFireDef(name, rounds, area)
                case _:
                    print(suppressive_fire_def_help_str)
        elif command.startswith(medical_check_str):
            match command_parts:
                case [_, name]:
                    healing.medicalCheck(name, given_roll=0)
                case [_, name, roll]:
                    healing.medicalCheck(name, given_roll=roll)
                case _:
                    print(medical_check_help_str)
        elif command.startswith(heal_calc_str):
            match command_parts:
                case [_, days]:
                    healing.calculateHealingAmount(days)
                case _:
                    print(heal_calc_help_str)
        elif command.startswith(heal_str):
            match command_parts:
                case [_, name, amount]:
                    healing.healCharacter(name, amount)
                case _:
                    print(heal_help_str)
        elif command.startswith(repair_sp_str):
            match command_parts:
                case [_, name]:
                    armor.repairSP(name)
                case _:
                    print(f'{repair_sp_help_str}')
        elif command.startswith(remove_armor_str):
            match command_parts:
                case [_, name, armor_id]:
                    armor.removeArmor(name, armor_id)
                case _:
                    print(f'{remove_armor_help_str}')
        elif command.startswith(add_status_str):
            match command_parts:
                case [_, name]:
                    status.addStatus(name)
                case _:
                    print(f'{add_status_help_str}')
        elif command.startswith(remove_status_str):
            match command_parts:
                case [_, name, status_id]:
                    status.removeStatus(name, status_id)
                case _:
                    print(remove_status_help_str)



def faceOffRoll(name, roll):
    character = DAO.getCharacterByName(name)
    if character is not None:
        res = character.rollFaceDown(roll)
        print(f'{character.name} face off result: {res}')


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
        print(f"Add {rep_type} reputation for {character.name}? {yes_no}")
        while tries < 3:
            command = askInput()
            if command == 'y':
                print(f'What is {character.name} gaining reputation for?')
                info = askInputCaseSensitive()
                DAO.addReputation(character.id, info, rep)
                printGreenLine(f'Reputation added for {character.name}')
                break
            elif command == 'n':
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
    characters_in_combat = len(rows)
    enough_in_combat = characters_in_combat > 1

    notInOrder = True
    notStarted = all(v['current'] == False for v in rows)
    if not enough_in_combat:
        print(f'Not enough characters in combat: {characters_in_combat}')
        notInOrder = False
    elif notStarted:
        notInOrder = False
        print('Starting combat sequence!')
        c = queue.pop()
        DAO.setNextInOrder(c['character_id'])
        printTurn(c['name'])

    while notInOrder:
        c = queue.pop()
        if c['current'] == True:
            next = queue.pop()
            queue.appendleft(c)
            queue.appendleft(next)
            notInOrder = False

            DAO.resetCurrentOrder()
            DAO.setNextInOrder(next['character_id'])
            printTurn(next['name'])
        else:
            queue.appendleft(c)


def clearCombat():
    DAO.clearCombat()


def addToCombat(name, initiative):
    character = DAO.getCharacterByName(name)
    if character is not None:
        DAO.addCharacterToCombat(character.id, initiative)
        print(f'{character.name} added to combat session')


#param = all/combat/info
def help(param):
    list_str = ', '

    help_str: str = f"""************ {coloredText(Fore.GREEN, 'list of commands')} ************
- {fieldName('Help')}:
{list_str.join(help_commands)}
{help_info}
- {fieldName('Quit / Exit')}
{list_str.join(exit_commands)}
- {fieldName('Roll for something')}
{roll_help_str}

"""

    combat_help = f"""
- {fieldName('Add new character to initiative sequence')}
{new_combat_initiative_help_str}
- {fieldName('List combat initiative')}
{list_combat_initiative_str}
- {fieldName('Advance combat initiative or start combat once initiatives have been added')}
{advance_combat_initiative_str}
- {fieldName('Clear combat sequence')}
{clear_combat_str}
- {fieldName('Reload weapon')}
{reload_help_str}
- {fieldName('Attack')}
{attack_help_str}
- {fieldName('Melee damage')}
{melee_dmg_help_str}
- {fieldName('Suppressive fire defence')}
{suppressive_fire_def_help_str}
- {fieldName('Medical check (for doctor)')}
{medical_check_help_str}
- {fieldName('Calculate healing amount for days recovered')}
{heal_calc_help_str}
- {fieldName('Healing (for patient)')}
{heal_help_str}"""

    info_help = f"""- {fieldName('See character info')}:
{character_helper_str}
- {fieldName('List character reputation')}
{l_rep_help_str}
- {fieldName('List skills (all | by attribute | by fuzzy logic | by character)')}
{list_skills_helper_str}
- {fieldName('See current stun check for character')}:
{stun_check_help_str}
- {fieldName('See fumble effect')}:
{fumble_help_str}
- {fieldName('Explain something')}:
{explain_str} <term>
- {fieldName('Add characters to quick notice check table')}
{add_character_for_notice_help_str}
- {fieldName('Roll quick notice check for all characters in the quick notice check table')}
{notice_roll_help_str}
- {fieldName('Clear quick notice check table')}
{clear_notice_str}
"""

    modify_help = f"""- {fieldName('Add new character')}:
{add_char_help_str}
- {fieldName('Add armor for character')}:
{add_armor_help_str}
- {fieldName('Add character skill')}:
{lvl_up_skill_help_str}
- {fieldName('Add reputation for character')}:
{add_reputation_help_str}
- {fieldName('New event log')}:
{add_event_str}
- {fieldName('Add weapon for character')}:
{add_weapon_help_str}
- {fieldName('Add chrome (not used as a weapon) for character')}:
{add_chrome_help_str}
- {fieldName('Repair character SP')}:
{repair_sp_help_str}
- {fieldName('Remove armor')}:
{remove_armor_help_str}
- {fieldName('Add status')}:
{add_status_help_str}
- {fieldName('Remove status')}:
{remove_status_help_str}"""

    if param == 'combat':
        help_str += combat_help
    elif param == 'info':
        help_str += info_help
    elif param == 'modify':
        help_str += modify_help
    else:
        help_str += info_help + modify_help + combat_help


    print(help_str)
