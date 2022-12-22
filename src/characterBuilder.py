import dice
import cyberdao as DAO
import roles
import bodytypes
from gameHelper import askInput, checkRollCommand, checkListCommand, safeCastToInt, roll_str, list_str


def addAttribute(attribute: str) -> int:
    print(f'<give val> or {roll_str} attribute {attribute} [1-10]')
    atr = 0
    while True:
        ans = askInput()
        if checkRollCommand(ans):
            atr = dice.roll(1, 10)
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
    print(f'<give role> or {roll_str} random role. {list_str} to see info on roles')
    role = ''
    while True:
        ans = askInput()
        if checkListCommand(ans):
            print(*roles.allRoles, sep='\n')
        elif roles.allRoles.__contains__(ans):
            role = ans
            print(f'Selected {role}')
            break
        elif checkRollCommand(ans):
            role = rollRole()
            print(f'Rolled {role}')
            break
    return role


def addSpecial(role):
    specialAbility = roles.roleDict[role][roles.ability]
    specialDescr = roles.roleDict[role][roles.abilityDesc]
    skill = 0

    print(f'<give skill level> or {roll_str} random level for special ability {specialAbility} ({specialDescr})')
    while True:
        ans = askInput()
        if checkRollCommand(ans):
            skill = dice.roll(1, 10)
            print(f'Rolled {specialAbility} = {skill}')
            break
        else:
            res = safeCastToInt(ans)
            if 0 < res <= 10:
                skill = res
                print(f'Set {specialAbility} = {skill}')
                break
    return skill


def rollBodyType():
    body_type = ''
    roll = dice.roll(1, 6)
    if roll == 1:
        body_type = bodytypes.very_weak
    elif roll == 2:
        body_type == bodytypes.weak
    elif roll == 3:
        body_type = bodytypes.average
    elif roll == 4:
        body_type = bodytypes.strong
    elif roll == 5:
        body_type = bodytypes.very_strong
    else:  # superhuman only achievable by cybernetics
        body_type = rollBodyType()
    return body_type


def addBodyType():
    print(f'<give body type> or {roll_str} random body type ({list_str} to show all)')
    body_type = ''
    while True:
        ans = askInput()
        if checkListCommand(ans):
            bodytypes.listAvailableModifiers()
        elif checkRollCommand(ans):
            body_type = rollBodyType()
            break
        else:
            t_bod_type = bodytypes.checkBodyTypeFromStr(ans.lower())
            if t_bod_type is None:
                print(f'Invalid body type, see possible ones with {list_str}')
            elif t_bod_type == bodytypes.superhuman:
                print(print(f'Body type {bodytypes.superhuman} is only achievable through cybernetics'))
            else:
                body_type = t_bod_type
                break

    print(f'Body type modifier = {body_type}')
    return body_type


def createCharacter(name: str):
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
    if roll == 1:
        return roles.solo
    elif roll == 2:
        return roles.cop
    elif roll == 3:
        return roles.corp
    elif roll == 4:
        return roles.fixer
    elif roll == 5:
        return roles.nomad
    elif roll == 6:
        return roles.techie
    elif roll == 7:
        return roles.netrunner
    elif roll == 8:
        return roles.meditechie
    elif roll == 9:
        return roles.rocker
    else:
        return roles.media
