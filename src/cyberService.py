import math

import src.cyberdao as DAO
from src.bonus import SkillBonus, handleBonuses
from src.campaign import valid_gig_statuses, CampaignGig, CampaignEvent, Campaign
from src.character import Character
from src.combat import fullAutoRoll, weaponByAttackType, characterSkillBonusForWeapon, weapon_info, modifiersForTarget, \
    hitDmg, dmg_info, rollToBeatStr, burstRoll, stunCheck, handleMeleeDmg, handleMelee, \
    weaponByAttackTypeAndWeaponId, resolveDmgPassingSP, resolveDmgDoneToCharacter, resolveApDmg
from src.dice import roll, rollWithCrit, rollWithCritAndGivenLuck, handleLuck, resolveAutoOrManualRollWithCrit
from src.gameHelper import askInput, printGreenLine, askForRoll, roll_str, safeCastToInt, EMP, BODY, body_parts, \
    uniqueArr, body_parts_armor_info, yes_no, body_part_head, body_part_body, body_part_l_arm, body_part_r_arm, \
    body_part_r_leg, body_part_l_leg, list_skills_helper_str, REF, printRedLine, checkListCommand, TECH, list_str, \
    attack_type_full_auto, attack_type_melee, attack_type_burst, attack_type_single, t_thrown, close_range_str, \
    medium_range_str, max_health
from src.logger import Log, log_event, log_neutral, log_neg, log_pos
from src.roles import roleSpecialAbility, meditechie
from src.skill import SkillInfo
from src.skills import printCharSkillInfo, printSkillInfo, skillBonusForSkill, skill_athletics, \
    character_special_atr_bonus_on_skill, easy_check, average_check, difficult_check, difficultyCheckInfo, \
    very_difficult_check, nearly_impossible_check, skill_first_aid
from src.status import status_pos, status_neutral, valid_statuses
from src.weapon import askReliability, askCon, askWeight, askWa, askRof, askForChrome, rangeByType, askWeaponType


# Chrome
def addChromeWithHumanityCost(
        character, item, descr, humanity_cost = None, item_bonus_id: int | None = None, atr_bonuses=None, skill_bonuses=None
) -> list[Log]:
    if atr_bonuses is None or skill_bonuses is None:
        (atr_bonuses, skill_bonuses) = handleBonuses()
    (humanity_cost, logs) = handleHumanity(character, humanity_cost)
    DAO.addChrome(character.id, item, humanity_cost, descr, item_bonus_id, atr_bonuses, skill_bonuses)

    return logs


def addChromeByCharacterId(id, item, descr, humanity_cost, atr_bonuses, skill_bonuses_dict):
    logs = []
    atr_dict = dict([])
    for atr_bonus in atr_bonuses:
        atr = atr_bonus['attribute']
        bonus = atr_bonus['bonus']
        t_a_bonus = atr_dict.get(atr)
        if t_a_bonus is None:
            atr_dict[atr] = bonus
        else:
            bonus = t_a_bonus + bonus
            atr_dict[atr] = bonus
    character = DAO.getCharacterById(id)
    skill_bonuses = []
    for s in skill_bonuses_dict:
        skill_bonus = SkillBonus(s['skillId'], s['bonus'], item_bonus_id=0)
        skill_bonuses.append(skill_bonus)

    if character is not None:
        chrome_logs = addChromeWithHumanityCost(character, item, descr, humanity_cost=humanity_cost, atr_bonuses=atr_dict, skill_bonuses=skill_bonuses)

    return logs + chrome_logs



def addChrome(character, name=None, descr=None) -> list[Log]:
    logs = []
    if character is not None:
        print('Give name of cybernetic:')
        item = askInput()
        print('Give description:')
        descr = askInput()

        addChromeWithHumanityCost(character, item, descr)
        printGreenLine(f'Chrome added for {character.name}')


def addChromeByName(name):
    character = DAO.getCharacterByName(name)
    addChrome(character)


def addChromeByCharacterId(id, item, descr, humanity_cost, atr_bonuses, skill_bonuses_dict):
    logs = []
    atr_dict = dict([])
    for atr_bonus in atr_bonuses:
        atr = atr_bonus['attribute']
        bonus = atr_bonus['bonus']
        t_a_bonus = atr_dict.get(atr)
        if t_a_bonus is None:
            atr_dict[atr] = bonus
        else:
            bonus = t_a_bonus + bonus
            atr_dict[atr] = bonus
    character = DAO.getCharacterById(id)
    skill_bonuses = []
    for s in skill_bonuses_dict:
        skill_bonus = SkillBonus(s['skillId'], s['bonus'], item_bonus_id=0)
        skill_bonuses.append(skill_bonus)

    if character is not None:
        chrome_logs = addChromeWithHumanityCost(character, item, descr, humanity_cost=humanity_cost, atr_bonuses=atr_dict, skill_bonuses=skill_bonuses)

    return logs + chrome_logs


def handleHumanity(char, humanity_cost=None) -> (int, list[Log]):
    if humanity_cost is None:
        print(f'Reduce humanity for chrome ({roll_str} or <amount>)')
        humanity_cost = 0
        while True:
            i = askInput()
            if i == roll_str:
                (dice, die, divide_by, bonus) = askForRoll()
                humanity_cost = roll(dice, die, divide_by) + bonus
                print(f'Rolled {humanity_cost}')
                break
            else:
                cost = safeCastToInt(i)
                if cost > 0:
                    humanity_cost = cost
                    break

    curr_hum = char.humanity
    t_hum = curr_hum - humanity_cost
    emp = math.ceil(t_hum / 10)
    logs = log_event([], f'Curr emp: {char.attributes[EMP]} - new emp: {emp}', log_neutral)
    logs = log_event(logs, f'Current humanity: {curr_hum} - new humanity: {t_hum}', log_neg)
    DAO.changeHumanityAndEmp(char.id, t_hum, emp)
    logs = log_event(logs, f'Updated humanity and empathy', log_neutral)
    return (humanity_cost, logs)



