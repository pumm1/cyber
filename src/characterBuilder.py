import random

import dice
import cyberdao as DAO
import roles
import bodytypes
from gameHelper import askInput, checkRollCommand, checkListCommand, safeCastToInt, roll_str, list_str, INT, REF, TECH, \
    COOL, ATTR, LUCK, MA, BODY, EMP, body_part_l_arm, body_part_body, body_part_head, body_part_r_arm, t_melee, \
    t_handgun, t_shotgun, t_rifle, t_thrown, t_smg, con_pocket, con_long_coat, con_jacket, not_hideable, yes_no, \
    body_part_l_leg, body_part_r_leg, printGreenLine, printRedLine, wep_standard_reliability
from logger import log_event, log_pos
from skills import udpateCharacterSkill
from roles import role_skills, role_guns, role_armors
from weapon import addCharacterWeaponById
from armor import addArmorForCharacter
from chrome import addChromeByCharacterId


def rollAtr():
    atr = dice.roll(2, 3) + dice.roll(2,2)
    return atr


def addAttribute(attribute: str) -> int:
    print(f'<give val> or {roll_str} attribute {attribute} [1-10]')
    atr = 0
    while True:
        ans = askInput()
        if checkRollCommand(ans):
            atr = rollAtr()
            break
        else:
            atr = safeCastToInt(ans)
            if 0 < atr <= 10:
                break
            else:
                print('Invalid attribute value')
    print(f'{attribute} = {atr}')
    return atr


def addRole():
    print(f'<give role num> or {roll_str} random role. {list_str} to see info on roles')
    role = manualRole(allow_roll=True)
    return role


def manualRole(allow_roll: bool):
    role = ''
    while True:
        ans = askInput()
        ans_idx = safeCastToInt(ans)
        if checkListCommand(ans):
            for role in roles.allRoles:
                idx = roles.allRoles.index(role)
                print(f'{idx + 1} - {role}')
        elif 0 < ans_idx <= len(roles.allRoles):
            role = roles.allRoles[ans_idx - 1]
            print(f'Selected {role}')
            break
        elif allow_roll and checkRollCommand(ans):
            role = rollRole()

            break
    return role


def rollSpecial(role):
    specialAbility = roles.roleDict[role][roles.ability]

    skill = dice.roll(1, 5)
    print(f'Rolled {specialAbility} = {skill}')
    return skill


def generateRandomSkillsAndGear(character_id):
    character = DAO.getCharacterById(character_id)
    if character is not None:
        generateSkills(character)
        generateWeapons(character)
        generateArmors(character)


def generateArmors(character):
    armors_of_role = roles.roleDict[character.role][roles.role_armors]
    possible_amount_of_armors = len(armors_of_role)
    armors_to_add = dice.roll(1, possible_amount_of_armors) - 1 #allow 0
    armors_to_add_indices = []
    while len(armors_to_add_indices) < armors_to_add:
        idx = random.randint(0, possible_amount_of_armors - 1)
        if not armors_to_add_indices.__contains__(idx):
            armors_to_add_indices.append(idx)
            armor = armors_of_role[idx]
            addArmorForCharacter(
                character,
                item=armor[roles.armor_name_str],
                ev=armor[roles.ev_str],
                humanity_cost=armor[roles.humanity_cost_str],
                sp=armor[roles.sp_str],
                covered_parts=armor[roles.covered_parts_str],
                atr_bonuses=armor[roles.atr_bonuses_str],
                skill_bonuses_dict=armor[roles.skill_bonuses_str]
            )


def generateWeapons(character):
    weps_of_role = roles.roleDict[character.role][role_guns]
    possible_amount_of_guns = len(weps_of_role)
    guns_to_add = dice.roll(1, possible_amount_of_guns)
    guns_to_add_indices = []
    while len(guns_to_add_indices) < guns_to_add:
        idx = random.randint(0, guns_to_add - 1)
        if not guns_to_add_indices.__contains__(idx):
            guns_to_add_indices.append(idx)
            wep = weps_of_role[idx]
            addCharacterWeaponById(
                character_id=character.id,
                dice=wep[roles.dice_str],
                die=wep[roles.die_str],
                divide_by=wep[roles.divide_by_str],
                bonus=wep[roles.bonus_str],
                weapon_name=wep[roles.weapon_name_str],
                clip_size=wep[roles.clip_size_str],
                rof=wep[roles.rof_str],
                humanity_cost=wep[roles.humanity_cost_str],
                weapon_t=wep[roles.weapon_type_str],
                wa=wep[roles.wa_str],
                con=wep[roles.con_str],
                weight=wep[roles.weight_str],
                reliability=wep[roles.reliability_str],
                effect_radius=wep[roles.effect_radius_str],
                custom_range=wep[roles.custom_range_str]
            )


