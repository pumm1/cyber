from gameHelper import weapon_types, t_shotgun, askInput, safeCastToInt, t_handgun, t_smg, t_rifle, t_thrown, BODY, \
    t_melee
import db.cyberdao as DAO

def addChracterWeapon(character_name):
    char = DAO.getCharacterByName(character_name)
    if char is not None:
        print(f'Give weapon name:')
        weapon_name = askInput()
        weapon_t = askWeaponType()
        weapon_range = rangeByType(char, weapon_t)
        is_chrome = askForChrome()
        rof = 1
        if weapon_t is not t_thrown or weapon_t is not t_melee:
            rof = askRof()

        (dice, die, bonus) = askForDmg()

        DAO.addWeapon(char.id, weapon_name, weapon_t, is_chrome, dice, die, bonus, weapon_range, rof)

        print('Weapon added!')


def askRof() -> int:
    print(f'Weapon ROF: (ROF > 0)')
    input = askInput()
    rof = safeCastToInt(input)
    if rof > 0:
        return rof
    else:
        askRof()


def rangeByType(char, weapon_t) -> int:
    range = 1
    if weapon_t is t_shotgun or weapon_t is t_handgun:
        range = 50
    elif weapon_t is t_smg:
        range = 150
    elif weapon_t is t_rifle:
        range = 400
    elif weapon_t is t_thrown:
        body = char.attributes[BODY]
        range = 10 * body

    return range

def askForDmg() -> (int, int, int):
    print('Give weapon dmg (e.g. 2D6+1 = 2-6-1, 1D6 = 1-6)')
    input = askInput()
    parts = input.split('-')
    match parts:
        case [dice_s, die_s]:
            dice = safeCastToInt(dice_s)
            die = safeCastToInt(die_s)
            return (dice, die, 0)
        case [dice_s, die_s, bonus_s]:
            dice = safeCastToInt(dice_s)
            die = safeCastToInt(die_s)
            bonus = safeCastToInt(bonus_s)
            return (dice, die, bonus)
        case _:
            print('Invalid input')
            return askForDmg()


def askForChrome() -> bool:
    is_chrome = False
    print('Is the weapon chrome? [y/n]')
    while True:
        input = askInput()
        i = input.lower()
        if input == 'y':
            is_chrome = True
            break
        elif input == 'n':
            is_chrome = False
            break
        else:
            print('Invalid answer')
    return is_chrome


def askWeaponType() -> str:
    weapon_types_str = ', '.join(weapon_types)
    print(f'Give weapon type ({weapon_types_str}):')
    weapon_type = ''
    while True:
        input = askInput()
        if weapon_types.__contains__(input):
            weapon_type = input
            break
        else:
            print('Invalid weapon type')
    return weapon_type
