import math
import random

import dice
from character import Character
import bodytypes
import cyberdao as DAO
from gameHelper import stunPenalty, body_part_body, body_part_head, body_part_l_leg, body_part_r_arm, \
    body_part_l_arm, body_part_r_leg, safeCastToInt, max_health, askInput, REF, t_melee, t_handgun, t_rifle, t_shotgun, \
    t_thrown, roll_str, close_range_str, medium_range_str, attack_type_single, attack_type_burst, \
    attack_type_full_auto, point_blank_range_str, attack_type_melee, unarmed, melee_dmg_help_str, body_parts, \
    t_heavy_weapon, printColorLine, printRedLine, printGreenLine, coloredText, t_smg
from skills import skillBonusForSkill, skill_athletics
from weapon import Weapon
from colorama import Fore, Style

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
        printRedLine(f'No weapons found for {attack_type}')
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
            if total >= roll_to_beat:
                printGreenLine(f'{character.name} avoided suppressive fire!')
            else:
                hits = dice.roll(1, 6)
                if hits > shots_in_area:
                    hits = shots_in_area
                printRedLine(f'{character.name} got hit by suppressive fire {hits} times!')
    else:
        print(f'Suppressive area needs at least one shot fired into it and valid area width')

def characterAttack(character, attack_type, attack_range, given_roll):
    wep = weaponByAttackType(attack_type, character)
    (skill_bonus, skill) = characterSkillBonusForWeapon(character, wep.weapon_type)

    if wep is not None:
        if wep.effect_radius > 0:
            print(
                f'Hit affects radius of {wep.effect_radius} - Check also if hit misses or if there are other targets in the radius!')
        if wep.weapon_type == t_shotgun:
            print(
                """For shotguns, point blank/short range attack is for one spot, mid range hits 2 spots and long/extreme hits 3 places."""
            )
        if attack_type == attack_type_single:
            handleSingleShot(character, wep, attack_range, given_roll, skill_bonus, skill)
        elif attack_type == attack_type_burst:
            handleBurst(character, wep, attack_range, given_roll, skill_bonus, skill)
        elif attack_type == attack_type_full_auto:
            handleFullAuto(character, wep, skill_bonus, skill)
        elif attack_type == attack_type_melee:
            handleMelee(character, wep, given_roll, skill_bonus, skill)
    else:
        print(f'{character.name} has no ways of attack for {attack_type}')


#TODO: collect all printed lines are array of strings/some result json and return to UI to be printed..?
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


def modifiersForTarget(target_num):
    print(
        f'Give attack modifier total for target {target_num} (e.g. immobile target, ambush, target size... Full auto/3 round burst is done automatically)')
    i = askInput()
    modifiers_total = safeCastToInt(i)
    return modifiers_total


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


def handleMelee(character, wep, given_roll, skill_bonus, skill):
    modifiers_total = modifiersForTarget(1)
    ref_bonus = character.attributes[REF]
    if wep.item == unarmed:
        print('Give skill for bonus (e.g. brawling, karate, judo...)')
        skill = askInput()
        skill_bonus = skillBonusForSkill(character.skills, skill)
    t_roll = safeCastToInt(given_roll)
    roll = 0
    if t_roll > 0:
        roll = t_roll
    else:
        roll = dice.rollWithCrit()
    total = roll + ref_bonus + skill_bonus + modifiers_total
    printGreenLine(f'{character.name} attacks with {wep.item} (Roll total = {total})')
    print(f'If attack is successful, calculate damage for roll (or automatically roll dmg) with {melee_dmg_help_str}')
    print(f'(dice roll = {roll}, REF bonus = {ref_bonus}, skill_bonus = {skill_bonus} ({skill}), modifiers = {modifiers_total})')
    printRedLine("Defend against melee attack by rolling opponent's REF + dodge skill + 1D10")