def generateSkills(character):
    basic_skills = ['awareness', 'library search', 'athletics', 'dodge/escape', 'brawling', 'handgun',
                    'melee']  # this requires DB to be set as instructed
    char_role_skills = roles.roleDict[character.role][role_skills]
    all_skills = basic_skills + char_role_skills
    for skill in all_skills:
        skill = DAO.skillByName(skill)
        if skill is not None:
            skill_id = skill['id']
            lvl_up_amount = dice.roll(1, 5)
            udpateCharacterSkill(character, skill_id, lvl_up_amount)
        else:
            printRedLine(f'{skill} not found!')


def addSpecial(role):
    specialAbility = roles.roleDict[role][roles.ability]
    specialDescr = roles.roleDict[role][roles.abilityDesc]
    skill = 0

    print(f'<give skill level> or {roll_str} random level for special ability {specialAbility} ({specialDescr})')
    while True:
        ans = askInput()
        if checkRollCommand(ans):
            skill = rollSpecial(role)
            break
        else:
            res = safeCastToInt(ans)
            if 0 < res <= 10:
                skill = res
                print(f'Set {specialAbility} = {skill}')
                break
    return skill


def rollBodyType():
    body_type = dice.roll(1, 5) - 1
    return body_type


def addBodyType(given_body_type=None) -> int:
    print(f'<give body type> or {roll_str} random body type ({list_str} to show all)')
    body_type = 0
    if given_body_type is not None:
        ans = given_body_type
        body_type = safeCastToInt(ans)
        if body_type > 4:
            print(print(f'Body type {bodytypes.superhuman} is only achievable through cybernetics'))
            body_type = 0
    else:
        body_type = handleManualBodyType()
    print(f'Body type modifier = {body_type} ({bodytypes.bodyTypeModifiersByValue(body_type)})')
    return body_type

def handleManualBodyType():
    body_type = None
    while True:
        ans = askInput()
        if checkListCommand(ans):
            bodytypes.listAvailableModifiers()
        elif checkRollCommand(ans):
            body_type = rollBodyType()
            break
        else:
            body_type_value = safeCastToInt(ans)
            print(f'.... ans: {ans} vs body_type_value {body_type_value}')
            if body_type_value > 4:
                print(print(f'Body type {bodytypes.superhuman} is only achievable through cybernetics'))
            else:
                body_type = body_type_value
                break

    return body_type

def handleRole(is_random: bool):
    role = ''
    if is_random:
        role = rollRole()
    else:
        role = addRole()
    return roles


def createCharacter(name: str, roll_all=False, roll_atr=False):
    if roll_all:
        print('Generating random character')
        createRandomCharacter(name)
    elif roll_atr:
        createCharacterWithRandomAtr(name)
    else:
        createManualCharacter(name)


def createCharacterWithRandomAtr(name):
    role = addRole()
    special = addSpecial(role)
    body_Type = addBodyType()
    (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp) = rollAtributes()
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


def createRandomCharacter(name, generate_gear=True):
    role = rollRole()
    special = rollSpecial(role)
    body_type = rollBodyType()
    (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp) = rollAtributes()
    character_id = DAO.addCharacter(
        name,
        role,
        special,
        body_type,
        atr_int=atr_int,
        atr_ref=atr_ref,
        atr_tech=atr_tech,
        atr_cool=atr_cool,
        atr_attr=atr_attr,
        atr_luck=atr_luck,
        atr_ma=atr_ma,
        atr_body=atr_body,
        atr_emp=atr_emp,
    )
    if generate_gear:
        generateGear(name)
    generateRandomSkillsAndGear(character_id)
    return character_id


low_q_armor_set = [
    {'item': 'vest', 'body_parts': [body_part_body], 'sp': 10, 'ev': 0},
    {'item': 'helmet', 'body_parts': [body_part_head], 'sp': 10, 'ev': 0}
]

mid_q_armor_set = [
    {'item': 'flak jacket', 'body_parts': [body_part_body, body_part_l_arm, body_part_r_arm], 'sp': 15, 'ev': 0},
    {'item': 'helmet', 'body_parts': [body_part_head], 'sp': 10, 'ev': 0}
]

