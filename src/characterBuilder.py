import dice
import cyberdao as DAO
import roles
import bodytypes
from gameHelper import askInput, checkRollCommand, checkListCommand, safeCastToInt, roll_str, list_str, INT, REF, TECH, \
    COOL, ATTR, LUCK, MA, BODY, EMP, body_part_l_arm, body_part_body, body_part_head, body_part_r_arm, t_melee, \
    t_handgun, t_shotgun, t_rifle, t_thrown
from cyberschema import head_column, body_column, l_arm_column, r_arm_column, l_leg_column, r_leg_column


def rollAtr():
    atr = dice.roll(2, 3) + 4
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
    print(f'<give role> or {roll_str} random role. {list_str} to see info on roles')
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
        elif roles.allRoles.__contains__(ans):
            role = ans
            print(f'Selected {role}')
            break
        elif allow_roll and checkRollCommand(ans):
            role = rollRole()

            break
    return role


def rollSpecial(role):
    specialAbility = roles.roleDict[role][roles.ability]

    skill = dice.roll(1, 10)
    print(f'Rolled {specialAbility} = {skill}')
    return skill


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


def addBodyType():
    print(f'<give body type> or {roll_str} random body type ({list_str} to show all)')
    body_type = 0
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

    print(f'Body type modifier = {body_type} ({bodytypes.bodyTypeModifiersByValue(body_type)})')
    return body_type


def handleRole(is_random: bool):
    role = ''
    if is_random:
        role = rollRole()
    else:
        role = addRole()
    return role


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


def createRandomCharacter(name):
    role = rollRole()
    special = rollSpecial(role)
    body_type = rollBodyType()
    (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp) = rollAtributes()
    DAO.addCharacter(
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
    generateGear(name)


low_q_armor_set = [
    {'item': 'vest', 'body_parts': [body_column], 'sp': 10},
    {'item': 'helmet', 'body_parts': [head_column], 'sp': 10}
]

mid_q_armor_set = [
    {'item': 'flak jacket', 'body_parts': [body_column, l_arm_column, r_arm_column], 'sp': 15},
    {'item': 'helmet', 'body_parts': [head_column], 'sp': 10}
]

high_q_armor_set = [
    {'item': 'combat armor', 'body_parts': [body_column, l_arm_column, r_arm_column, l_leg_column, r_leg_column], 'sp': 20},
    {'item': 'combat helmet', 'body_parts': [head_column], 'sp': 20}
]

low_q_melee_set = [
    {'item': 'Rippers', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 3,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'effect_radius': 0}
]

mid_q_melee_set = [
    {'item': 'Slice n dice', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 2, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'effect_radius': 0},
    {'item': 'Cybersnake',
     'weapon_type': t_melee, 'is_chrome': True,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'effect_radius': 0}
]

high_q_melee_set = [
    {'item': 'Wolvers', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 3, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'effect_radius': 0},
    {'item': 'Cybersnake 1', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'effect_radius': 0},
    {'item': 'Cybersnake 2', 'is_chrome': True,
     'weapon_type': t_melee,
     'dice_number': 1, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 1, 'rof': 1, 'clip_size': 0, 'shots_left': 0,
     'effect_radius': 0}
]

low_q_gun_set = [
    {'item': 'Colt .45', 'is_chrome': False,
     'weapon_type': t_handgun,
     'dice_number': 2, 'dice_dmg': 6, 'dmg_bonus': 3,
     'range': 50, 'rof': 2, 'clip_size': 6, 'shots_left': 6,
     'effect_radius': 0}
]

mid_q_gun_set = [
    {'item': 'Double barrel shotgun', 'is_chrome': False,
     'weapon_type': t_shotgun,
     'dice_number': 4, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 50, 'rof': 1, 'clip_size': 2, 'shots_left': 2,
     'effect_radius': 0},
    {'item': 'Molotov cocktail', 'is_chrome': False,
     'weapon_type': t_thrown,
     'dice_number': 2, 'dice_dmg': 10, 'dmg_bonus': 0,
     'range': 30, 'rof': 1, 'clip_size': 1, 'shots_left': 1,
     'effect_radius': 0},
]

high_q_gun_set = [
    {'item': 'Militech Ronin Lt. AR', 'is_chrome': False,
     'weapon_type': t_rifle,
     'dice_number': 5, 'dice_dmg': 6, 'dmg_bonus': 0,
     'range': 400, 'rof': 35, 'clip_size': 30, 'shots_left': 30,
     'effect_radius': 0},
    {'item': 'Frag. Grenade', 'is_chrome': False,
     'weapon_type': t_thrown,
     'dice_number': 3, 'dice_dmg': 10, 'dmg_bonus': 0,
     'range': 30, 'rof': 1, 'clip_size': 1, 'shots_left': 1,
     'effect_radius': 5},
]



def generateGear(name):
    print('Generate gear? [Y/N]')
    gen_gear = False
    while True:
        i = askInput()
        if i.lower() == 'y':
            gen_gear = True
            break
        elif i.lower() == 'n':
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
                if i.lower() == '-1':
                    add_gear = False
                else:
                    gear = i.lower().split('-')
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
                                if input.lower() == 'g':
                                    is_melee = False
                                    break
                                elif input.lower() == 'm':
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
                                    addWeaponSet(char.id, mid_q_gun_set)
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
        DAO.addArmor(character_id, armor['item'], armor['sp'], armor['body_parts'])
    print('Armor set added')


def addWeaponSet(character_id, weapon_set):
    for weapon in weapon_set:
        print(f"Adding {weapon['item']}")
        DAO.addWeapon(character_id, weapon['item'], weapon['weapon_type'], weapon['is_chrome'], weapon['dice_number'], weapon['dice_dmg'], weapon['dmg_bonus'], weapon['range'], weapon['rof'], weapon['clip_size'], weapon['effect_radius'])
print('Weapon set added')


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
