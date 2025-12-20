import math
import random

import src.dice as dice
from src.character import Character
import src.bodytypes as bodytypes
from src.gameHelper import stunPenalty, body_part_body, body_part_head, body_part_l_leg, body_part_r_arm, \
    body_part_l_arm, body_part_r_leg, safeCastToInt, max_health, askInput, REF, t_melee, t_handgun, t_rifle, t_shotgun, \
    t_thrown, roll_str, close_range_str, medium_range_str, attack_type_single, attack_type_burst, \
    attack_type_full_auto, point_blank_range_str, attack_type_melee, unarmed, melee_dmg_help_str, body_parts, \
    t_heavy_weapon, printColorLine, printRedLine, printGreenLine, coloredText, t_smg, BODY
from src.skills import skillBonusForSkill, skill_athletics
from src.logger import Log, log_neg, log_pos, log_neutral, log_event
from src.weapon import Weapon, manualWeaponFromReq


def weaponsByAttackType(attack_type, weapons):
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


def weaponByAttackTypeAndWeaponId(character, weapon_id, attack_type):
    weapons = weaponsByAttackType(attack_type, character.weapons)
    weapon = None
    for w in weapons:
        if w.weapon_id == weapon_id:
            weapon = w
            break
    if weapon is None:
        printRedLine(f'No weapons found for {attack_type}, character_id = {character.id}, weapon_id = {weapon_id}')

    return weapon


def weaponByAttackType(attack_type, character, wep_id=None):
    weapons = weaponsByAttackType(attack_type, character.weapons)
    if len(weapons) > 0:
        if wep_id is None:
            idx = 0
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
            wep = None
            for w in weapons:
                if w.weapon_id == wep_id:
                    wep = w
            return wep
    else:
        printRedLine(f'No weapons found for {attack_type}')
        return None


def weapon_info(wep):
    if wep.effect_radius > 0:
        print(
            f'Hit affects radius of {wep.effect_radius} - Check also if hit misses or if there are other targets in the radius!'
        )
    if wep.weapon_type == t_shotgun:
        print(
            """For shotguns, point blank/short range attack is for one spot, mid range hits 2 spots and long/extreme hits 3 places."""
        )


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


def handleMelee(character, wep, given_roll, skill_bonus, skill, modifiers_total):
    logs = []
    if modifiers_total is None:
        modifiers_total = modifiersForTarget(1)
    ref_bonus = character.attributes[REF]
    # TODO: specify judo etc
    # if wep.item == unarmed:
    # print('Give skill for bonus (e.g. brawling, karate, judo...)')
    # skill = askInput()
    # skill_bonus = skillBonusForSkill(character.skills, skill)
    t_roll = safeCastToInt(given_roll)
    roll = 0
    if t_roll > 0:
        roll = t_roll
    else:
        (roll_res, _) = dice.rollWithCrit(skip_luck=True)
    total = roll_res + ref_bonus + skill_bonus + modifiers_total
    logs = log_event(logs, f'{character.name} attacks with {wep.item} (Roll total = {total})', log_pos)
    logs = log_event(logs, "Defend against melee attack by rolling opponent's dodge skill", log_neg)
    logs = log_event(logs,
                     f'If attack is successful, calculate damage for roll (or automatically roll dmg) with {melee_dmg_help_str}',
                     log_neutral)
    logs = log_event(logs,
                     f'(dice roll = {roll_res}, REF bonus = {ref_bonus}, skill_bonus = {skill_bonus} ({skill}), modifiers = {modifiers_total})',
                     log_neutral)

    return logs


