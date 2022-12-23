import dice
import cyberdao as DAO
import roles
import bodytypes
from gameHelper import askInput, checkRollCommand, checkListCommand, safeCastToInt, roll_str, list_str, INT, REF, TECH, COOL, ATTR, LUCK, MA, BODY, EMP

def rollAtr():
    atr = dice.roll(2, 3) + 4
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
    print(f'<give role> or {roll_str} random role. {list_str} to see info on roles')
    role = manualRole(allow_roll=True)
    return role

def manualRole(allow_roll: bool):
    role = ''
    while True:
        ans = askInput()
        if checkListCommand(ans):
            print(*roles.allRoles, sep='\n')
        elif roles.allRoles.__contains__(ans):
            role = ans
            print(f'Selected {role}')
            break
        elif allow_roll and checkRollCommand(ans):
            role = rollRole()

            break
    return role

def rollSpecial(role):
    specialAbility = roles.roleDict[role][roles.ability]

    skill = dice.roll(1, 10)
    print(f'Rolled {specialAbility} = {skill}')
    return skill

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

def handleRole(is_random: bool):
    role = ''
    if is_random:
        role = rollRole()
    else:
        role = addRole()
    return role


def createCharacter(name: str, roll_all = False, roll_atr = False):
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
    body_Type = addBodyType()
    (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp) = rollAtributes()
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

def createRandomCharacter(name):
    role = rollRole()
    special = rollSpecial(role)
    body_type = rollBodyType()
    (atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp) = rollAtributes()

    DAO.addCharacter(
        name,
        role,
        special,
        body_type,
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

def createManualCharacter(name):
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