def removeChromeByCharacterId(chararacter_id, chrome_id) -> list[Log]:
    character = DAO.getCharacterById(chararacter_id)
    logs = []
    if character is not None:
        DAO.deleteCharacterChrome(chararacter_id, chrome_id)
        logs = log_event(logs, f'Chrome deleted from {character.name}', log_neutral)
    else:
        logs = log_event(logs, f'Character not found for chrome deletion', log_neg)
    return logs


# Armor

def checkBodyPartNum(i):
    num = safeCastToInt(i)
    body_part = None
    if num == 1:
        body_part = body_part_head
    elif num == 2:
        body_part = body_part_body
    elif num == 3:
        body_part = body_part_l_arm
    elif num == 4:
        body_part = body_part_r_arm
    elif num == 5:
        body_part = body_part_r_leg
    elif num == 6:
        body_part = body_part_l_leg
    return body_part


def addArmorForCharacter(character, item=None, ev=None, humanity_cost=None, sp=None, covered_parts=None, atr_bonuses=None, skill_bonuses_dict=None) -> list[Log]:
    logs = []
    """
        small HAX: 
        armor could use all bonuses, but it's not fetched now for armor (would be easy fix..),
        but skill improvements feel more like chrome thing
    """
    if character is not None:
        if item is None:
            print(f'Give armor name:')
            item = askInput()

        is_chrome = False
        if humanity_cost is not None:
            if len(skill_bonuses_dict) > 0:
                is_chrome = True
            elif humanity_cost is not None:
                if humanity_cost > 0:
                    is_chrome = True
        else:
            print(f'Is chrome? {yes_no}')
            while True:
                t_chrome = askInput()
                if t_chrome == 'y':
                    is_chrome = True
                    break
                elif t_chrome == 'n':
                    break
        if sp is None:
            print(f'Give SP:')
            sp = 0
            while True:
                sp_i = askInput()
                sp = safeCastToInt(sp_i)
                if sp > 0:
                    break
        if atr_bonuses is None or skill_bonuses_dict is None:
            (atr_bonuses, skill_bonuses) = handleBonuses()
        if ev is None:
            print('Give encumbrance (EV):')
            ev = -1
            while ev < 0:
                i = askInput()
                ev = safeCastToInt(i)

        if covered_parts is None:
            print(f'Give covered body parts: (end with -1 if there is at least one body part)')
            print(body_parts_armor_info)
            covered_parts = []
            while len(covered_parts) < 6:
                input = askInput()
                if (body_parts.__contains__(input)):
                    covered_parts = uniqueArr(covered_parts.append(input))
                elif input == '-1' and len(covered_parts) > 0:
                    break
                else:
                    input = checkBodyPartNum(input)
                    if input is not None:
                        covered_parts.append(input)
                        covered_parts = uniqueArr(covered_parts)

        skill_bonuses = []
        for s in skill_bonuses_dict:
            skill_bonus = SkillBonus(s['skillId'], s['bonus'], item_bonus_id=0)
            skill_bonuses.append(skill_bonus)

        item_bonus_id = DAO.addArmor(character.id, item, sp, covered_parts, ev, atr_bonuses, skill_bonuses)
        chrome_logs = []
        if is_chrome:
            chrome_logs = addChromeWithHumanityCost(
                character, item, 'Added with armor', item_bonus_id=item_bonus_id, humanity_cost=humanity_cost,
                atr_bonuses={}, skill_bonuses=skill_bonuses
            )
        logs = logs + chrome_logs
        logs = log_event(logs, f'Armor added!', log_pos)
    else:
        logs = log_event(logs, 'Character not found for armor adding', log_neg)
    return logs


def addArmorForCharacterById(id, item, ev, sp, body_parts, humanity_cost, atr_bonuses_arr, skill_bonuses_dict):
    character = DAO.getCharacterById(id)
    atr_bonuses = {}
    for a in atr_bonuses_arr:
        atr = a.pop('attribute')
        atr_bonuses[atr] = a['bonus']
    return addArmorForCharacter(character, item, ev, humanity_cost, sp, body_parts, atr_bonuses, skill_bonuses_dict)

def addArmorForCharacterByName(name):
    character = DAO.getCharacterByName(name)
    return addArmorForCharacter(character)


def repairCharSP(char) -> bool:
    logs = []
    if char is not None:
        DAO.repairCharacterSP(char.id)
        logs = log_event(logs, f'Armor repaired for {char.name}', log_pos)
        return logs
    else:
        logs = log_event(logs, f'Character not found for armor repair', log_neg)
    return logs

def repairSPById(char_id) -> bool:
    char = DAO.getCharacterById(char_id)
    return repairCharSP(char)


def repairSPByName(name) -> bool:
    char = DAO.getCharacterByName(name)
    return repairCharSP(char)


def removeArmor(character, armor_id) -> list[Log]:
    logs = []
    if character is not None:
        DAO.deleteCharacterArmor(character.id, armor_id)
        logs = log_event(logs, f'Character armor removed', log_neutral)
    else:
        logs = log_event(logs, f'Character not found for armor removal', log_neg)
    return logs


def removeArmorByCharacterId(id, armor_id) -> list[Log]:
    char = DAO.getCharacterById(id)
    return removeArmor(char, armor_id)


