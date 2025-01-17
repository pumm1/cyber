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
from logger import Log, log_neg, log_pos, log_neutral, log_event
from weapon import Weapon, manualWeaponFromReq
from colorama import Fore, Style


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


def suppressiveFireDef(name, rounds, area):
    shots_in_area = safeCastToInt(rounds)
    area_width = safeCastToInt(area)
    if shots_in_area > 0 and area_width > 0:
        character = DAO.getCharacterByName(name)
        if character is not None:
            (roll, _) = dice.rollWithCrit()
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


def weapon_info(wep):
    if wep.effect_radius > 0:
        print(
            f'Hit affects radius of {wep.effect_radius} - Check also if hit misses or if there are other targets in the radius!'
        )
    if wep.weapon_type == t_shotgun:
        print(
            """For shotguns, point blank/short range attack is for one spot, mid range hits 2 spots and long/extreme hits 3 places."""
        )


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
                    roll=given_roll,
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
        (roll, _) = dice.rollWithCrit(skip_luck=True)
    total = roll + ref_bonus + skill_bonus + modifiers_total
    logs = log_event(logs, f'{character.name} attacks with {wep.item} (Roll total = {total})', log_pos)
    logs = log_event(logs, "Defend against melee attack by rolling opponent's dodge skill", log_neg)
    logs = log_event(logs,
                     f'If attack is successful, calculate damage for roll (or automatically roll dmg) with {melee_dmg_help_str}',
                     log_neutral)
    logs = log_event(logs,
                     f'(dice roll = {roll}, REF bonus = {ref_bonus}, skill_bonus = {skill_bonus} ({skill}), modifiers = {modifiers_total})',
                     log_neutral)

    return logs


def handleMeleeDmg(character, roll, wep_id=None, method=None) -> list[Log]:
    logs = []
    dmg_roll = safeCastToInt(roll)
    if character is not None:
        dmg_bonus = bodytypes.meleeDmgBonusByModifier(character.bodyTypeModifier)
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


def handleMeleeDmgByCharacterId(character_id, roll, wep_id, method=None):
    character = DAO.getCharacterById(character_id)
    return handleMeleeDmg(character, roll, wep_id, method)


def handleMeleeDmgByCharacterName(name, roll, method=None):
    character = DAO.getCharacterByName(name)
    return handleMeleeDmg(character, roll, method)


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


def handleFullAuto(character, wep, skill_bonus, skill, attack_range=0, num_of_targets=0, num_of_shots=0, roll=0,
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
        if roll <= 0:
            roll = dice.resolveAutoOrManualRollWithCrit(auto_roll=auto_roll, skip_luck=skip_luck)
        roll_total = roll + ref_bonus + skill_bonus + modifiers_total + wep.wa
        full_auto_logs = fullAutoRoll(roll_total, wep, skill, skill_bonus, roll, ref_bonus, attack_range,
                                      num_of_targets, num_of_shots, modifiers_total, auto_roll, skip_luck)
        logs = logs + full_auto_logs

        DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)
    else:
        logs = log_event(logs, f"Can't attack with {wep.item} [{wep.shots_left} / {wep.clip_size}]", log_neg)

    return logs


def weaponToolResultFromReq(roll_total, weapon_type, wa, attack_range, num_of_targets=1, num_of_shots=1):
    logs = []
    wep = manualWeaponFromReq(weapon_type=weapon_type, rof=50, wa=wa, clip_size=50, shots_left=50, custom_range=None)

    if num_of_shots == 3:
        logs = burstRoll(roll_total, attack_range=attack_range, shots_fired=3, shots_left=50, wep=wep,
                         skill='<manual check>', roll=0, auto_roll=True)
    elif num_of_shots > 3:
        logs = fullAutoRoll(roll_total, wep, '<manual check>', roll=roll_total,
                            attack_range=attack_range, num_of_targets=num_of_targets, num_of_shots=num_of_shots,
                            modifiers_total=0, auto_roll=True, skip_luck=True)
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