high_q_armor_set = [
    {'item': 'combat armor', 'body_parts': [body_part_body, body_part_l_arm, body_part_r_arm, body_part_l_leg, body_part_r_leg], 'sp': 20, 'ev': 1},
    {'item': 'combat helmet', 'body_parts': [body_part_head], 'sp': 20, 'ev': 0}
]

low_q_melee_set = [
    {'item': 'Rippers', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 3,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'wa': 0, 'con': con_pocket,  'reliability': 'ST',
     'effect_radius': 0, 'weight': 1}
]

mid_q_melee_set = [
    {'item': 'Slice n dice', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 2, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'wa': 0, 'con': con_pocket,  'reliability': 'ST',
     'effect_radius': 0, 'weight': 1},
    {'item': 'Cybersnake',
     'weapon_type': t_melee, 'is_chrome': True,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'wa': 0, 'con': con_long_coat,  'reliability': 'ST',
     'effect_radius': 0, 'weight': 1}
]

high_q_melee_set = [
    {'item': 'Wolvers', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 3, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'wa': 0, 'con': con_pocket,  'reliability': 'ST',
     'effect_radius': 0, 'weight': 1},
    {'item': 'Cybersnake 1', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'wa': 0, 'con': con_long_coat,  'reliability': 'ST',
     'effect_radius': 0, 'weight': 1},
    {'item': 'Cybersnake 2', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'wa': 0, 'con': con_long_coat,  'reliability': 'ST',
     'effect_radius': 0, 'weight': 1}
]

low_q_gun_set = [
    {'item': 'Colt .45', 'is_chrome': False,
     'weapon_type': t_handgun,
     'dice_number': 2, 'dice_dmg': 6, 'dmg_bonus': 3,
     'range': 50, 'rof': 2, 'clip_size': 6, 'shots_left': 6,
     'wa': 0, 'con': con_jacket,  'reliability': 'ST',
     'effect_radius': 0, 'weight': 1}
]

mid_q_gun_set1 = [
    {'item': 'Double barrel shotgun', 'is_chrome': False,
     'weapon_type': t_shotgun,
     'dice_number': 4, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 50, 'rof': 1, 'clip_size': 2, 'shots_left': 2,
     'wa': -1, 'con': con_long_coat,  'reliability': 'UR',
     'effect_radius': 0, 'weight': 1},
    {'item': 'Molotov cocktail', 'is_chrome': False,
     'weapon_type': t_thrown,
     'dice_number': 2, 'dice_dmg': 10, 'dmg_bonus': 0,
     'range': 30, 'rof': 1, 'clip_size': 1, 'shots_left': 1,
     'wa': 0, 'con': con_jacket, 'reliability': 'ST',
     'effect_radius': 0, 'weight': 1},
]

mid_q_gun_set2 = [
    {'item': 'Uzi', 'is_chrome': False,
     'weapon_type': t_smg,
     'dice_number': 2, 'dice_dmg': 6, 'dmg_bonus': 1,
     'range': 50, 'rof': 35, 'clip_size': 30, 'shots_left': 30,
     'wa': 0, 'con': con_jacket,  'reliability': 'VR',
     'effect_radius': 0, 'weight': 1},
]

high_q_gun_set = [
    {'item': 'Militech Ronin Lt. AR', 'is_chrome': False,
     'weapon_type': t_rifle,
     'dice_number': 5, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 400, 'rof': 35, 'clip_size': 30, 'shots_left': 30,
     'wa': 1, 'con': not_hideable, 'reliability': 'VR',
     'effect_radius': 0, 'weight': 1},
    {'item': 'Frag. Grenade', 'is_chrome': False,
     'weapon_type': t_thrown,
     'dice_number': 3, 'dice_dmg': 10, 'dmg_bonus': 0,
     'range': 30, 'rof': 1, 'clip_size': 1, 'shots_left': 1,
     'wa': 0, 'con': con_pocket,  'reliability': 'ST',
     'effect_radius': 5, 'weight': 2},
]