def handleMeleeDmg(character, roll, wep_id=None, method=None) -> list[Log]:
    logs = []
    dmg_roll = safeCastToInt(roll)
    if character is not None:
        dmg_bonus = bodytypes.meleeDmgBonusByBodyType(character.attributes[BODY])
        different_melee_attacks = ', '.join(melee_attacks)
        dmg = 0
        while True:
            if method is None:
                print(f'Give attack method ({different_melee_attacks}):')
                method = askInput()
            match method:
                case 'weapon':
                    wep = weaponByAttackType(attack_type_melee, character, wep_id)
                    if wep is not None:
                        if dmg_roll == 0:
                            dmg_roll = dice.roll(wep.dice_num, wep.dice_dmg, divide_by=wep.divide_by,
                                                 bonus=wep.dmg_bonus)
                        dmg = dmg_roll + dmg_bonus
                        method = wep.item
                        break
                    else:
                        logs = log_event(logs, f'Weapon not found', log_neg)
                        break
                case 'strike':
                    if dmg_roll == 0:
                        dmg_roll = dice.roll(1, 6, divide_by=2)
                    dmg = dmg_roll + dmg_bonus
                    break
                case 'kick':
                    if dmg_roll == 0:
                        dmg_roll = dice.roll(1, 6)
                    dmg = dmg_roll + dmg_bonus
                    break
                case 'throw':
                    if dmg_roll == 0:
                        dmg_roll = dice.roll(1, 6)
                    dmg = dmg_roll + dmg_bonus
                    break
                case 'choke':
                    if dmg_roll == 0:
                        dmg_roll = dice.roll(1, 6)
                    dmg = dmg_roll
                    break
        hit_loc = determineHitLocation()
        logs, head_is_hit = handleHitLocationInfoForLogs(hit_loc, logs)
        if dmg < 0:
            dmg = 0
        if head_is_hit:
            dmg = dmg * 2
        logs = log_event(
            logs,
            f'{character.name} did {dmg} DMG to {hit_loc} using {method} [dmg roll = {dmg_roll}, dmg_bonus = {dmg_bonus}]',
            log_neutral
        )
    else:
        logs = log_event(logs, f'Character not found for melee dmg', log_neg)
    return logs


def handleHitLocationInfoForLogs(hit_loc: str, logs: list[Log]) -> (list[Log], bool):
    head_is_hit = False
    if hit_loc == body_part_head:
        head_is_hit = True
        logs = log_event(logs, 'Hit to head doubles damage!', log_neg)
    return logs, head_is_hit


def resolveDmgPassingSP(char_sp: int, dmg: int) -> (int, bool):
    dmg_to_sp = char_sp - dmg
    dmg_to_character = 0
    armor_damaged = False
    if dmg_to_sp < 0:
        dmg_to_character = abs(dmg_to_sp)
        armor_damaged = True

    return dmg_to_character, armor_damaged


#bodyTypeModifier = dmgReduction
def resolveDmgDoneToCharacter(dmg: int, bodyTypeModifier: int) -> (int, bool):
    total_dmg = dmg - bodyTypeModifier
    if total_dmg < 0:
        total_dmg = 0
    body_part_destroyed = False

    if total_dmg >= 8:
        body_part_destroyed = True

    return total_dmg, body_part_destroyed


#AP halves damage passing the calculated SP
def resolveApDmg(char_sp: int, dmg: int):
    sp_left = math.floor(char_sp / 2)
    dmg_done = math.ceil((dmg - sp_left) / 2)
    if dmg_done < 0:
        dmg_done = 0

    return dmg_done


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


def weaponToolResultFromReq(roll_total, weapon_type, wa, attack_range, num_of_targets=1, num_of_shots=1):
    logs = []
    wep = manualWeaponFromReq(weapon_type=weapon_type, rof=50, wa=wa, clip_size=50, shots_left=50, custom_range=None)

    if num_of_shots == 3:
        logs = burstRoll(roll_total=roll_total, roll_res=roll_total, attack_range=attack_range, wep=wep,
                         skill='<manual check>', auto_roll=True, skip_dmg_logs=True)
    elif num_of_shots > 3:
        logs = fullAutoRoll(roll_total, wep, skill='<manual check>',
                            attack_range=attack_range, num_of_targets=num_of_targets, num_of_shots=num_of_shots,
                            modifiers_total=0, auto_roll=True, skip_luck=True, skip_dmg_logs=True)
    else:
        (roll_to_beat, range_str, _) = wep.rollToBeatAndRangeStr(attack_range)
        info_str = f'[Roll to beat = {roll_to_beat}, range = {range_str}]'
        if roll_total >= roll_to_beat:
            logs = log_event(logs, "Hit!", log_pos)
            if wep.weapon_type == t_shotgun:
                hits, dice_num, logs = resolveShotgunHitsAndDmgDiceByRange(wep, attack_range, logs)
                logs = log_event(logs,
                                 f'Roll damage for {hits} spots for each target in spread area with {dice_num}D{wep.dice_dmg}',
                                 log_pos)
        else:
            logs = log_event(logs, "Miss!", log_neg)
        logs = log_event(logs, info_str, log_neutral)
    return logs


