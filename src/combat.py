import dice
from character import Character
import bodytypes
from db import cyberdao as DAO
from src.gameHelper import stunPenalty, body_part_body, body_part_head, body_part_l_leg, body_part_r_arm, \
    body_part_l_arm, body_part_r_leg, safeCastToInt


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
        stunCheck(c)


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