def removeArmorByName(name, armor_id):
    char = DAO.getCharacterByName(name)
    removeArmor(char, armor_id)


# Weapons
def addCharWeapon(
        char: Character, dice=None, die=None, divide_by=None, bonus=0, weapon_name=None, clip_size=None, rof=None,
        humanity_cost=None, weapon_t=None, wa=None, con=None, weight=None, reliability=None, effect_radius=None,
        custom_range=None
) -> list[Log]:
    logs = []
    if char is not None:
        if weapon_name is None:
            print(f'Give weapon name:')
            weapon_name = askInput()
        if clip_size is None or weapon_t is None:
            (weapon_t, clip_size) = askWeaponType()
        weapon_range = rangeByType(char.attributes[BODY], weapon_t, custom_range=custom_range)
        is_chrome = False
        if humanity_cost is None:
            is_chrome = askForChrome()
        elif humanity_cost > 0:
            is_chrome = True
        if effect_radius is None:
            print('Give effect radius (e.g. explosives)')
            r = askInput()
            effect_radius = safeCastToInt(r)
        if rof is None:
            rof = 1
            rof = askRof()

        if wa is None:
            wa = askWa()
        if con is None:
            con = askCon()
        if reliability is None:
            reliability = askReliability()
        if weight is None:
            weight = askWeight()

        if dice is None or die is None or divide_by is None or bonus is None:
            (dice, die, divide_by, bonus) = askForRoll()

        DAO.addWeapon(char.id, weapon_name, weapon_t, is_chrome, dice, die, divide_by, bonus, weapon_range, rof, clip_size,
                      effect_radius, wa, con, reliability, weight)

        if is_chrome:
            (_, humanity_logs) = handleHumanity(char, humanity_cost=humanity_cost)
            logs = logs + humanity_logs

        logs = log_event(logs, f'Weapon ({weapon_name}) added!', log_pos)
    else:
        logs = log_event(logs, 'Character not found for weapon add', log_neg)

    return logs


def addCharacterWeaponById(
        character_id, dice=None, die=None, divide_by=None, bonus=0, weapon_name=None, clip_size=None,
        rof=None, humanity_cost=None, weapon_t=None, wa=None, con=None, weight=None, reliability=None,
        effect_radius=None, custom_range=None
) -> list[Log]:
    char = DAO.getCharacterById(character_id)
    logs = addCharWeapon(
        char,
        dice=dice,
        die=die,
        divide_by=divide_by,
        bonus=bonus,
        weapon_name=weapon_name,
        clip_size=clip_size,
        rof=rof,
        humanity_cost=humanity_cost,
        weapon_t=weapon_t,
        wa=wa,
        con=con,
        weight=weight,
        reliability=reliability,
        effect_radius=effect_radius,
        custom_range=custom_range
    )
    return logs

def addChracterWeaponByName(character_name):
    char = DAO.getCharacterByName(character_name)
    addCharWeapon(char)


def removeWeapon(character, weapon_id) -> list[Log]:
    logs = []
    if character is not None:
        deleted = DAO.deleteCharacterWeapon(character.id, weapon_id)
        if deleted:
            logs = log_event(logs, f'Character weapon removed', log_neutral)
    else:
        logs = log_event(logs, f'Character not found for weapon removal', log_neg)
    return logs


def removeWeaponByCharacterId(character_id, weapon_id) -> list[Log]:
    character = DAO.getCharacterById(character_id)
    return removeWeapon(character, weapon_id)

# Statuses

def addStatus(character_id: int, status: str, effect: str, status_type: str):
    char = DAO.getCharacterById(character_id)
    if char is not None:
        DAO.addCharacterStatus(character_id, status, effect, status_type)
        l_type = log_neg
        if status_type == status_pos:
            l_type = log_pos
        elif status_type == status_neutral:
            l_type = log_neutral
        logs = log_event(list(), f'Status {status} added for {char.name}', l_type)
        return logs

def addStatusManual(name):
    char = DAO.getCharacterByName(name)
    if char is not None:
        print(f'Give status: (e.g. drugged, stunned, psychosis, but can be anything else too)')
        status = askInput()
        print("Give brief description on status effect (e.g. can't move, -2 to some attribute etc.)")
        effect = askInput()
        print(f"Give statusType ({valid_statuses})")
        statusType = ''
        while True:
            statusType = askInput()
            if valid_statuses.__contains__(statusType):
                break
            else:
                print(f"Not valid status ({valid_statuses})")
        DAO.addCharacterStatus(char.id, status, effect, statusType)
        print('Status added')

def removeStatusByCharId(charcter_id, status_id):
    char = DAO.getCharacterById(charcter_id)
    logs = []
    if char is not None:
        status_row = DAO.getCharacterStatusById(status_id, charcter_id)
        if status_row is not None:
            status = status_row['status']
            DAO.removeStatus(status_id, char.id)
            logs = log_event(logs, f'Status {status} removed from {char.name}', log_neutral)
        else:
            logs = log_event(logs, f'Status not found', log_neg)

    return logs

def removeStatusByCharName(name, status_id):
    char = DAO.getCharacterByName(name)
    if char is not None:
        DAO.removeStatus(status_id, char.id)
        print('Status removed')

# Skills