def generateGear(name):
    print(f'Generate gear? {yes_no}')
    gen_gear = False
    while True:
        i = askInput()
        if i == 'y':
            gen_gear = True
            break
        elif i == 'n':
            break
    if gen_gear:
        char = DAO.getCharacterByName(name)
        if char is not None:
            add_gear = True
            while add_gear:
                print(
                    f'Armor/weapon and quality? [a/w]-[1-3] (e.g. a-1 for low quality armor, w-3 for high quality weapon)')
                print('Stop adding gear with -1')
                i = askInput()
                if i == '-1':
                    add_gear = False
                else:
                    gear = i.split('-')
                    q = 0
                    match gear:
                        case ['a', quality]:
                            q = safeCastToInt(quality)
                            if q == 1:
                                addArmorSet(char.id, low_q_armor_set)
                            elif q == 2:
                                addArmorSet(char.id, mid_q_armor_set)
                            elif q == 3:
                                addArmorSet(char.id, high_q_armor_set)
                            else:
                                print(f'Invalid quality [{quality}]')
                        case ['w', quality]:
                            print('Melee or gun set? [g/m]')
                            is_melee = False
                            while True:
                                input = askInput()
                                if input == 'g':
                                    is_melee = False
                                    break
                                elif input == 'm':
                                    is_melee = True
                                    break
                                else:
                                    print('Invalid selection')
                            q = safeCastToInt(quality)
                            if q == 1:
                                if is_melee:
                                    addWeaponSet(char.id, low_q_melee_set)
                                else:
                                    addWeaponSet(char.id, low_q_gun_set)
                            elif q == 2:
                                if is_melee:
                                    addWeaponSet(char.id, mid_q_melee_set)
                                else:
                                    roll = dice.roll(1, 2)
                                    if roll == 1:
                                        addWeaponSet(char.id, mid_q_gun_set1)
                                    else:
                                        addWeaponSet(char.id, mid_q_gun_set2)
                            elif q == 3:
                                if is_melee:
                                    addWeaponSet(char.id, high_q_melee_set)
                                else:
                                    addWeaponSet(char.id, high_q_gun_set)
                            else:
                                print(f'Invalid quality [{quality}]')
                        case _:
                            print('Invalid input')


def addArmorSet(character_id, armor_set):
    for armor in armor_set:
        print(f"Adding {armor['item']}")
        DAO.addArmor(character_id, armor['item'], armor['sp'], armor['body_parts'], armor['ev'], {})
    printGreenLine('Armor set added')


def addWeaponSet(character_id, weapon_set):
    for wep in weapon_set:
        print(f"Adding {wep['item']}")
        DAO.addWeapon(character_id, wep['item'], wep['weapon_type'], wep['is_chrome'], wep['dice_number'],
                      wep['dice_dmg'], wep['dmg_bonus'], wep['range'], wep['rof'], wep['clip_size'],
                      wep['effect_radius'], wep['wa'], wep['con'], wep['reliability'], wep['weight'])
        printGreenLine('Weapon set added')


def rollAtributes():
    atr_int = rollAtr()
    atr_ref = rollAtr()
    atr_tech = rollAtr()
    atr_cool = rollAtr()
    atr_attr = rollAtr()
    atr_luck = rollAtr()
    atr_ma = rollAtr()
    atr_body = rollAtr()
    atr_emp = rollAtr()

    print(f"""Rolled attributes: 
{INT}: {atr_int}
{REF}: {atr_ref}
{TECH}: {atr_tech}
{COOL}: {atr_cool}
{ATTR}: {atr_attr}
{LUCK}: {atr_luck}
{MA}: {atr_ma}
{BODY}: {atr_body}
{EMP}: {atr_emp}
""")

    return (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp)

def createCharacterFromReq(name, role, given_body_type, attributes, randomize=False):
    logs = []
    character_id = 0
    if randomize:
        character_id = createRandomCharacter(name, generate_gear=False)
    else:
        body_Type = addBodyType(given_body_type)
        special = 0
        character_id = DAO.addCharacter(
            name,
            role,
            special,
            body_Type,
            atr_int=attributes[INT],
            atr_ref=attributes[REF],
            atr_tech=attributes[TECH],
            atr_cool=attributes[COOL],
            atr_attr=attributes[ATTR],
            atr_luck=attributes[LUCK],
            atr_ma=attributes[MA],
            atr_body=attributes[BODY],
            atr_emp=attributes[EMP]
        )
    logs = log_event(logs, f'Character {name} created', log_pos)

    return (logs, character_id)

def createManualCharacter(name):
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


def rollRole():
    roll = dice.roll(1, 10)
    role = ''
    if roll == 1:
        role = roles.solo
    elif roll == 2:
        role = roles.cop
    elif roll == 3:
        role = roles.corp
    elif roll == 4:
        role = roles.fixer
    elif roll == 5:
        role = roles.nomad
    elif roll == 6:
        role = roles.techie
    elif roll == 7:
        role = roles.netrunner
    elif roll == 8:
        role = roles.meditechie
    elif roll == 9:
        role = roles.rocker
    else:
        role = roles.media

    print(f'Rolled {role}')
    return role
