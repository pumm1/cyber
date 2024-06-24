import random

import dice
import cyberdao as DAO
import roles
import bodytypes
from gameHelper import askInput, checkRollCommand, checkListCommand, safeCastToInt, roll_str, list_str, INT, REF, TECH, \
    COOL, ATTR, LUCK, MA, BODY, EMP, body_part_l_arm, body_part_body, body_part_head, body_part_r_arm, t_melee, \
    t_handgun, t_shotgun, t_rifle, t_thrown, t_smg, con_pocket, con_long_coat, con_jacket, not_hideable, yes_no, \
    body_part_l_leg, body_part_r_leg, printGreenLine, printRedLine, wep_standard_reliability, GEAR_TIER_LOW, \
    GEAR_TIER_MID, GEAR_TIER_HIGH, gear_is_allowed, GEAR_TIER_COMMON
from logger import log_event, log_pos
from skills import udpateCharacterSkill
from roles import role_skills, role_guns, role_armors
from weapon import addCharacterWeaponById
from armor import addArmorForCharacter
from chrome import addChromeByCharacterId
import genericGear


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


def generateRandomSkillsAndGear(character_id, gear_tier=None):
    character = DAO.getCharacterById(character_id)
    if character is not None:
        generateSkills(character)
        generateWeapons(character, gear_tier)
        generateArmors(character, gear_tier)
        if dice.roll(1, 3) > 1: #some more randomness to generating chrome
            generateChrome(character, gear_tier)



def generateChrome(character, gear_tier=None):
    chrome_of_role = roles.roleDict[character.role][roles.role_chrome] + genericChromeWithSkillChanges()
    possible_amount_of_chrome = len(chrome_of_role)
    chrome_to_add = dice.roll(1, possible_amount_of_chrome) - 1  # allow 0
    if gear_tier == GEAR_TIER_LOW and chrome_to_add > 0:
        chrome_to_add = 1
    elif gear_tier == GEAR_TIER_MID and chrome_to_add > 0:
        chrome_to_add = 2
    elif gear_tier == GEAR_TIER_HIGH and chrome_to_add > 0:
        chrome_to_add = 3
    chrome_to_add_indices = []
    while len(chrome_to_add_indices) < chrome_to_add:
        idx = random.randint(0, len(chrome_of_role) - 1)
        chrome = chrome_of_role[idx]
        chrome_tier = chrome[genericGear.tier_str]
        tier_matches = gear_is_allowed(chrome_tier, gear_tier)
        print(f'(CHROME) gear tier requested: {gear_tier} ... equipment ({chrome[genericGear.chrome_name_str]}) tier: {chrome_tier} .. matches: {tier_matches}')
        if not chrome_to_add_indices.__contains__(idx) and tier_matches:
            chrome_to_add_indices.append(idx)
            chrome = chrome_of_role[idx]
            addChromeByCharacterId(
                character.id,
                item=chrome[genericGear.chrome_name_str],
                descr=chrome[genericGear.chrome_descr_str],
                humanity_cost=chrome[genericGear.humanity_cost_str],
                atr_bonuses=chrome[genericGear.atr_bonuses_str],
                skill_bonuses_dict=chrome[genericGear.skill_bonuses_str]
            )


def genericChromeWithSkillChanges():
    c1 = generic_voice_stress_analyzer()
    c2 = generic_cyber_eyes()
    return [c1, c2]


def generic_voice_stress_analyzer():
    skill = DAO.skillByName('human perception')
    human_perception_skill_id = skill['id']
    skill_bonuses = [
        {
            'skillId': human_perception_skill_id,
            'bonus': 1
        }
    ]
    res = {
        genericGear.chrome_name_str: 'Voice stress analyzer',
        genericGear.chrome_descr_str: 'Lie detector. +2 To human perception',
        genericGear.humanity_cost_str: 5,
        genericGear.atr_bonuses_str: [],
        genericGear.skill_bonuses_str: skill_bonuses,
        genericGear.tier_str: GEAR_TIER_COMMON
    }
    return res

def generic_cyber_eyes():
    skill = DAO.skillByName('awareness')
    awareness_skill_id = skill['id']
    skill_bonuses = [
        {
            'skillId': awareness_skill_id,
            'bonus': 1
        }
    ]

    res = {
        genericGear.chrome_name_str: 'Cyber eyes',
        genericGear.chrome_descr_str: '+1 to awareness',
        genericGear.humanity_cost_str: 4,
        genericGear.atr_bonuses_str: [],
        genericGear.skill_bonuses_str: skill_bonuses,
        genericGear.tier_str: GEAR_TIER_COMMON
    }
    return res

