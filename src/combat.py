import math

import dice
from character import Character
import bodytypes
from db import cyberdao as DAO
from src.gameHelper import stunPenalty, body_part_body, body_part_head, body_part_l_leg, body_part_r_arm, \
    body_part_l_arm, body_part_r_leg, safeCastToInt, max_health, askInput, REF, t_melee, t_handgun, t_rifle, t_shotgun, \
    t_thrown, roll_str, guns, close_range_str, medium_range_str, attack_type_single, attack_type_burst, \
    attack_type_full_auto, point_blank_range_str, attack_type_melee, unarmed, melee_dmg_help_str, skill_athletics
from src.weapon import Weapon


# TODO: add auto shotguns
# TODO: add AP rounds (shotgun, rifle?)

def weaponsByType(attack_type, weapons):
    weps = []
    if attack_type == attack_type_melee:
        for w in weapons:
            if w.weapon_type == 'melee':
                weps.append(w)
    elif attack_type == attack_type_burst or attack_type == attack_type_full_auto:
        for w in weapons:
            if w.rof > 2:
                weps.append(w)
    elif attack_type == attack_type_single:
        for w in weapons:
            if w.weapon_type != 'melee':
                weps.append(w)
    return weps

def weaponByAttackType(attack_type, character):
    weapons = weaponsByType(attack_type, character.weapons)
    idx = 0
    if len(weapons) > 0:
        print(f'Select weapon num: ')
        for w in weapons:
            i = weapons.index(w)
            print(f'{i} - {w.item}')
        while True:
            input = askInput()
            idx = safeCastToInt(input)
            if 0 <= idx < len(weapons):
                break
        wep: Weapon = weapons[idx]
        return wep
    else:
        print(f'No weapons found for {attack_type}')
        return None

def suppressiveFireDef(name, rounds, area):
    shots_in_area = safeCastToInt(rounds)
    area_width = safeCastToInt(area)
    if shots_in_area > 0 and area_width > 0:
        character = DAO.getCharacterByName(name)
        if character is not None:
            roll = dice.rollWithCrit()
            athletics_bonus = skillBonusForSkill(character.skills, skill_athletics)
            ref_bonus = character.attributes[REF]
            total = roll + athletics_bonus + ref_bonus
            roll_to_beat = math.floor(shots_in_area / area_width)
            if total > roll_to_beat:
                print(f'{character.name} avoided suppressive fire!')
            else:
                hits = dice.roll(1, 6)
                if hits > shots_in_area:
                    hits = shots_in_area
                print(f'{character.name} got hit by suppressive fire {hits} times!')
    else:
        print(f'Suppressive area needs at least one shot fired into it and valid area width')


def characterAttack(name, attack_type, range_str, given_roll):
    attack_range = safeCastToInt(range_str)
    if attack_range > 0:
        character = DAO.getCharacterByName(name)
        if character is not None:
            weapons = weaponsByType(attack_type, character.weapons)
            idx = 0
            wep = weaponByAttackType(attack_type, character)
            if wep is not None:
                if attack_type == attack_type_single:
                    handleSingleShot(character, wep, attack_range, given_roll)
                elif attack_type == attack_type_burst:
                    handleBurst(character, wep, attack_range, given_roll)
                elif attack_type == attack_type_full_auto:
                    handleFullAuto(character, wep)
                elif attack_type == attack_type_melee:
                    handleMelee(character, wep)
            else:
                print(f'{character.name} has no ways of attack for {attack_type}')

    else:
        print(f'Range must be bigger than 0')


def meleeDamageModifierByStrength(character):
    dmg_bonus = 0
    match character.bodyTypeModifier:
        case 'very weak':
            dmg_bonus = -2
        case 'weak':
            dmg_bonus = -1
        case 'average':
            dmg_bonus = 0
        case 'strong':
            dmg_bonus = 1
        case 'very strong':
            dmg_bonus = 2
        case _:
            print('TODO for super human levels')
    return dmg_bonus


melee_attacks = [
    'weapon',
    'strike',
    'kick',
    'throw',
    'choke',
]