def resolveFullAutoRangeBonus(num_of_shots: int, range_name: str):
    range_bonus_for_num_of_shots = math.floor(num_of_shots / 10)
    if not (range_name == close_range_str or range_name == point_blank_range_str):
        range_bonus_for_num_of_shots = -1 * range_bonus_for_num_of_shots

    return range_bonus_for_num_of_shots

def resolveFullAutoTargetHits(roll_total: int, roll_to_beat: int, shots_per_target) -> (bool, int):
    target_hit = False
    num_of_hits = 0
    if roll_total >= roll_to_beat:
        target_hit = True
        num_of_hits = roll_total - roll_to_beat
        if num_of_hits >= shots_per_target:
            num_of_hits = shots_per_target
        if num_of_hits <= 0:
            num_of_hits = 1

    return target_hit, num_of_hits

# TODO: think about some balancing changes?
def fullAutoRoll(roll_total, wep, skill, skill_bonus=0, roll_res=0, ref_bonus=0, attack_range=0, num_of_targets=0,
                 num_of_shots=0, modifiers_total=None, auto_roll=False, skip_luck=False, skip_dmg_logs=False) -> list[
    Log]:
    logs = []
    total_hits = 0
    targets_hit = 0
    roll_total = roll_total + wep.wa

    (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
    range_bonus_for_num_of_shots = resolveFullAutoRangeBonus(num_of_shots, r)

    shots_per_target = math.floor(num_of_shots / num_of_targets)
    for target_num in range(num_of_targets):
        t = target_num + 1
        logs = log_event(logs, f'Rolling attack for target {t} / {num_of_targets}', log_neutral)
        if attack_range <= 0:
            print(f'Give range for target {t}:')
            while True:
                i = askInput()
                attack_range = safeCastToInt(i)
                if attack_range > 0:
                    break

        if modifiers_total is None:
            modifiers_total = modifiersForTarget(t)
        target_total_dmg = 0
        # last minus is balancing test. more targts = more sway in aiming
        roll_total = roll_total + range_bonus_for_num_of_shots
        num_of_hits = 0
        logs = log_event(
            logs,
            f'{rollToBeatStr(roll_to_beat, roll_total)} '
            f'[roll = {roll_res}, REF bonus = {ref_bonus}, skill_bonus = {skill_bonus} ({skill}), range bonus = {range_bonus_for_num_of_shots}, WA = {wep.wa}]',
            log_neutral
        )

        target_hit, num_of_hits = resolveFullAutoTargetHits(roll_total, roll_to_beat, shots_per_target)
        if target_hit:
            total_hits = total_hits + num_of_hits

            logs = log_event(logs, f'Target {t} hit {num_of_hits} times!', log_pos)

            if not skip_dmg_logs:
                for i in range(num_of_hits):
                    (dmg, dmg_logs) = hitDmg(wep, attack_range, auto_roll=auto_roll)
                    logs = possiblyWarnAboutLimbDestroyed(dmg, logs)
                    logs = logs + dmg_logs
                    target_total_dmg = target_total_dmg + dmg
                    logs = log_event(logs,
                                     f'Total dmg done to target [{t}]: {target_total_dmg} [{num_of_hits}x {dmg_info(wep)}]',
                                     log_pos)
            logs = log_event(logs,f'{num_of_shots} shots fired in full auto with {wep.item} hitting {total_hits} times',log_neutral)

        else:
            logs = log_event(logs, f'Full auto missed target {t}!', log_neg)
    return logs


def burstRoll(roll_total, attack_range, wep, skill, roll_res, skill_bonus=0, ref_bonus=0,
              auto_roll=False, skip_dmg_logs=False) -> [Log]:
    logs = []
    (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
    roll_total = roll_total + wep.wa
    hits = 0
    range_bonus = 0
    if r == close_range_str or r == medium_range_str:
        range_bonus = 3
    roll_total = roll_total + range_bonus
    if roll_total >= roll_to_beat:
        total_dmg = 0
        if not skip_dmg_logs:
            hits = dice.roll(1, 6, 2)
            logs = log_event(logs, f'{hits} hits to target!', log_pos)
        else:
            logs = log_event(logs, f'Roll number of hits with 1D6 / 2', log_pos)
        if not skip_dmg_logs:
            for i in range(hits):
                (dmg, hitLogs) = hitDmg(wep, attack_range, auto_roll=auto_roll)
                logs = logs + hitLogs
                total_dmg = total_dmg + dmg
            logs = log_event(logs, f'Total dmg done to target: {total_dmg} [{hits}x {dmg_info(wep)}]', log_pos)
    else:
        logs = log_event(logs, f'Burst attack misses target!', log_neg)

    attack_info_str = f"""
            Character selected {wep.item} for BURST fire [weapon max range = {wep.range}m]
            (total = {roll_total} vs roll to beat {roll_to_beat} [{range_str}] | roll = {roll_res} skill_lvl = {skill_bonus} range_bonus={range_bonus} ({skill}) REF bonus = {ref_bonus} WA = {wep.wa})
                        """
    logs = log_event(logs, attack_info_str, log_neutral)
    return logs


def rollToBeatStr(to_beat, total):
    return f'[roll to beat ({to_beat}) vs total ({total})]'


def dmg_info(wep):
    dmg_bonus_str = ''
    if wep.dmg_bonus != 0:
        if wep.dmg_bonus < 0:
            dmg_bonus_str = f'{wep.dmg_bonus}'
        else:
            dmg_bonus_str = f'+{wep.dmg_bonus}'
    return f'[{wep.dice_num}D{wep.dice_dmg}{dmg_bonus_str}]'


def hitDmg(wep, attack_range, targets=1, auto_roll=False) -> (int, list[Log]):
    log_events = []
    dmg = 0
    # TODO for REST
    if wep.weapon_type == t_shotgun:
        if targets is None or targets <= 0:
            while True:
                input = askInput()
                targets = safeCastToInt(input)
                if targets > 0:
                    break
        log_events = log_event(log_events,
                               f'{targets} targets in shotgun spread area (At least main target is hit, others have 50/50 a chance of not being hit)',
                               log_neutral)

        for target in range(targets):
            t_dmg = 0
            print(f'Target {target + 1}:')
            if target > 1:
                hit = dice.roll(1, 2)
                if hit > 1:
                    (t_dmg, logs) = handleShotgunDmgAndHit(wep, attack_range, log_events)
            else:
                (t_dmg, logs) = handleShotgunDmgAndHit(wep, attack_range, log_events)

            dmg += t_dmg

    else:
        (dmg, hitDmgLogs) = handleWeaponDmgAndHit(wep, auto_roll)
        log_events = log_events + hitDmgLogs

    return dmg, log_events


def handleWeaponDmgAndHit(wep, auto_roll) -> (int, list[Log]):
    dmg = 0
    while True:
        input = ''
        if auto_roll:
            input = roll_str
        else:
            print(f'{roll_str} or give dmg (> 0):')
            input = askInput()

        if input == roll_str:
            dmg = dice.roll(wep.dice_num, wep.dice_dmg, divide_by=wep.divide_by, bonus=wep.dmg_bonus)
            break
        else:
            dmg = safeCastToInt(input)
            if dmg > 0:
                break
    location = determineHitLocation()
    logs, head_is_hit = handleHitLocationInfoForLogs(location, [])
    if head_is_hit:
        dmg = dmg * 2
    logs = log_event(logs, f'{dmg} DMG to {location}', log_neg)
    logs = possiblyWarnAboutLimbDestroyed(dmg, logs)

    return dmg, logs


def resolveShotgunHitsAndDmgDiceByRange(wep, attack_range, logs: list[Log]):
    hits = 1
    dice_num = wep.dice_num

    if wep.isCloseRange(attack_range):
        logs = log_event(logs, f'Close range shotgun attack with full damage to single spot!', log_pos)
    elif wep.isMidRange(attack_range):
        hits = 2
        dice_num -= 1
        logs = log_event(logs, f'Middle range shotgun attack with lessened damage but 2 spots hit (1m spread)', log_pos)
    elif wep.isLongRange(attack_range):
        hits = 3
        dice_num -= 2
        logs = log_event(logs, f'Long range shotgun attack with Half damage but 3 spots hit (2m spread)', log_pos)
    elif wep.isExtremeRange(attack_range):
        hits = 4
        dice_num -= 3
        logs = log_event(logs, f'Extreme range shotgun attack with minimum damage but 4 spots hit (3m spread)', log_pos)

    return hits, dice_num, logs


def possiblyWarnAboutLimbDestroyed(dmg, logs: list[Log]):
    if dmg >= 8:
        logs = log_event(logs, f'If armor passing damage is greater than 8, then the hit limb is destroyed!',
                         log_neg)

    return logs


def handleShotgunDmgAndHit(wep, attack_range, logs: list[Log]):
    shotgun_dmg = wep.dice_dmg
    dmg = 0
    hit_locations = []
    hits, dmg_dice, logs = resolveShotgunHitsAndDmgDiceByRange(wep, attack_range, logs)
    for hit in range(hits):
        dmg = dice.roll(dmg_dice, shotgun_dmg)
        hit = determineHitLocation()
        hit_locations.append(hit)

    logs = possiblyWarnAboutLimbDestroyed(dmg, logs)
    logs = determineHitLocDamages(dmg, hit_locations, logs)

    return dmg, logs


# | -- x ----- x --- |
def determineHitLocDamages(dmg, locations, logs: list[Log]):
    dmg_left = dmg
    loc_size = len(locations)
    i = 0
    dmg_for_part = 0
    while i < loc_size:
        if i == loc_size - 1:
            dmg_for_part = dmg_left
        else:
            dmg_for_part = random.randint(0, dmg_left)
        dmg_left -= dmg_for_part
        logs = possiblyWarnAboutLimbDestroyed(dmg_for_part, logs)
        logs, head_is_hit = handleHitLocationInfoForLogs(locations[i], logs)
        if head_is_hit:
            dmg_for_part = dmg_for_part * 2
        logs = log_event(logs, f'{dmg_for_part} DMG to {locations[i]}', log_neg)
        i += 1

    return logs


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


def stunCheckToBeat(dmg_taken, body) -> (int, list[Log]):
    logs = []
    penalty = stunPenalty(dmg_taken)
    if penalty > 0:
        logs = log_event(logs, f'penalty for {dmg_taken} DMG taken is {penalty}', log_neg)
    save_against = body - penalty
    if (save_against > 0):
        logs = log_event(logs, f'To not be stunned/shocked (or to not lose death save), roll {save_against} or lower',
                         log_neutral)
    else:
        logs = log_event(logs, f'Stun/shock saves cannot help anymore, character needs to be stabilized fast', log_neg)

    return (save_against, logs)


def stunCheck(c: Character) -> list[Log]:
    logs = []
    (save_against, stun_logs) = stunCheckToBeat(c.dmg_taken, c.attributes['BODY'])
    logs = logs + stun_logs
    roll_res = dice.roll(1, 10)
    is_stunned = roll_res > save_against

    if is_stunned:
        logs = log_event(logs, f'{c.name} fails stun check!', log_neg)
        logs = log_event(logs, rollStunOverActingEffect(c.name), log_neg)
    else:
        logs = log_event(logs, f"{c.name} wasn't stunned!", log_pos)
    logs = log_event(logs, f'[Stun save against = {save_against} > roll = {roll_res}]', log_neutral)
    return logs
