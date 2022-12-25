import math

from gameHelper import weapon_types, t_shotgun, askInput, safeCastToInt, t_handgun, t_smg, t_rifle, t_thrown, BODY, \
    t_melee, guns, EMP
import dice
import db.cyberdao as DAO


class Weapon:
    def __init__(self, row):
        self.weapon_id = row['id']
        self.item = row['item']
        self.weapon_type = row['weapon_type']
        self.is_chrome = row['is_chrome']
        self.dice_num = row['dice_number']
        self.dice_dmg = row['dice_dmg']
        self.dmg_bonus = row['dmg_bonus']
        self.range = row['range']
        self.rof = row['rof']
        self.clip_size = row['clip_size']
        self.shots_left = row['shots_left']


    def toStr(self):
        cybernetic_str = ''
        if self.is_chrome:
            cybernetic_str = ' [cybernetic]'
        str = f'(id: {self.weapon_id}) {self.item} ({self.weapon_type}{cybernetic_str}) [{self.shots_left} / {self.clip_size}] - {dice.diceToStr(self.dice_num, self.dice_dmg, self.dmg_bonus)} | range {self.range}m | #ROF: {self.rof}'
        return str

    def isGun(self) -> bool:
        return guns.__contains__(self.weapon_type)

def addChracterWeapon(character_name):
    char = DAO.getCharacterByName(character_name)
    if char is not None:
        print(f'Give weapon name:')
        weapon_name = askInput()
        (weapon_t, clip_size) = askWeaponType()
        weapon_range = rangeByType(char, weapon_t)
        is_chrome = askForChrome()
        rof = 1
        if guns.__contains__(weapon_t):
            rof = askRof()

        if rof is None:
            print('NO ROF!')

        (dice, die, bonus) = askForDmg()

        DAO.addWeapon(char.id, weapon_name, weapon_t, is_chrome, dice, die, bonus, weapon_range, rof, clip_size)
        if is_chrome:
            print('Reduce humanity for chrome:')
            while True:
                i = askInput()
                hum_cost = safeCastToInt(i)
                if hum_cost > 0:
                    curr_hum = char.humanity
                    print(f'Current humanity {curr_hum}')
                    t_hum = curr_hum - hum_cost
                    emp = math.ceil(t_hum / 10)
                    print(f'Curr emp: {char.attributes[EMP]} - new emp: {emp}')

                    DAO.reduceHumanity(char.id, t_hum, emp)
                    print(f'Updated humanity and empathy')
                    break

        print('Weapon added!')


def askRof() -> int:
    print(f'Weapon ROF: (ROF > 0)')
    rof = 0
    while True:
        input = askInput()
        rof = safeCastToInt(input)
        if rof > 0:
            break
    return rof



def rangeByType(char, weapon_t) -> int:
    range = 1
    if weapon_t == t_shotgun or weapon_t == t_handgun:
        range = 50
    elif weapon_t == t_smg:
        range = 150
    elif weapon_t == t_rifle:
        range = 400
    elif weapon_t == t_thrown:
        body = char.attributes[BODY]
        range = 10 * body

    print(f'{weapon_t} range: {range}m')

    return range

def askForDmg() -> (int, int, int):
    print('Give weapon dmg (e.g. 2D6+1 = 2-6-1, 1D6 = 1-6)')
    input = askInput()
    parts = input.split('-')
    match parts:
        case [dice_s, die_s]:
            dice = safeCastToInt(dice_s)
            die = safeCastToInt(die_s)
            bonus = 0
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
    clip_size = 0
    print(f'Give weapon type ({weapon_types_str}):')
    weapon_type = ''
    while True:
        input = askInput()
        if weapon_types.__contains__(input):
            weapon_type = input

            break
        else:
            print('Invalid weapon type')

    if guns.__contains__(weapon_type):
        while True:
            print('Give clip size:')
            input = askInput()
            cs = safeCastToInt(input)
            if cs > 0:
                clip_size = cs
                break


    return (weapon_type, clip_size)