def rollCharacterMeleeDef(name, roll_res):
    character = DAO.getCharacterByName(name)
    if character is not None:
        skill = DAO.getSkillByName('dodge/escape')
        if skill is not None:
            die_roll = safeCastToInt(roll_res)
            if die_roll <= 0:
                (die_roll, _) = rollWithCrit(True)

            atr_bonus = character.attributes[skill['attribute']]

            char_dodge_skill = None
            for s in character.skills:
                if s.id == skill['id']:
                    char_dodge_skill = s
                    break
            char_dodge_lvl = 0
            if char_dodge_skill is not None:
                char_dodge_lvl = char_dodge_skill.lvl
            roll_res = die_roll + atr_bonus + char_dodge_lvl
            print(f"""(die roll = {die_roll}, atr_bonus = {atr_bonus}, dodge = {char_dodge_lvl})""")
            printGreenLine(f"Melee def total: {roll_res} (hopefully the attacker rolled lower..)")


def rollCharacterSkillById(id, skill_num, roll, modifier, added_luck) -> list[Log]:
    character = DAO.getCharacterById(id)
    return rollCharacterSkill(character, skill_num, roll, modifier, added_luck)


def rollCharacterSkillByName(name, skill_num, roll, modifier):
    character = DAO.getCharacterByName(name)
    return rollCharacterSkill(character, skill_num, roll, modifier, added_luck=None)

def allSkills():
    skills = DAO.listSkills()
    return skills


def updateCharSkillById(char_id, skill_id, lvl_up_amount):
    character = DAO.getCharacterById(char_id)
    return udpateCharacterSkill(character, skill_id, lvl_up_amount)


def updateCharSkill(name, skill_id, lvl_up_amount):
    character = DAO.getCharacterByName(name)
    return udpateCharacterSkill(character, skill_id, lvl_up_amount)


def printCharacterSkills(name):
    skills = characterSkills(name)
    printCharSkillInfo(skills)