def handleMeleeDmg(name, roll):
    dmg_roll = safeCastToInt(roll)
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
                    if dmg_roll == 0:
                        dmg_roll = dice.roll(wep.dice_num, wep.dice_dmg, divide_by=wep.divide_by, bonus=wep.dmg_bonus)
                    if wep is not None:
                        dmg = dmg_roll + dmg_bonus
                        method = wep.item
                        break
                case 'strike':
                    if dmg_roll == 0:
                        dmg_roll = dice.roll(1, 6, divide_by=2)
                    dmg = dmg_roll + dmg_bonus
                    break
                case 'kick':
                    if dmg_roll == 0:
                        dice.roll(1, 6)
                    dmg = dmg_roll + dmg_bonus
                    break
                case 'throw':
                    if dmg_roll == 0:
                        dice.roll(1, 6)
                    dmg = dmg_roll + dmg_bonus
                    break
                case 'choke':
                    if dmg_roll == 0:
                        dice.roll(1, 6)
                    dmg = dmg_roll
                    break
        hit_loc = determineHitLocation()
        printGreenLine(f'{character.name} did {dmg} DMG to {hit_loc} using {method}')


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
    elif wep_t == t_heavy_weapon:
        skill = 'heavy weapons'
    elif wep_t == t_smg:
        skill = 'smg'
    skill_bonus = skillBonusForSkill(skills, skill)

    return (skill_bonus, skill)


def handleFullAuto(character, wep, skill_bonus, skill):
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
        if num_of_shots > shots_left:
            num_of_shots = shots_left
        print(f'Num of shots: {num_of_shots}')
        print('How many targets?')
        num_of_targets = 0
        # multiple targets = divide shots for each
        while True:
            input = askInput()
            num_of_targets = safeCastToInt(input)
            if num_of_targets > 0:
                break
        ref_bonus = character.attributes[REF]
        range_bonus = math.ceil(num_of_shots / 10)
        shots_per_target = math.ceil(num_of_shots / num_of_targets)

        shots_left_after_firing = wep.shots_left - num_of_shots

        targets_hit = 0
        total_hits = 0
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

            modifiers_total = modifiersForTarget(t)
            target_total_dmg = 0
            roll = dice.resolveAutoOrManualRollWithCrit()
            (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
            if not (r == close_range_str or r == point_blank_range_str):
                range_bonus = -1 * range_bonus
            total = roll + ref_bonus + skill_bonus + range_bonus + modifiers_total + wep.wa
            num_of_hits = 0
            print(
                f'{rollToBeatStr(roll_to_beat, total)} '
                f'[roll = {roll}, REF bonus = {ref_bonus}, skill_bonus = {skill_bonus} ({skill}), range bonus = {range_bonus} WA = {wep.wa}]'
            )

            if total >= roll_to_beat:
                targets_hit = targets_hit + 1
                num_of_hits = total - roll_to_beat
                if num_of_hits >= shots_per_target:
                    num_of_hits = shots_per_target
                if num_of_hits <= 0:
                    num_of_hits = 1

                total_hits = total_hits + num_of_hits

                printGreenLine(f'Target {t} hit {num_of_hits} times!')

                for i in range(num_of_hits):
                    dmg = hitDmg(wep, attack_range)
                    target_total_dmg = target_total_dmg + dmg
                printGreenLine(f'Total dmg done to target [{t}]: {target_total_dmg}')

            else:
                printRedLine(f'Full auto missed target {t}!')

            DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)
        printGreenLine(f'{num_of_shots} shots fired in full auto with {wep.item} hitting {total_hits} times')
    else:
        printRedLine(f"Can't attack with {wep.item} [{wep.shots_left} / {wep.clip_size}]")


def rollToBeatStr(to_beat, total):
    return f'[{coloredText(Fore.RED, f"roll to beat ({to_beat})")} vs {coloredText(Fore.GREEN, f"total ({total})")}]'


def handleBurst(character, wep, attack_range, given_roll, skill_bonus, skill):
    modifiers_total = modifiersForTarget(1)
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
        ref_bonus = character.attributes[REF]
        range_bonus = 0
        if r == close_range_str or r == medium_range_str:
            range_bonus = 3

        shots_fired = 3
        if shots_left < 3:
            shots_fired = shots_left
        shots_left_after_firing = wep.shots_left - shots_fired

        total = roll + ref_bonus + skill_bonus + range_bonus + modifiers_total + wep.wa
        print(rollToBeatStr(roll_to_beat, total))
        if total >= roll_to_beat:
            hits = dice.roll(1, 6, divide_by=2)
            if shots_fired < 3 and hits == 3:
                hits = shots_left
            total_dmg = 0
            printGreenLine(f'{hits} hits to target!')
            print(
                f'{character.name} selected {wep.item} [range = {wep.range}m] '
                f'(roll = {roll} vs roll to beat {roll_to_beat} - skill_lvl = {skill_bonus} ({skill}) REF bonus = {ref_bonus} WA = {wep.wa})'
            )
            for i in range(hits):
                dmg = hitDmg(wep, attack_range)
                total_dmg = total_dmg + dmg
            printGreenLine(f'Total dmg done to target: {total_dmg}')
        else:
            printRedLine(f'Burst attack misses target!')
        DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)

    else:
        printRedLine(
            f"Unable to do burst attack with {wep.item} ({wep.weapon_type}) [{wep.shots_left} / {wep.clip_size}] ROF: {wep.rof}"
        )


