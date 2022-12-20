import dice
from character import Character
from math import floor

def dmgReductionByBodyTypeModifier(bodyTypeModifier):
    if bodyTypeModifier == 'very weak':
        return 0
    elif bodyTypeModifier == 'weak':
        return 1
    elif bodyTypeModifier == 'average':
        return 2
    elif bodyTypeModifier == 'strong':
        return 3
    elif bodyTypeModifier == 'very strong':
        return 4
    else:
        return 5

def damageCharacter(c: Character, dmg):
    dmgReduction = dmgReductionByBodyTypeModifier(c.bodyTypeModifier)
    totalDmg = dmg - dmgReduction
    if (totalDmg < 0):
        totalDmg = 0
    c.takeDmg(totalDmg)
    stunCheck(c)

def stunPenalty(dmg: int):
    return floor(dmg / 4)

def determineHitLocation():
    roll = dice.roll(1, 10)
    if roll == 1:
        return 'head'
    elif 2 <= roll <= 4:
        return 'body'
    elif roll == 5:
        return 'r. arm'
    elif roll == 6:
        return 'l. arm'
    elif 7 <= roll <= 8:
        return 'r. leg'
    else:
        return 'l. leg'

def woundState(dmg_taken: int):
    stun_penalty = stunPenalty(dmg_taken)
    if dmg_taken == 0:
        return 'At least physically healthy!'
    elif stun_penalty == 0:
        return 'Just a scratch'
    elif stun_penalty == 1:
        return 'Bleeding a bit'
    elif stun_penalty == 2:
        return 'Very nasty wound'
    elif dmg_taken <= 40:
        return 'Start rolling those death saves..'
    else:
        return 'Flatlined.'

def rollStunOverActingEffect():
    roll = dice.roll(1, 6)
    if roll == 1:
        return 'Screams, windmills arms, falls'
    elif roll == 2:
        return 'Crumples like a rag doll'
    elif roll == 3:
        return 'Spins around in place, falls'
    elif roll == 4:
        return 'Clutches wound, staggers and falls'
    elif roll == 5:
        return 'Stares stupidly at wound, then falls'
    else:
        return 'Slumps into ground, moaning'

def stunCheckToBeat(dmg_taken, body):
    penalty = stunPenalty(dmg_taken)
    print(f'penalty for {dmg_taken} dmg is {penalty}')
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
        print(rollStunOverActingEffect())
    return isStunned