def characterSkills(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        skills = DAO.getCharacterSkillsById(character.id)
        return skills
    else:
        print(f'{name} Not found')
        return list()


def skillsByAttribute(atr):
    skills = DAO.listSkillsByAttribute(atr)
    return skills


def listSkillsByAttribute(atr: str):
    atr_skills = skillsByAttribute(atr)
    printSkillInfo(atr_skills)


def findSkillsByString(string: str):
    skills = DAO.skillsByFuzzyLogic(string)
    printSkillInfo(skills)


def awarenessSkill():
    return DAO.skillByName('awareness')


def fetchAllSkils():
    skills = allSkills().values()
    return list(skills)

def listAllSkills():
    all_skills = allSkills()
    printSkillInfo(all_skills)

def udpateCharacterSkill(character, skill_id, lvl_up_amount) -> list[Log]:
    event_logs = []
    t_skill = safeCastToInt(skill_id)
    if t_skill >= 0:
        if character is not None:
            if t_skill == 0:
                DAO.updateCharSpecial(character.id, character.role, lvl_up_amount)
                special_log = Log(f'{character.name} special updated (+{lvl_up_amount})', log_pos)
                event_logs.append(special_log.toJson())
            else:
                skill = DAO.getSkillById(skill_id)
                char_skills: list[SkillInfo] = character.skills
                curr_skill_lvl = 0
                for s in char_skills:
                    if s.id == skill_id:
                        curr_skill_lvl = s.lvl
                can_update = curr_skill_lvl + lvl_up_amount <= 10
                if skill is not None:
                    if can_update:
                        DAO.updateCharSkill(character.id, skill, lvl_up_amount)
                        skill_updated_log = Log(f"Skill {skill['skill']} (+{lvl_up_amount}) updated for {character.name}", log_pos)
                        event_logs.append(skill_updated_log.toJson())
                    else:
                        event_logs.append(Log("Skill can't get above 10", log_neg).toJson())
                else:
                    not_found_log = Log(f'Skill not found by id ({skill_id})', log_neg)
                    event_logs.append(not_found_log.toJson())
    else:
        not_valid_skill_log = Log(f"'{skill_id}' not a valid skill id", log_neg)
        event_logs.append(not_valid_skill_log.toJson())

    return event_logs



def listSkills(command):
    match command:
        case[_]:
            listAllSkills()
        case[_, 'atr', atr]:
            listSkillsByAttribute(atr)
        case[_, 'fuzzy', str]:
            findSkillsByString(str)
        case[_, 'char', name]:
            printCharacterSkills(name)
        case _:
            print(list_skills_helper_str)


#TODO: handle special skill
def rollCharacterSkill(character, skill_num, roll=0, modifier=0, added_luck=None) -> list[Log]:
    logs = []
    skill_name = ''
    roll_modifier = safeCastToInt(modifier)
    skill_id = safeCastToInt(skill_num)
    skill = None
    if character is not None:
        t_roll = safeCastToInt(roll)
        atr_bonus = 0
        char_skill_lvl = 0
        die_roll = 0
        (special_atr_bonus, special_atr) = character_special_atr_bonus_on_skill(character)
        if skill_id == 0:
            skill = {
                'id': 0,
                'skill': roleSpecialAbility(character.role),
                'attribute': special_atr,  # TODO: define for all special skills
                'description': 'TODO'
            }
        else:
            skill = DAO.getSkillById(skill_id)

        if skill is not None:
            skill_name = skill['skill']

            if t_roll <= 0:
                if added_luck == None:
                    added_luck = handleLuck()
                (die_roll, dice_logs) = rollWithCritAndGivenLuck(added_luck)
                logs = logs + dice_logs
            else:
                die_roll = t_roll
            skill_with_lvl = None
            if skill_id == 0:
                atr_bonus = special_atr_bonus
                skill_with_lvl = SkillInfo(skill_id, skill['skill'], character.specialAbility, skill['attribute'], is_original=True)
            else:
                skill_with_lvl_arr = [s for s in character.skills if s.skill == skill_name]
                skill_atr = skill['attribute']
                atr_bonus = character.attributes[skill_atr]
                if len(skill_with_lvl_arr) > 0:
                    skill_with_lvl = skill_with_lvl_arr[0]
                    char_skill_lvl = skill_with_lvl.lvl
            roll_ress = die_roll + char_skill_lvl + atr_bonus + roll_modifier

            logs = log_event(logs, f"""{character.name} rolled {roll_ress} for {skill_name}""", log_neutral)
            logs = log_event(
                logs,
                f"(die roll = {die_roll}, atr_bonus = {atr_bonus}, skill_level = {char_skill_lvl}, modifier = {roll_modifier})",
                log_neutral
            )

        else:
            logs = log_event(logs, f'SKILL NOT FOUND [skill_id = {skill_id}]', log_neg)

    return logs


# Combat

def stunCheckById(character_id) -> list[Log]:
    logs = []
    c = DAO.getCharacterById(character_id)
    if c is not None:
        logs = stunCheck(c)
    else:
        logs = log_event(logs, f'Character not found [id = {character_id}]', log_neg)
    return logs


def stunCheckByName(name) -> list[Log]:
    logs = []
    c = DAO.getCharacterByName(name)
    if c is not None:
        logs = stunCheck(c)
    else:
        logs = log_event(logs, f'Character not found [name = {name}]', log_neg)
    return logs


def hitCharacter(character, body_part, dmg_str, is_ap, pass_sp):
    dmg = safeCastToInt(dmg_str)
    logs = []
    if character is not None:
        if pass_sp == True:
            logs = damageCharacter(character, dmg=dmg, body_part=body_part)
        elif body_parts.__contains__(body_part):
            if is_ap:
                logs = handleApHit(character, dmg, body_part, logs)
            else:
                logs = handleNormalHit(character, dmg, body_part)
        else:
            valid_body_parts = ', '.join(body_parts)
            logs = log_event(logs, f'Invalid body part {body_part} [{valid_body_parts}]', log_neg)
    else:
        logs = log_event(logs, 'Character not found', log_neg)
    return logs


def handleNormalHit(character: Character, dmg, body_part) -> list[Log]:
    logs = []
    char_sp = character.sp[body_part]
    if char_sp > 0:
        (passed_dmg, armor_damaged) = resolveDmgPassingSP(char_sp, dmg)
        if armor_damaged:
            logs = log_event(logs, f'Armor damaged at {body_part} and {passed_dmg} DMG done to {character.name}',
                             log_neg)
            DAO.dmgCharacterSP(character.id, body_part)
            logs = damageCharacter(character, passed_dmg, body_part, logs)
        else:
            logs = log_event(logs, f"{character.name}'s armor absorbed the hit", log_neutral)
    else:
        logs = log_event(logs, f'{character.name} has no armor left at {body_part}', log_neutral)
        dmg_logs = damageCharacter(character, dmg, body_part)
        logs = logs + dmg_logs
    return logs


def handleApHit(character: Character, dmg, body_part, logs) -> list[Log]:
    char_sp = character.sp[body_part]
    dmg_done = resolveApDmg(char_sp, dmg)
    log_type = log_pos
    if dmg_done > 0:
        log_type = log_neg
        logs = log_event(logs, f'{dmg_done} DMG done with AP shot [original dmg = {dmg}]', log_type)
        if char_sp > 0:
            DAO.dmgCharacterSP(character.id, body_part)
        logs = damageCharacter(character, dmg_done, body_part, logs=logs)
    return logs


def damageCharacter(c: Character, dmg, body_part, logs: list[Log] = []) -> list[Log]:
    (total_dmg, body_part_destroyed) = resolveDmgDoneToCharacter(dmg, c.bodyTypeModifier)
    if total_dmg > 0:
        logs = log_event(logs, f'{c.name} damaged by {dmg}! (DMG reduced by {c.bodyTypeModifier})', log_neg)
        DAO.dmgCharacter(c.id, total_dmg)
        updated_character = DAO.getCharacterById(c.id)
        if body_part_destroyed:
            logs = log_event(logs, f"Body part hit ({body_part}) is badly damaged/destroyed!", log_neg)

        if updated_character.dmg_taken >= max_health:
            logs = log_event(logs, f'{c.name} has flatlined', log_neg)
        else:
            logs = logs + stunCheckById(updated_character.id)
    else:
        logs = log_event(logs, f'The hit did not damage target (DMG = {dmg}, DMG reduced by = {c.bodyTypeModifier})',
                         log_neutral)

    return logs


def hitCharacterById(id, body_part, dmg_str, is_ap=False, pass_sp=False):
    character = DAO.getCharacterById(id)
    return hitCharacter(character, body_part, dmg_str, is_ap, pass_sp)


def hitCharacterByName(name, body_part, dmg_str, is_ap=False, pass_sp=False):
    character = DAO.getCharacterByName(name)
    return hitCharacter(character, body_part, dmg_str, is_ap, pass_sp)


def reloadWeapon(weapon_id, shots):
    logs = []
    id = safeCastToInt(weapon_id)
    amount = safeCastToInt(shots)
    weapon = DAO.getWeaponById(id)
    if weapon is not None and amount > 0:
        if weapon.isGun():
            if weapon.clip_size < amount:
                logs = log_event(logs, f"Can't hold that many shots for {weapon.item}, clip size = {weapon.clip_size}",
                                 log_neutral)
                amount = weapon.clip_size

            DAO.updateShotsInClip(id, amount)
            logs = log_event(logs, f'{weapon.item} reloaded with {amount} shots', log_pos)
        else:
            logs = log_event(logs, f"{weapon.item} is not a gun, can't reload it", log_neutral)
    else:
        logs = log_event(logs, 'Weapon not found or invalid amount to reload', log_neg)
    return logs


def handleSingleShot(character, wep, attack_range, given_roll, skill_bonus, skill, modifiers_total, targets=1,
                     skip_luck=False, auto_roll=False):
    if modifiers_total is None:
        modifiers_total = modifiersForTarget(1)
    roll_res = safeCastToInt(given_roll)
    logs = []
    if roll_res <= 0:
        (roll_res, added_logs) = rollWithCrit(skip_luck)
        logs = logs + added_logs
    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun():
        if shots_left <= 0:
            weapon_can_attack = False

    (roll_to_beat, range_str, _) = wep.rollToBeatAndRangeStr(attack_range)

    ref_bonus = character.attributes[REF]
    total = roll_res + ref_bonus + skill_bonus + modifiers_total + wep.wa
    hit_res = roll_res > 1 and total >= roll_to_beat
    success_str = 'successful'
    failure_str = 'unsuccessful'
    end_res = success_str
    dmg = 0

    if weapon_can_attack:
        if wep.isGun():
            DAO.updateShotsInClip(wep.weapon_id, shots_left - 1)
        elif wep.weapon_type == t_thrown:
            DAO.deleteThrown(wep.weapon_id)
            logs = log_event(logs, f'Thrown weapon gone', log_neg)

        if hit_res == False:
            end_res = failure_str
            if wep.isThrown():
                logs = log_event(logs,
                                 'Roll 1D10 to see how the throw misses and another 1D10 to see how far! (See grenade table)',
                                 log_neutral)
        else:
            logs = log_event(logs, f'Attack successful!', log_pos)
            (dmg, dmg_logs) = hitDmg(wep, attack_range, targets=targets, auto_roll=auto_roll)
            logs = logs + dmg_logs
            logs = log_event(logs, f'DMG done: {dmg} {dmg_info(wep)}', log_pos)

        attack_info_str = f'{character.name} selected {wep.item} [weapon range = {wep.range}m] (TOTAL = {total}, roll = {roll_res}, skill_lvl = {skill_bonus} ({skill}), REF bonus = {ref_bonus}, WA = {wep.wa})'
        logs = log_event(logs, attack_info_str, log_neutral)

        range_info_str = f'{range_str} range attack ({attack_range}m) is {end_res} {rollToBeatStr(roll_to_beat, total)}'
        logs = log_event(logs, range_info_str, log_neutral)
    else:
        unable_str = f'Unable to attack with (id: {wep.weapon_id}) {wep.item} [Shots left: {wep.shots_left} / {wep.clip_size}]'
        logs = log_event(logs, unable_str, log_neg)

    return logs


def handleBurst(character, wep, attack_range, given_roll, skill_bonus, skill, modifiers_total, skip_luck=False,
                auto_roll=False) -> [Log]:
    logs = []
    if modifiers_total < 0 or modifiers_total is None:
        modifiers_total = modifiersForTarget(1)
    logs = log_event(logs, f'Trying burst attack with {wep.item}', log_neutral)
    roll_res = safeCastToInt(given_roll)
    if roll_res <= 0:
        (roll_res, added_logs) = rollWithCrit(skip_luck)
        logs = logs + added_logs
    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun() and wep.rof > 2:
        if shots_left <= 1:
            weapon_can_attack = False

    if weapon_can_attack:
        logs = log_event(logs, f'{wep.item} can do burst [shots left: {wep.shots_left}, rof: {wep.rof}]', log_neutral)
        (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
        ref_bonus = character.attributes[REF]

        shots_fired = 3
        if shots_left < 3:
            shots_fired = shots_left
        shots_left_after_firing = wep.shots_left - shots_fired

        total = roll_res + ref_bonus + skill_bonus + modifiers_total + wep.wa
        burst_logs = burstRoll(roll_total=total, attack_range=attack_range, wep=wep, skill=skill, roll_res=roll_res, skill_bonus=skill_bonus, ref_bonus=ref_bonus,
                               auto_roll=auto_roll)
        logs = logs + burst_logs
        DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)
    else:
        logs = log_event(logs,
                         f"Unable to do burst attack with {wep.item} ({wep.weapon_type}) [{wep.shots_left} / {wep.clip_size}] ROF: {wep.rof}",
                         log_neg)

    return logs


def handleFullAuto(character, wep, skill_bonus, skill, attack_range=0, num_of_targets=0, num_of_shots=0, roll_res=0,
                   modifiers_total=None, auto_roll=False, skip_luck=False) -> list[Log]:
    logs = []
    logs = log_event(logs, f'Trying full auto attack with {wep.item}', log_neutral)
    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun() and wep.rof > 2:
        if shots_left <= 1:
            weapon_can_attack = False

    if weapon_can_attack:
        if num_of_shots <= 0:
            print('How many shots fired? (> 1)')
            while True:
                input = askInput()
                num_of_shots = safeCastToInt(input)
                if num_of_shots > 1:
                    break
        if num_of_shots > wep.rof:
            num_of_shots = wep.rof
        if num_of_shots > shots_left:
            num_of_shots = shots_left
        logs = log_event(logs, f'Num of shots actually fired: {num_of_shots}', log_neutral)
        if num_of_targets <= 0:
            print('How many targets?')
            # multiple targets = divide shots for each
            while True:
                input = askInput()
                num_of_targets = safeCastToInt(input)
                if num_of_targets > 0:
                    break
        ref_bonus = character.attributes[REF]

        shots_left_after_firing = wep.shots_left - num_of_shots
        # test one roll for whole full auto attack
        if roll_res <= 0:
            roll_res = resolveAutoOrManualRollWithCrit(auto_roll=auto_roll, skip_luck=skip_luck)
        roll_total = roll_res + ref_bonus + skill_bonus + modifiers_total + wep.wa
        full_auto_logs = fullAutoRoll(roll_total, wep, skill, skill_bonus, roll_res, ref_bonus, attack_range,
                                      num_of_targets, num_of_shots, modifiers_total, auto_roll, skip_luck)
        logs = logs + full_auto_logs

        DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)
    else:
        logs = log_event(logs, f"Can't attack with {wep.item} [{wep.shots_left} / {wep.clip_size}]", log_neg)

    return logs