# TODO: think about some balancing changes?
def fullAutoRoll(roll_total, wep, skill, skill_bonus=0, roll=0, ref_bonus=0, attack_range=0, num_of_targets=0,
                 num_of_shots=0, modifiers_total=None, auto_roll=False, skip_luck=False) -> list[Log]:
    logs = []
    total_hits = 0
    targets_hit = 0
    roll_total = roll_total + wep.wa
    range_bonus = math.ceil(num_of_shots / 10)
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
        (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
        if not (r == close_range_str or r == point_blank_range_str):
            range_bonus = -1 * range_bonus
        # last minus is balancing test. more targts = more sway in aiming
        sway_balance = 3 * target_num
        range_penalty = math.floor(num_of_shots / 10)
        roll_total = roll_total - sway_balance - range_penalty + range_bonus
        num_of_hits = 0
        logs = log_event(
            logs,
            f'{rollToBeatStr(roll_to_beat, roll_total)} '
            f'[roll = {roll}, REF bonus = {ref_bonus}, skill_bonus = {skill_bonus} ({skill}), range bonus = {range_bonus}, WA = {wep.wa}, range_penalty={range_penalty}, target sway_balance = {sway_balance}]',
            log_neutral
        )

        if roll_total >= roll_to_beat:
            targets_hit = targets_hit + 1
            num_of_hits = roll_total - roll_to_beat
            if num_of_hits >= shots_per_target:
                num_of_hits = shots_per_target
            if num_of_hits <= 0:
                num_of_hits = 1

            total_hits = total_hits + num_of_hits

            logs = log_event(logs, f'Target {t} hit {num_of_hits} times!', log_pos)

            for i in range(num_of_hits):
                (dmg, dmg_logs) = hitDmg(wep, attack_range, auto_roll=auto_roll)
                logs = possiblyWarnAboutLimbDestroyed(dmg, logs)
                logs = logs + dmg_logs
                target_total_dmg = target_total_dmg + dmg
            logs = log_event(logs,
                             f'Total dmg done to target [{t}]: {target_total_dmg} [{num_of_hits}x {dmg_info(wep)}]',
                             log_pos)
            logs = log_event(logs,
                             f'{num_of_shots} shots fired in full auto with {wep.item} hitting {total_hits} times',
                             log_neutral)

        else:
            logs = log_event(logs, f'Full auto missed target {t}!', log_neg)
    return logs


def burstRoll(roll_total, attack_range, shots_fired, shots_left, wep, skill, roll, skill_bonus=0, ref_bonus=0,
              auto_roll=False) -> [Log]:
    logs = []
    (roll_to_beat, range_str, r) = wep.rollToBeatAndRangeStr(attack_range)
    roll_total = roll_total + wep.wa
    if roll_total >= roll_to_beat:
        hits = 1
        if roll_total - roll_to_beat > 4:
            hits = 3
        elif roll_total - roll_to_beat > 2:
            hits = 2

        if shots_fired < 3 and hits == 3:
            hits = shots_left
        total_dmg = 0
        logs = log_event(logs, f'{hits} hits to target!', log_pos)
        attack_info_str = f"""
    Character selected {wep.item} for BURST fire [weapon range = {wep.range}m]
    (total = {roll_total} vs roll to beat {roll_to_beat} - roll = {roll} skill_lvl = {skill_bonus} ({skill}) REF bonus = {ref_bonus} WA = {wep.wa})
                    """
        logs = log_event(logs, attack_info_str, log_neutral)
        for i in range(hits):
            (dmg, hitLogs) = hitDmg(wep, attack_range, auto_roll=auto_roll)
            logs = logs + hitLogs
            total_dmg = total_dmg + dmg
        logs = log_event(logs, f'Total dmg done to target: {total_dmg} [{hits}x {dmg_info(wep)}]', log_pos)
    else:
        logs = log_event(logs, f'Burst attack misses target!', log_neg)
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


def handleBurst(character, wep, attack_range, given_roll, skill_bonus, skill, modifiers_total, skip_luck=False,
                auto_roll=False) -> [Log]:
    logs = []
    if modifiers_total < 0 or modifiers_total is None:
        modifiers_total = modifiersForTarget(1)
    logs = log_event(logs, f'Trying burst attack with {wep.item}', log_neutral)
    roll = safeCastToInt(given_roll)
    if roll <= 0:
        (roll, added_logs) = dice.rollWithCrit(skip_luck)
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
        range_bonus = 0
        if r == close_range_str or r == medium_range_str:
            range_bonus = 3

        shots_fired = 3
        if shots_left < 3:
            shots_fired = shots_left
        shots_left_after_firing = wep.shots_left - shots_fired

        total = roll + ref_bonus + skill_bonus + range_bonus + modifiers_total + wep.wa
        burst_logs = burstRoll(roll_total=total, attack_range=attack_range, shots_fired=shots_fired,
                               shots_left=shots_left,
                               wep=wep, skill=skill, roll=roll, skill_bonus=skill_bonus, ref_bonus=ref_bonus,
                               auto_roll=auto_roll)
        logs = logs + burst_logs
        DAO.updateShotsInClip(wep.weapon_id, shots_left_after_firing)
    else:
        logs = log_event(logs,
                         f"Unable to do burst attack with {wep.item} ({wep.weapon_type}) [{wep.shots_left} / {wep.clip_size}] ROF: {wep.rof}",
                         log_neg)

    return logs


def handleSingleShot(character, wep, attack_range, given_roll, skill_bonus, skill, modifiers_total, targets=1,
                     skip_luck=False, auto_roll=False):
    if modifiers_total is None:
        modifiers_total = modifiersForTarget(1)
    roll = safeCastToInt(given_roll)
    logs = []
    if roll <= 0:
        (roll, added_logs) = dice.rollWithCrit(skip_luck)
        logs = logs + added_logs
    shots_left = wep.shots_left
    weapon_can_attack = True
    if wep.isGun():
        if shots_left <= 0:
            weapon_can_attack = False

    (roll_to_beat, range_str, _) = wep.rollToBeatAndRangeStr(attack_range)

    ref_bonus = character.attributes[REF]
    total = roll + ref_bonus + skill_bonus + modifiers_total + wep.wa
    hit_res = roll > 1 and total >= roll_to_beat
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

        attack_info_str = f'{character.name} selected {wep.item} [weapon range = {wep.range}m] (TOTAL = {total}, roll = {roll}, skill_lvl = {skill_bonus} ({skill}), REF bonus = {ref_bonus}, WA = {wep.wa})'
        logs = log_event(logs, attack_info_str, log_neutral)

        range_info_str = f'{range_str} range attack ({attack_range}m) is {end_res} {rollToBeatStr(roll_to_beat, total)}'
        logs = log_event(logs, range_info_str, log_neutral)
    else:
        unable_str = f'Unable to attack with (id: {wep.weapon_id}) {wep.item} [Shots left: {wep.shots_left} / {wep.clip_size}]'
        logs = log_event(logs, unable_str, log_neg)

    return logs


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


def hitCharacterById(id, body_part, dmg_str, is_ap=False, pass_sp=False):
    character = DAO.getCharacterById(id)
    return hitCharacter(character, body_part, dmg_str, is_ap, pass_sp)


def hitCharacterByName(name, body_part, dmg_str, is_ap=False, pass_sp=False):
    character = DAO.getCharacterByName(name)
    return hitCharacter(character, body_part, dmg_str, is_ap, pass_sp)


def handleNormalHit(character: Character, dmg, body_part) -> list[Log]:
    logs = []
    char_sp = character.sp[body_part]
    dmg_passing_sp = 0
    if char_sp > 0:
        dmg_passing_sp = char_sp - dmg
        if dmg_passing_sp < 0:
            passed_dmg = abs(dmg_passing_sp)
            logs = log_event(logs, f'Armor damaged at {body_part} and {passed_dmg} DMG done to {character.name}',
                             log_neg)
            DAO.dmgCharacterSP(character.id, body_part)
            damageCharacter(character, passed_dmg, body_part)
        else:
            logs = log_event(logs, f"{character.name}'s armor absorbed the hit", log_neutral)
    else:
        logs = log_event(logs, f'{character.name} has no armor left at {body_part}', log_neutral)
        dmg_logs = damageCharacter(character, dmg, body_part)
        logs = logs + dmg_logs
    return logs


def handleApHit(character: Character, dmg, body_part, logs) -> list[Log]:
    char_sp = character.sp[body_part]
    sp_left = math.floor(char_sp / 2)
    dmg_done = math.ceil((dmg - sp_left) / 2)
    log_type = log_pos
    if dmg_done > 0:
        log_type = log_neg
    else:
        dmg_done = 0
    logs = log_event(logs, f'{dmg_done} DMG done with AP shot [original dmg = {dmg}]', log_type)
    if dmg_done > 0:
        if char_sp > 0:
            DAO.dmgCharacterSP(character.id, body_part)
        logs = damageCharacter(character, dmg_done, body_part, logs=logs)
    return logs


def damageCharacter(c: Character, dmg, body_part, logs: list[Log] = []) -> list[Log]:
    dmgReduction = c.bodyTypeModifier
    total_dmg = dmg - dmgReduction
    if total_dmg > 0:
        logs = log_event(logs, f'{c.name} damaged by {total_dmg}! (DMG reduced by {dmgReduction})', log_neg)
        DAO.dmgCharacter(c.id, total_dmg)
        updated_character = DAO.getCharacterById(c.id)
        if total_dmg >= 8:
            logs = log_event(logs, f"Body part hit ({body_part}) is badly damaged/destroyed!", log_neg)

        if updated_character.dmg_taken >= max_health:
            logs = log_event(logs, f'{c.name} has flatlined', log_neg)
        else:
            logs = logs + stunCheckById(updated_character.id)
    else:
        logs = log_event(logs, f'The hit did not damage target (DMG = {dmg}, DMG reduced by = {dmgReduction})',
                         log_neutral)

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
    roll = dice.roll(1, 10)
    is_stunned = roll > save_against

    if is_stunned:
        logs = log_event(logs, f'{c.name} fails stun check!', log_neg)
        logs = log_event(logs, rollStunOverActingEffect(c.name), log_neg)
    else:
        logs = log_event(logs, f"{c.name} wasn't stunned!", log_pos)
    logs = log_event(logs, f'[Stun save against = {save_against} > roll = {roll}]', log_neutral)
    return logs


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