def handleSingleShot(character, wep, attack_range, given_roll, skill_bonus, skill):
    modifiers_total = modifiersForTarget(1)
    roll = safeCastToInt(given_roll)
    if roll <= 0:
        roll = dice.rollWithCrit()

    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun():
        if shots_left <= 0:
            weapon_can_attack = False

    (roll_to_beat, range_str, _) = wep.rollToBeatAndRangeStr(attack_range)

    ref_bonus = character.attributes[REF]
    total = roll + ref_bonus + skill_bonus + modifiers_total + wep.wa
    hit_res = total >= roll_to_beat
    success = coloredText(Fore.GREEN, 'successful')
    failure = coloredText(Fore.RED, 'unsuccessful')
    end_res = success
    dmg = 0

    if weapon_can_attack:
        if wep.isGun():
            DAO.updateShotsInClip(wep.weapon_id, shots_left - 1)
        elif wep.weapon_type == t_thrown:
            DAO.deleteThrown(wep.weapon_id)
            printRedLine(f'Thrown weapon gone')

        if hit_res == False:
            end_res = failure
            if wep.isThrown():
                print('Roll 1D10 to see how the throw misses and another 1D10 to see how far! (See grenade table)')
        else:
            printGreenLine(f'Attack successful!')
            dmg = hitDmg(wep, attack_range)
            printGreenLine(f'DMG done: {dmg}')

        print(
            f'{character.name} selected {wep.item} [range = {wep.range}m] (roll = {roll} skill_lvl = {skill_bonus} ({skill}) REF bonus = {ref_bonus} WA = {wep.wa})'
        )
        print(
            f'{range_str} range attack ({attack_range}m) is {end_res} {rollToBeatStr(roll_to_beat, total)}'
        )
    else:
        printRedLine(
            f'Unable to attack with (id: {wep.weapon_id}) {wep.item} [Shots left: {wep.shots_left} / {wep.clip_size}]'
        )


def hitDmg(wep, attack_range):
    dmg = 0
    targets = 0
    if wep.weapon_type == t_shotgun:
        print('Give targets in shotgun spread area (At least main target is hit, others have 50/50 a chance of not being hit):')
        while True:
            input = askInput()
            targets = safeCastToInt(input)
            if targets > 0:
                break

        for target in range(targets):
            t_dmg = 0
            print(f'Target {target + 1}:')
            if target > 1:
                hit = dice.roll(1, 2)
                if hit > 1:
                    t_dmg = handleShotgunDmgAndHit(wep, attack_range)
            else:
                t_dmg = handleShotgunDmgAndHit(wep, attack_range)

            dmg += t_dmg

    else:
        dmg = handleWeaponDmgAndHit(wep, attack_range)
    return dmg


def handleWeaponDmgAndHit(wep, attack_range):
    print(f'{roll_str} or give dmg (> 0):')
    dmg = 0
    while True:
        input = askInput()
        if input == roll_str:
            dmg = dice.roll(wep.dice_num, wep.dice_dmg, divide_by=wep.divide_by, bonus=wep.dmg_bonus)
            break
        else:
            dmg = safeCastToInt(input)
            if dmg > 0:
                break
    location = determineHitLocation()
    printRedLine(f'{dmg} DMG to {location}')
    return dmg