def handleMeleeDmgByCharacterId(character_id, roll, wep_id, method=None):
    character = DAO.getCharacterById(character_id)
    return handleMeleeDmg(character, roll, wep_id, method)


def handleMeleeDmgByCharacterName(name, roll, method=None):
    character = DAO.getCharacterByName(name)
    return handleMeleeDmg(character, roll, method)


def characterAttack(character, attack_type, attack_range, given_roll):
    wep = weaponByAttackType(attack_type, character)
    (skill_bonus, skill) = characterSkillBonusForWeapon(character, wep.weapon_type)

    if wep is not None:
        weapon_info(wep)
        if attack_type == attack_type_single:
            handleSingleShot(character, wep, attack_range, given_roll, skill_bonus, skill, modifiers_total=None)
        elif attack_type == attack_type_burst:
            handleBurst(character, wep, attack_range, given_roll, skill_bonus, skill)
        elif attack_type == attack_type_full_auto:
            handleFullAuto(character, wep, skill_bonus, skill)
        elif attack_type == attack_type_melee:
            handleMelee(character, wep, given_roll, skill_bonus, skill)
    else:
        print(f'{character.name} has no ways of attack for {attack_type}')


# TODO: collect all printed lines are array of strings/some result json and return to UI to be printed..?
def characterAttackById(id, attack_type, range_str, given_roll):
    attack_range = safeCastToInt(range_str)
    if attack_range > 0:
        character = DAO.getCharacterById(id)
        if character is not None:
            characterAttack(character, attack_type, attack_range, given_roll)
    else:
        print(f'Range must be bigger than 0')


