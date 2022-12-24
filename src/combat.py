import dice
from character import Character
import bodytypes
from db import cyberdao as DAO
from src.gameHelper import stunPenalty, body_part_body, body_part_head, body_part_l_leg, body_part_r_arm, \
    body_part_l_arm, body_part_r_leg, safeCastToInt, max_health, askInput, REF, t_melee, t_handgun, t_rifle, t_shotgun, \
    t_thrown, roll_str


def characterAttack(name, range_str, given_roll):
    attack_range = safeCastToInt(range_str)
    if attack_range > 0:
        character = DAO.getCharacterByName(name)
        if character is not None:
            weapons = character.weapons
            print(f'Select weapon num: ')
            idx = 0
            for w in weapons:
                i = weapons.index(w)
                print(f'{i} - {w.item}')
            while True:
                input = askInput()
                idx = safeCastToInt(input)
                if 0 <= idx < len(weapons):
                    break
            wep = weapons[idx]
            wep_t = wep.weapon_type
            ref_bonus = character.attributes[REF]
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
                skill = 'athletics'
            skill_bonus = skillBonusForSkill(skills, skill)

            roll = safeCastToInt(given_roll)
            if roll <= 0:
                roll = dice.rollWithCrit()

            roll_to_beat = 10
            wep_range = wep.range
            range_str = ''
            point_blank_range_limit = 1
            close_limit = wep_range / 4
            mid_limit = wep_range / 2
            long_limit = wep_range
            extreme_limit = wep_range * 2
            if 0 < wep_range <= point_blank_range_limit:
                range_str = f'Point blank ({point_blank_range_limit}m)'
            elif 1 < wep_range <= close_limit:
                range_str = f'Close ({close_limit}m)'
                roll_to_beat = 15
            elif 1 < wep_range <= mid_limit:
                range_str = f'Medium ({mid_limit}m)'
                roll_to_beat = 20
            elif 1 < wep_range <= long_limit:
                range_str = f'Long ({long_limit}m)'
                roll_to_beat = 25
            elif 1 < wep_range <= extreme_limit:
                range_str = f'Extreme ({extreme_limit}m)'
                roll_to_beat = 30
            elif wep_range < extreme_limit:
                range_str = 'Impossible'
                roll_to_beat = 999999

            total = roll + ref_bonus + skill_bonus
            #TODO: add modifiers?
            hit_res = total >= roll_to_beat
            end_res = 'successful'
            dmg = 0
            if hit_res == False:
                end_res = 'unsuccessful'
            else:
                print(f'Attack successful!')
                print(f'{roll_str} or give dmg (> 0):')
                input = askInput()
                while True:
                    if input == roll_str:
                        dmg = dice.roll(wep.dice_num, wep.dice_dmg) + wep.dmg_bonus
                        break
                    else:
                        dmg = safeCastToInt(input)
                        if dmg > 0:
                            break
                print(f'DMG done: {dmg}')


            print(f'{character.name} selected {wep.item} [range = {wep_range}m] (roll = {roll} skill_lvl = {skill_bonus} ({skill}) REF bonus = {ref_bonus})')
            print(f'{range_str} range attack ({attack_range}m) is {end_res} [roll to beat ({roll_to_beat}) vs total ({total})]')

            print(f'')
    else:
        print(f'Range must be bigger than 0')

def skillBonusForSkill(skills, skill):
    skill_bonus = 0
    for s in skills:
        if s.skill == skill:
            skill_bonus = s.lvl
    return skill_bonus

def dmgReductionByBodyTypeModifier(bodyTypeModifier):
    reduction = bodytypes.bodyTypeModifiersDict[bodyTypeModifier]
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
    dmgReduction = dmgReductionByBodyTypeModifier(c.bodyTypeModifier)
    total_dmg = dmg - dmgReduction
    if total_dmg > 0:
        print(f'{c.name} damaged by {dmg}!')
        DAO.dmgCharacter(c.id, total_dmg)
        updated_character = DAO.getCharacterByName(c.name)
        if (updated_character.dmg_taken >= max_health):
            print(f'{c.name} has flatlined')
        else:
            stunCheck(updated_character)


def determineHitLocation():
    roll = dice.roll(1, 10)
    if roll == 1:
        return body_part_head
    elif 2 <= roll <= 4:
        return body_part_body
    elif roll == 5:
        return body_part_r_arm
    elif roll == 6:
        return body_part_l_arm
    elif 7 <= roll <= 8:
        return body_part_r_leg
    else:
        return body_part_l_leg


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

