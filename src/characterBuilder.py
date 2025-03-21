import random

import src.dice as dice
import src.cyberdao as DAO
import src.roles as roles
import src.bodytypes as bodytypes
from src.gameHelper import askInput, checkRollCommand, checkListCommand, safeCastToInt, roll_str, list_str, INT, REF, TECH, \
    COOL, ATTR, LUCK, MA, BODY, EMP, body_part_l_arm, body_part_body, body_part_head, body_part_r_arm, t_melee, \
    t_handgun, t_shotgun, t_rifle, t_thrown, t_smg, con_pocket, con_long_coat, con_jacket, not_hideable, yes_no, \
    body_part_l_leg, body_part_r_leg, printGreenLine, printRedLine, wep_standard_reliability, GEAR_TIER_LOW, \
    GEAR_TIER_MID, GEAR_TIER_HIGH, gear_is_allowed, GEAR_TIER_COMMON
from src.logger import log_event, log_pos
from src.cyberService import udpateCharacterSkill, addChromeByCharacterId, addCharacterWeaponById, addArmorForCharacter
from src.roles import role_skills, role_guns, role_armors
import src.genericGear as genericGear


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
    chrome_by_tier = list(filter(lambda c: gear_is_allowed(c[genericGear.tier_str], gear_tier), chrome_of_role))
    possible_amount_of_chrome = len(chrome_by_tier)
    chrome_to_add = dice.roll(1, possible_amount_of_chrome) - 1  # allow 0
    if gear_tier == GEAR_TIER_LOW and chrome_to_add > 0:
        chrome_to_add = 1
    elif gear_tier == GEAR_TIER_MID and chrome_to_add > 0:
        chrome_to_add = 2
    elif gear_tier == GEAR_TIER_HIGH and chrome_to_add > 0:
        chrome_to_add = 3
    chrome_to_add_indices = []
    while len(chrome_to_add_indices) < chrome_to_add:
        idx = random.randint(0, len(chrome_by_tier) - 1)
        chrome = chrome_by_tier[idx]
        chrome_tier = chrome[genericGear.tier_str]
        tier_matches = gear_is_allowed(chrome_tier, gear_tier)
        print(f'(CHROME) gear tier requested: {gear_tier} ... equipment ({chrome[genericGear.chrome_name_str]}) tier: {chrome_tier} .. matches: {tier_matches}')
        if not chrome_to_add_indices.__contains__(idx) and tier_matches:
            chrome_to_add_indices.append(idx)
            chrome = chrome_by_tier[idx]
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
    max_armors_to_add = 3 #the number of armors is a bit of a hack because of the way generic gear is handled
    incude_helmet = True

    if gear_tier == GEAR_TIER_LOW:
        incude_helmet = False

    armors_to_add = dice.roll(1, max_armors_to_add)
    if gear_tier == GEAR_TIER_LOW:
        armors_to_add = armors_to_add - 1 # allow 0 for low tier
    elif gear_tier == GEAR_TIER_HIGH:
        armors_to_add = max_armors_to_add

    weighted_armor_tries = 5
    weighted_armor_try = 0

    use_armor_set = dice.roll(1, 2) > 1

    armors_to_use = []
    if use_armor_set:
        armors_to_use = genericGear.generic_sets
    else:
        armors_to_use = genericGear.generic_body_armors

    if incude_helmet:
        armors_to_use = armors_to_use + genericGear.generic_helmets

    armors_by_tier = list(filter(lambda a: gear_is_allowed(a[genericGear.tier_str], gear_tier), armors_to_use))
    print(f'Use set: {use_armor_set} - possibly include helmet: {incude_helmet}')
    print(f'Tier {gear_tier} armors: {len(armors_by_tier)}')

    armors_to_add_indices = []
    max_tries = 15
    add_try = 0
    while len(armors_to_add_indices) < armors_to_add and add_try < max_tries:
        add_try += 1
        print(f'Attempting to add armor (try {add_try} / {max_tries})')
        idx = random.randint(0, len(armors_by_tier) - 1)
        armor = armors_by_tier[idx]
        armor_gear_tier = armor[genericGear.tier_str]
        weighted_gear_match = False
        if weighted_armor_try < weighted_armor_tries and gear_tier is not None:
            weighted_gear_match = armor_gear_tier == gear_tier

            if not weighted_gear_match:
                print(f'Weighted armor try {weighted_armor_try}/{weighted_armor_tries}')
                weighted_armor_try += 1
            else:
                weighted_armor_try = weighted_armor_tries
        else:
            weighted_gear_match = True

        tier_matches = gear_is_allowed(armor_gear_tier, gear_tier)
        print(f'(ARMOR) gear tier requested: {gear_tier} ... equipment ({armor[genericGear.armor_name_str]}) tier: {armor_gear_tier} .. matches: {tier_matches}')
        if not armors_to_add_indices.__contains__(idx) and tier_matches and weighted_gear_match:
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
    weps_of_role = list(roles.roleDict[character.role][role_guns])
    weps_by_tier = list(filter(lambda w: gear_is_allowed(w[genericGear.tier_str], gear_tier), weps_of_role))
    max_guns_to_add = len(weps_by_tier)
    #trying to make the weapons more likely a bit more realistic
    weighted_weapon_type = t_handgun
    weighted_roll = dice.roll(1, 6)
    guns_to_add = 1

    if gear_tier == GEAR_TIER_LOW:
        if weighted_roll <= 2:
            weighted_weapon_type = t_melee
    elif gear_tier == GEAR_TIER_MID:
        guns_to_add = dice.roll(1, 2)
        if weighted_roll <= 3:
            weighted_weapon_type = t_smg
        else:
            weighted_weapon_type = t_shotgun
    elif gear_tier == GEAR_TIER_HIGH:
        guns_to_add = 2
        if weighted_roll <= 1:
            weighted_weapon_type = t_shotgun
        elif weighted_roll < 3:
            weighted_weapon_type = t_smg
        else:
            weighted_weapon_type = t_rifle

    print(f'Guns to add = MIN({max_guns_to_add}, {guns_to_add})')

    unique_weapon_types = []

    guns_to_add_indices = []
    weighted_weapon_tries = 5
    weighted_weapon_try = 0
    max_tries = 15
    add_try = 0
    while len(guns_to_add_indices) < guns_to_add and add_try < max_tries:
        add_try += 1
        num_of_weps = len(weps_by_tier)
        print(f'Num of weapons to choose from: {num_of_weps} (try {add_try} / {max_tries})')
        idx = random.randint(0, num_of_weps - 1)
        wep = weps_by_tier[idx]
        wep_gear_tier = wep[genericGear.tier_str]
        wep_type = wep[genericGear.weapon_type_str]
        is_unique_wep_type = not unique_weapon_types.__contains__(wep_type)

        tier_matches = gear_is_allowed(wep_gear_tier, gear_tier)
        wep_is_uniq = not guns_to_add_indices.__contains__(idx)
        weighted_type_match = False
        if weighted_weapon_try < weighted_weapon_tries:
            weighted_type_match = weighted_weapon_type == wep[genericGear.weapon_type_str]
            weighted_weapon_try += 1
        else:
            weighted_type_match = True

        if not weighted_type_match:
            print(f'Weighted weapon try {weighted_weapon_try}/{weighted_weapon_tries}')
        else:
            weighted_weapon_try = weighted_weapon_tries
        print(f'Maybe adding {wep[genericGear.weapon_name_str]} ({wep_type})')
        print(f'guns to add: {guns_to_add} - guns added: {len(guns_to_add_indices)} [{guns_to_add_indices}]')
        print(f'idx: {idx} - (unique: {wep_is_uniq}, unique type: {is_unique_wep_type}) (WEAPON) gear tier requested: {gear_tier} ... equipment ({wep[genericGear.weapon_name_str]}) tier: {wep_gear_tier} .. matches: {tier_matches}')

        if wep_is_uniq and tier_matches and weighted_type_match and is_unique_wep_type:
            guns_to_add_indices.append(idx)
            if is_unique_wep_type:
                unique_weapon_types.append(wep_type)
                weps_by_tier = list(filter(lambda w: not unique_weapon_types.__contains__(w[genericGear.weapon_type_str]),weps_by_tier))
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
    (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp) = rollAtributes()
    DAO.addCharacter(
        name,
        role,
        special,
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
    (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp) = rollAtributes()
    character_id = DAO.addCharacter(
        name,
        role,
        special,
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
        special = 0
        character_id = DAO.addCharacter(
            name,
            role,
            special,
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