def characterAttackByName(name, attack_type, range_str, given_roll):
    attack_range = safeCastToInt(range_str)
    if attack_range > 0:
        character = DAO.getCharacterByName(name)
        if character is not None:
            characterAttack(character, attack_type, attack_range, given_roll)
    else:
        print(f'Range must be bigger than 0')


def characterAttackByCharacterAndWeaponId(character_id, weapon_id, attack_type, attack_range, given_roll,
                                          attack_modifier, targets, shots_fired=1):
    character = DAO.getCharacterById(character_id)
    result_logs = []
    if character is not None:
        wep = weaponByAttackTypeAndWeaponId(character, weapon_id, attack_type)
        if wep is not None:
            weapon_info(wep)
            (skill_bonus, skill) = characterSkillBonusForWeapon(character, wep.weapon_type)
            if attack_type == attack_type_single:
                result_logs = handleSingleShot(
                    character=character,
                    wep=wep,
                    attack_range=attack_range,
                    given_roll=given_roll,
                    skill_bonus=skill_bonus,
                    skill=skill,
                    modifiers_total=attack_modifier,
                    targets=targets,
                    skip_luck=True,
                    auto_roll=True
                )
            elif attack_type == attack_type_melee:
                result_logs = handleMelee(
                    character=character,
                    wep=wep,
                    given_roll=given_roll,
                    skill_bonus=skill_bonus,
                    skill=skill,
                    modifiers_total=attack_modifier
                )
            elif attack_type == attack_type_burst:
                result_logs = handleBurst(
                    character=character,
                    wep=wep,
                    attack_range=attack_range,
                    given_roll=given_roll,
                    skill_bonus=skill_bonus,
                    skill=skill,
                    modifiers_total=attack_modifier,
                    skip_luck=True,
                    auto_roll=True
                )
            elif attack_type == attack_type_full_auto:
                result_logs = handleFullAuto(
                    character=character,
                    wep=wep,
                    roll_res=given_roll,
                    num_of_shots=shots_fired,
                    num_of_targets=targets,
                    attack_range=attack_range,
                    skill_bonus=skill_bonus,
                    skill=skill,
                    modifiers_total=attack_modifier,
                    auto_roll=True,
                    skip_luck=True
                )
        else:
            wep_not_found = Log(f'Weapon not found [character_id = {character_id}, weapon_id = {weapon_id}]', log_neg)
            wep_not_found.log()
            result_logs.append(wep_not_found.toJson())
    else:
        char_not_found = Log(f'Character not found [character_id = {character_id}]', log_neg)
        char_not_found.log()
        result_logs.append(char_not_found.toJson())

    return result_logs


#TODO: add to the app?
def suppressiveFireDef(name, rounds, area):
    shots_in_area = safeCastToInt(rounds)
    area_width = safeCastToInt(area)
    if shots_in_area > 0 and area_width > 0:
        character = DAO.getCharacterByName(name)
        if character is not None:
            (roll_res, _) = rollWithCrit()
            athletics_bonus = skillBonusForSkill(character.skills, skill_athletics)
            ref_bonus = character.attributes[REF]
            total = roll_res + athletics_bonus + ref_bonus
            roll_to_beat = math.floor(shots_in_area / area_width)
            if total >= roll_to_beat:
                printGreenLine(f'{character.name} avoided suppressive fire!')
            else:
                hits = roll(1, 6)
                if hits > shots_in_area:
                    hits = shots_in_area
                printRedLine(f'{character.name} got hit by suppressive fire {hits} times!')
    else:
        print(f'Suppressive area needs at least one shot fired into it and valid area width')