def handleShotgunDmgAndHit(wep, attack_range):
    shotgun_max_dice = wep.dice_num
    shotgun_dmg = wep.dice_dmg
    dmg = 0
    hit_locations = []
    if wep.isCloseRange(attack_range):
        print('Damage is for 1m pattern')
        dmg = dice.roll(shotgun_max_dice, shotgun_dmg)
        location = determineHitLocation()
        hit_locations.append(location)
    elif wep.isMidRange(attack_range):
        print('Damage is for 2m pattern')
        dmg = dice.roll(shotgun_max_dice - 1, shotgun_dmg)
        hit1 = determineHitLocation()
        hit2 = determineHitLocation()

        hit_locations.append(hit1)
        hit_locations.append(hit2)
    elif wep.isLongRange(attack_range) or wep.isExtremeRange(attack_range):
        print('Damage is for 3m pattern')
        dmg = dice.roll(shotgun_max_dice - 2, shotgun_dmg)
        hit1 = determineHitLocation()
        hit2 = determineHitLocation()
        hit3 = determineHitLocation()
        hit_locations.append(hit1)
        hit_locations.append(hit2)
        hit_locations.append(hit3)

    hit_loc_data = determineHitLocDamages(dmg, hit_locations)
    locations_str = ', '.join(hit_loc_data)

    printRedLine(f'{locations_str}')

    return dmg


# | -- x ----- x --- |
def determineHitLocDamages(dmg, locations):
    dmg_left = dmg
    loc_data = []
    loc_size = len(locations)
    i = 0
    dmg_for_part = 0
    while i < loc_size:
        if i == loc_size - 1:
            dmg_for_part = dmg_left
        else:
            dmg_for_part = random.randint(0, dmg_left)
        dmg_left -= dmg_for_part
        loc_data.append(f'{dmg_for_part} DMG to {locations[i]}')
        i += 1
    return loc_data


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
            printGreenLine(f'{weapon.item} reloaded with {amount} shots')
        else:
            print(f"{weapon.item} is not a gun, can't reload it")


def hitCharacter(name, body_part, dmg_str, is_ap=False, pass_sp=False):
    dmg = safeCastToInt(dmg_str)
    character = DAO.getCharacterByName(name)
    if character is not None:
        if pass_sp == True:
            damageCharacter(character, dmg)
        elif body_parts.__contains__(body_part):
            if is_ap:
                handleApHit(character, dmg, body_part)
            else:
                handleNormalHit(character, dmg, body_part)
        else:
            valid_body_parts = ', '.join(body_parts)
            print(f'Invalid body part {body_part} [{valid_body_parts}]')


def handleNormalHit(character: Character, dmg, body_part):
    char_sp = character.sp[body_part]
    sp_left = 0
    if char_sp > 0:
        sp_left = char_sp - dmg
        if sp_left >= 0:
            printRedLine(f'Armor damaged at {body_part}')
            DAO.dmgCharacterSP(character.id, body_part, dmg)
        else:
            printRedLine(f'Armor broken at {body_part}')
            dmg_left = abs(sp_left)
            DAO.dmgCharacterSP(character.id, body_part, char_sp)
            damageCharacter(character, dmg_left)
    else:
        damageCharacter(character, dmg)


def handleApHit(character: Character, dmg, body_part):
    char_sp = character.sp[body_part]
    sp_left = math.ceil(char_sp / 2)
    dmg_done = math.floor((dmg - sp_left) / 2)
    DAO.dmgCharacterSP(character.id, body_part, dmg)
    damageCharacter(character, dmg_done)


def damageCharacter(c: Character, dmg):
    dmgReduction = c.bodyTypeModifier
    total_dmg = dmg - dmgReduction
    if total_dmg > 0:
        printRedLine(f'{c.name} damaged by {total_dmg}! (DMG reduced by {dmgReduction})')
        DAO.dmgCharacter(c.id, total_dmg)
        updated_character = DAO.getCharacterById(c.id)

        if updated_character.dmg_taken >= max_health:
            printRedLine(f'{c.name} has flatlined')
        else:
            stunCheck(updated_character.name)
    else:
        print('The hit did not damage target')


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
        printRedLine(f'penalty for {dmg_taken} DMG taken is {penalty}')
    save_against = body - penalty
    if (save_against > 0):
        print(f'To not be stunned/shocked (or to not lose death save), roll {save_against} or lower')
    else:
        printRedLine(f'Stun/shock saves cannot help anymore, character needs to be stabilized fast')

    return save_against



def stunCheck(name):
    c = DAO.getCharacterByName(name)
    if c is not None:
        save_against = stunCheckToBeat(c.dmg_taken, c.attributes['BODY'])
        roll = dice.roll(1, 10)
        isStunned = roll > save_against

        if isStunned:
            printRedLine(rollStunOverActingEffect(c.name))
        else:
            printGreenLine(f"{c.name} wasn't stunned!")
        print(f'[Save against = {save_against} vs roll = {roll}]')

        return isStunned