def handleMelee(character, wep):
    ref_bonus = character.attributes[REF]
    skill_bonus = 0
    if wep.item == unarmed:
        print('Give skill for bonus (e.g. brawling, karate, judo...)')
        skill = askInput()
        skill_bonus = skillBonusForSkill(character.skills, skill)

    else:
        (skill_b, skill) = characterSkillBonusForWeapon(character, wep.weapon_type)
        skill_bonus = skill_b


    roll = dice.resolveAutoOrManualRollWithCrit()
    total = roll + ref_bonus + skill_bonus
    print(f'{character.name} attacks with {wep.item} (Roll total = {total})')
    print("Defend against melee attack by rolling opponent's REF + <some appropriate skill> + 1D10")
    print(f'If attack is successful, {melee_dmg_help_str}')


def handleMeleeDmg(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        dmg_bonus = bodytypes.meleeDmgBonusByModifier(character.bodyTypeModifier)
        different_melee_attacks = ', '.join(melee_attacks)
        dmg = 0
        print(f'Give attack method ({different_melee_attacks}):')
        while True:
            method = askInput()
            match method:
                case 'weapon':
                    wep = weaponByAttackType(attack_type_melee, character)
                    if wep is not None:
                        dmg = dice.roll(wep.dice_num, wep.dice_dmg) + wep.dmg_bonus + dmg_bonus
                        break
                case 'strike':
                    dmg = math.floor(dice.roll(1, 6) / 2) + dmg_bonus
                    break
                case 'kick':
                    dmg = dice.roll(1, 6) + dmg_bonus
                    break
                case 'throw':
                    dmg = dice.roll(1, 6) + dmg_bonus
                    break
                case 'choke':
                    dmg = dice.roll(1, 6)
                    break
        hit_loc = determineHitLocation()
        print(f'Did {dmg} DMG to {hit_loc} using {method}')



def characterSkillBonusForWeapon(character, wep_t) -> (int, str):
    skill_bonus = 0
    skill = ''
    skills = character.skills
    if wep_t == t_melee:
        skill = 'melee'
    elif wep_t == t_rifle or wep_t == t_shotgun:
        skill = 'rifle'
    elif wep_t == t_handgun:
        skill = 'handgun'
    elif wep_t == t_thrown:
        skill = skill_athletics
    skill_bonus = skillBonusForSkill(skills, skill)

    return (skill_bonus, skill)


def handleFullAuto(character, wep):
    print(f'Trying full auto attack with {wep.item}')
    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun() and wep.rof > 2:
        if shots_left <= 1:
            weapon_can_attack = False

    if weapon_can_attack:
        print('How many shots fired? (> 1)')
        num_of_shots = 0
        while True:
            input = askInput()
            num_of_shots = safeCastToInt(input)
            if num_of_shots > 1:
                break
        if num_of_shots > wep.rof:
            num_of_shots = wep.rof
        print('How many targets?')
        num_of_targets = 0
        #multiple targets = divide shots for each
        while True:
            input = askInput()
            num_of_targets = safeCastToInt(input)
            if num_of_targets > 0:
                break

        (skill_bonus, skill) = characterSkillBonusForWeapon(character, wep.weapon_type)
        ref_bonus = character.attributes[REF]
        range_bonus = math.ceil(num_of_shots / 10)
        shots_per_target = math.ceil(num_of_targets / num_of_shots)

        shots_left_after_firing = wep.shots_left - num_of_shots

        targets_hit = 0
        for target in range(num_of_targets):
            t = target + 1
            print(f'Rolling attack for target {t} / {num_of_targets}')
            print(f'Give range for target {t}:')
            attack_range = 0
            while True:
                i = askInput()
                attack_range = safeCastToInt(i)
                if attack_range > 0:
                    break

            target_total_dmg = 0
            roll = dice.resolveAutoOrManualRollWithCrit()
            total = roll + ref_bonus + skill_bonus + range_bonus

            (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
            if not (r == close_range_str or r == point_blank_range_str):
                range_bonus = -1 * range_bonus

            if total > roll_to_beat:
                targets_hit = targets_hit + 1
                num_of_hits = total - roll_to_beat
                if num_of_hits > shots_per_target:
                    num_of_hits = shots_per_target
                print(f'Target {t} hit {num_of_hits} times!')
                for i in range(num_of_hits):
                    dmg = hitDmg(wep)
                    target_total_dmg = target_total_dmg + dmg
                print(f'Total dmg done to target {t}: {target_total_dmg}')

            else:
                print(f'Full auto missed target {t}!')

            DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)
            print(f'{num_of_shots} shots fired in full auto hitting {num_of_hits} times')



def handleBurst(character, wep, attack_range, given_roll):
    print(f'Trying burst attack with {wep.item}')
    roll = safeCastToInt(given_roll)
    if roll <= 0:
        roll = dice.rollWithCrit()
    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun() and wep.rof > 2:
        if shots_left <= 1:
            weapon_can_attack = False

    if weapon_can_attack:
        print(f'{wep.item} can do burst [shots left: {wep.shots_left}, rof: {wep.rof}]')
        (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
        (skill_bonus, skill) = characterSkillBonusForWeapon(character, wep.weapon_type)
        ref_bonus = character.attributes[REF]
        range_bonus = 0
        if r == close_range_str or r == medium_range_str:
            range_bonus = 3

        shots_fired = 3
        if shots_left < 3:
            shots_fired = shots_left
        shots_left_after_firing = wep.shots_left - shots_fired

        total = roll + ref_bonus + skill_bonus + range_bonus
        print(f'[roll to beat ({roll_to_beat}) vs total ({total})]')
        if total >= roll_to_beat:
            hits = math.ceil(dice.roll(1, 6) / 2)
            if shots_fired < 3 and hits == 3:
                hits = shots_left
            total_dmg = 0
            print(f'{hits} hits to target!')
            for i in range(hits):
                dmg = hitDmg(wep)
                total_dmg = total_dmg + dmg
            print(f'Total dmg done to target: {total_dmg}')
        else:
            print(f'Burst attack misses target!')
        DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)

    else:
        print(f"Unable to do burst attack with {wep.item} ({wep.weapon_type}) [{wep.shots_left} / {wep.clip_size}] ROF: {wep.rof}")



def handleSingleShot(character, wep, attack_range, given_roll):
    roll = safeCastToInt(given_roll)
    if roll <= 0:
        roll = dice.rollWithCrit()

    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun():
        if shots_left <= 0:
            weapon_can_attack = False

    (roll_to_beat, range_str, _) = wep.rollToBeatAndRangeStr(attack_range)

    (skill_bonus, skill) = characterSkillBonusForWeapon(character, wep.weapon_type)
    ref_bonus = character.attributes[REF]
    total = roll + ref_bonus + skill_bonus
    # TODO: add modifiers?
    hit_res = total >= roll_to_beat
    end_res = 'successful'
    dmg = 0
    if weapon_can_attack:
        if wep.isGun():
            print(f'... wep_id: {wep.weapon_id} ... wpn: {wep.item} .. clip: {wep.shots_left} / {wep.clip_size} ')
            DAO.updateShotsInClip(wep.weapon_id, shots_left - 1)
        if hit_res == False:
            end_res = 'unsuccessful'
        else:
            print(f'Attack successful!')
            dmg = hitDmg(wep)
            print(f'DMG done: {dmg}')

        print(f'{character.name} selected {wep.item} [range = {wep.range}m] (roll = {roll} skill_lvl = {skill_bonus} ({skill}) REF bonus = {ref_bonus})')
        print(f'{range_str} range attack ({attack_range}m) is {end_res} [roll to beat ({roll_to_beat}) vs total ({total})]')
    else:
        print(
            f'Unable to attack with (id: {wep.weapon_id}) {wep.item} [Shots left: {wep.shots_left} / {wep.clip_size}]')


def hitDmg(wep):
    print(f'{roll_str} or give dmg (> 0):')
    dmg = 0
    while True:
        input = askInput()
        if input == roll_str:
            dmg = dice.roll(wep.dice_num, wep.dice_dmg) + wep.dmg_bonus
            break
        else:
            dmg = safeCastToInt(input)
            if dmg > 0:
                break
    location = determineHitLocation()
    print(f'{dmg} DMG to {location}')
    return dmg

def reloadWeapon(weapon_id, shots):
    id = safeCastToInt(weapon_id)
    amount = safeCastToInt(shots)
    weapon = DAO.getWeaponById(id)
    if weapon is not None and amount > 0:
        if weapon.isGun():
            if weapon.clip_size < amount:
                print(f"Can't hold that many shots for {weapon.item}, clip size = {weapon.clip_size}")
                amount = weapon.clip_size

            DAO.updateShotsInClip(id, amount)
            print(f'{weapon.item} reloaded with {amount} shots')
        else:
            print(f"{weapon.item} is not a gun, can't reload it")


def skillBonusForSkill(skills, skill):
    skill_bonus = 0
    for s in skills:
        if s.skill == skill:
            skill_bonus = s.lvl

    if not skills.__contains__(skill):
        print(f'{skill} not found in character skills')
    return skill_bonus


def dmgReductionByBodyTypeModifier(bodyTypeModifier):
    reduction = bodyTypeModifier
    if reduction is None:
        print(f'Unknown body type {bodyTypeModifier}')
        return 0
    else:
        return reduction


def hitCharacter(name, body_part, dmg_str):
    dmg = safeCastToInt(dmg_str)
    character = DAO.getCharacterByName(name)
    if character is not None:
        char_sp = character.sp[body_part]
        sp_left = 0
        if char_sp > 0:
            sp_left = char_sp - dmg
            if sp_left >= 0:
                print(f'Armor damaged at {body_part}')
                DAO.dmgCharacterSP(character.id, body_part, dmg)
            else:
                print(f'Armor broken at {body_part}')
                dmg_left = abs(sp_left)
                DAO.dmgCharacterSP(character.id, body_part, char_sp)
                damageCharacter(character, dmg_left)
        else:
            damageCharacter(character, dmg)


def damageCharacter(c: Character, dmg):
    dmgReduction = c.bodyTypeModifier
    total_dmg = dmg - dmgReduction
    if total_dmg > 0:
        print(f'{c.name} damaged by {dmg}!')
        DAO.dmgCharacter(c.id, total_dmg)
        updated_character = DAO.getCharacterByName(c.name)
        if (updated_character.dmg_taken >= max_health):
            print(f'{c.name} has flatlined')
        else:
            stunCheck(updated_character)


def determineHitLocation() -> str:
    print(f'determining hit location')
    roll = dice.roll(1, 10)
    hit_loc = ''
    if roll == 1:
        hit_loc = body_part_head
    elif 2 <= roll <= 4:
        hit_loc = body_part_body
    elif roll == 5:
        hit_loc = body_part_r_arm
    elif roll == 6:
        hit_loc = body_part_l_arm
    elif 7 <= roll <= 8:
        hit_loc = body_part_r_leg
    else:
        hit_loc = body_part_l_leg

    return hit_loc

def rollStunOverActingEffect(name):
    print(f'{name} gets stunned! Rolling stun effect')
    roll = dice.roll(1, 6)
    if roll == 1:
        return f'{name} screams, windmills arms, falls'
    elif roll == 2:
        return f'{name} crumples like a rag doll'
    elif roll == 3:
        return f'{name} spins around in place, falls'
    elif roll == 4:
        return f'{name} clutches wound, staggers and falls'
    elif roll == 5:
        return f'{name} stares stupidly at wound, then falls'
    else:
        return f'{name} slumps into ground, moaning'


def stunCheckToBeat(dmg_taken, body):
    penalty = stunPenalty(dmg_taken)
    if penalty > 0:
        print(f'penalty for {dmg_taken} dmg taken is {penalty}')
    save_against = body - penalty
    if (save_against > 0):
        print(f'To not be stunned/shocked (or to not lose death save), roll {save_against} or lower')
    else:
        print(f'Stun/shock saves cannot help anymore, character needs to be stabilized fast')

    return save_against


def stunCheck(c: Character):
    save_against = stunCheckToBeat(c.dmg_taken, c.attributes['BODY'])
    roll = dice.roll(1, 10)
    isStunned = roll > save_against

    if isStunned:
        print(rollStunOverActingEffect(c.name))

    return isStunned