# Healing

def medicalCheck(name, given_roll):
    character = DAO.getCharacterByName(name)
    if character is not None:
        tech_bonus = character.attributes[TECH]
        first_aid_bonus = skillBonusForSkill(character.skills, skill_first_aid)
        med_tech_bonus = 0  # house rule
        healing_rate = 1
        if character.role == meditechie:
            healing_rate += 1
            med_tech_bonus = math.ceil(character.specialAbility / 2)

        print(f'Patient will heal {healing_rate}hp/day')


        print(f'House rule by programmer: med tech bonus gives (med_tech / 2) bonus to first aid skill and also +1 to healing rate')
        print(f"""Select difficulty of medical check or {list_str} for roll info:
1 = Easy
2 = Average
3 = Difficult
4 = Very difficult
5 = Nearly impossible 
""")
        to_beat = 0
        while True:
            input = askInput()
            i = safeCastToInt(input) - 1
            if checkListCommand(input):
                difficultyCheckInfo()
            elif i == 0:
                to_beat = easy_check
                break
            elif i == 1:
                to_beat = average_check
                break
            elif i == 2:
                to_beat = difficult_check
                break
            elif i == 3:
                to_beat = very_difficult_check
                break
            elif i == 4:
                to_beat = nearly_impossible_check
                break

        t_roll = safeCastToInt(given_roll)
        if t_roll > 0:
            roll_res = t_roll
        else:
            (roll_res, _) = rollWithCrit()
        total = tech_bonus + first_aid_bonus + med_tech_bonus + roll_res

        info = f'Roll total ({total}) vs {to_beat} [roll = {roll_res}, first aid bonus = {first_aid_bonus}, medtech bonus = {med_tech_bonus}, tech_bonus = {tech_bonus}]'
        if total >= to_beat:
            printGreenLine(f'Medical check successful! {info}')
        else:
            printRedLine(f'Medical check unsuccessful! {info}')

def healCharacter(char, amount) -> list[Log]:
    logs = []
    if char is not None:
        healing = safeCastToInt(amount)
        dmg_taken = char.dmg_taken
        dmg_taken -= healing
        if dmg_taken < 0:
            dmg_taken = 0
        DAO.healCharacter(char.id, dmg_taken)
        logs = log_event(logs, f"{char.name} healed by {healing}", log_pos)
    else:
        logs = log_event(logs, f"Character not found to heal", log_neg)

    return logs


def healCharacterById(id, amount) -> list[Log]:
    char = DAO.getCharacterById(id)
    return healCharacter(char, amount)

def healCharacterByName(name, amount) -> list[Log]:
    char = DAO.getCharacterByName(name)
    return healCharacter(char, amount)

# IP stuff


def saveIP(character_id, ip_amount) -> list[Log]:
    logs = []
    character = DAO.getCharacterById(character_id)
    if character is not None:
        DAO.updateCharacterIp(character_id, ip_amount)
        logs = log_event(logs, f'{ip_amount} IP for {character.name}', log_pos)
    else:
        logs = log_event(logs, f'Character not found [character_id = {character_id}]')

    return logs

# Campaigns

def allCampaigns():
    rows = DAO.listCampaigns()
    campaigns = map(lambda r: (
        Campaign(r).asJson()
    ), rows)

    return list(campaigns)


def addCampaign(name: str, info: str | None):
    DAO.addCampaign(name, info)


def updateCampaignInfo(campaignId: int, info: str | None):
    DAO.updateCampaignInfo(campaignId, info)


def campaignEvents(campaignId: int):
    rows = DAO.campaignEvents(campaignId)
    events = []
    for row in rows:
        event_id = row['id']
        event_character_rows = DAO.eventChracters(event_id)
        ce = CampaignEvent(row, event_character_rows).asJson()
        events.append(ce)
    return list(events)


def campaignGigs(campaignId: int):
    rows = DAO.campaignGigs(campaignId)
    gigs = []
    for row in rows:
        gig_id = row['id']
        gig_character_rows = DAO.gigChracters(gig_id)
        ce = CampaignGig(row, gig_character_rows).asJson()
        gigs.append(ce)
    return list(gigs)


def addCampaignEvent(campaignId: int, sessionNumber, info: str | None):
    DAO.addEvent(campaignId, sessionNumber, info)


def updateEventInfo(eventId: int, info: str | None):
    DAO.updateEventInfo(eventId, info)


def addEventCharacter(eventId: int, characterId: int):
    DAO.addEventCharacter(eventId, characterId)
    event_row = DAO.eventCampaign(eventId)
    campaign_id = event_row['campaign_id']
    return campaignEvents(campaign_id)


def addCampaignGig(campaign_id: int, name: str, info: str | None, status: str):
    DAO.addGig(campaign_id, name, info, status)


def updateGigStatus(gigId: int, status: str):
    assert(valid_gig_statuses.__contains__(status))
    DAO.updateGigStatus(gigId, status)


def updateGigInfo(gigId: int, info: str | None):
    DAO.updateGigInfo(gigId, info)


def addGigCharacter(gigId: int, characterId: int):
    DAO.addGigCharacter(gigId, characterId)
    gig_row = DAO.gigCampaign(gigId)
    campaign_id = gig_row['campaign_id']
    return campaignGigs(campaign_id)


def deleteGigCharacter(gigId: int, characterId: int):
    DAO.deleteGigCharacter(gigId, characterId)


def deleteEventCharacter(eventId: int, characterId: int):
    DAO.deleteEventCharacter(eventId, characterId)