def generateArmors(character, gear_tier=None):
    armors_of_role = roles.roleDict[character.role][roles.role_armors]
    possible_amount_of_armors = len(armors_of_role)
    armors_to_add = dice.roll(1, possible_amount_of_armors) - 1 #allow 0
    if gear_tier == GEAR_TIER_LOW:
        armors_to_add = dice.roll(1, 3)
    if armors_to_add > 4: #limit to 5
        armors_to_add = 4
    armors_to_add_indices = []
    while len(armors_to_add_indices) < armors_to_add:
        idx = random.randint(0, len(armors_of_role) - 1)
        armor = armors_of_role[idx]
        armor_gear_tier = armor[genericGear.tier_str]
        tier_matches = gear_is_allowed(armor_gear_tier, gear_tier)
        print(f'(ARMOR) gear tier requested: {gear_tier} ... equipment ({armor[genericGear.armor_name_str]}) tier: {armor_gear_tier} .. matches: {tier_matches}')
        if not armors_to_add_indices.__contains__(idx) and tier_matches:
            armors_to_add_indices.append(idx)
            addArmorForCharacter(
                character,
                item=armor[genericGear.armor_name_str],
                ev=armor[genericGear.ev_str],
                humanity_cost=armor[genericGear.humanity_cost_str],
                sp=armor[genericGear.sp_str],
                covered_parts=armor[genericGear.covered_parts_str],
                atr_bonuses=armor[genericGear.atr_bonuses_str],
                skill_bonuses_dict=armor[genericGear.skill_bonuses_str]
            )


def generateWeapons(character, gear_tier=None):
    weps_of_role = roles.roleDict[character.role][role_guns]
    guns_to_add = 1
    if gear_tier == GEAR_TIER_LOW:
        guns_to_add = 1
    elif gear_tier == GEAR_TIER_MID:
        guns_to_add = dice.roll(1, 2)
    elif gear_tier == GEAR_TIER_HIGH:
        guns_to_add = max(dice.roll(1, 3), 2)
    else:
        guns_to_add = dice.roll(1, 3)
    guns_to_add_indices = []
    while len(guns_to_add_indices) < guns_to_add:
        idx = random.randint(0, len(weps_of_role) - 1)
        wep = weps_of_role[idx]
        wep_gear_tier = wep[genericGear.tier_str]
        tier_matches = gear_is_allowed(wep_gear_tier, gear_tier)
        wep_is_uniq = not guns_to_add_indices.__contains__(idx)
        print(f'guns added: {len(guns_to_add_indices)} [{guns_to_add_indices}] - guns to add: {guns_to_add}')
        print(f'idx: {idx} - (unique: {wep_is_uniq}) (WEAPON) gear tier requested: {gear_tier} ... equipment ({wep[genericGear.weapon_name_str]}) tier: {wep_gear_tier} .. matches: {tier_matches}')

        if wep_is_uniq and tier_matches:
            guns_to_add_indices.append(idx)
            addCharacterWeaponById(
                character_id=character.id,
                dice=wep[genericGear.dice_str],
                die=wep[genericGear.die_str],
                divide_by=wep[genericGear.divide_by_str],
                bonus=wep[genericGear.bonus_str],
                weapon_name=wep[genericGear.weapon_name_str],
                clip_size=wep[genericGear.clip_size_str],
                rof=wep[genericGear.rof_str],
                humanity_cost=wep[genericGear.humanity_cost_str],
                weapon_t=wep[genericGear.weapon_type_str],
                wa=wep[genericGear.wa_str],
                con=wep[genericGear.con_str],
                weight=wep[genericGear.weight_str],
                reliability=wep[genericGear.reliability_str],
                effect_radius=wep[genericGear.effect_radius_str],
                custom_range=wep[genericGear.custom_range_str]
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


def createRandomCharacter(name, gear_tier=None):
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
    generateRandomSkillsAndGear(character_id, gear_tier)
    return character_id


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

def createCharacterFromReq(name, role, given_body_type, attributes, randomize=False, gear_tier=None):
    logs = []
    character_id = 0
    if randomize:
        character_id = createRandomCharacter(name, gear_tier)
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
