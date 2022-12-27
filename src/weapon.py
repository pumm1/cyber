import math

from gameHelper import weapon_types, t_shotgun, askInput, safeCastToInt, t_handgun, t_smg, t_rifle, t_thrown, BODY, \
    guns, EMP, point_blank_range_str, close_range_str, medium_range_str, long_range_str, extreme_range_str, \
    impossible_range_str, askForRoll
import dice
import cyberdao as DAO


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


    def isPointBlankRange(self, attack_range):
        if 0 < attack_range <= self.pointBlankLimit():
            return True
        return False

    def isCloseRange(self, attack_range):
        if attack_range <= self.closeRangeLimit():
            return True
        return False

    def isMidRange(self, attack_range):
        if attack_range <= self.midRangeLimit():
            return True
        return False

    def isLongRange(self, attack_range):
        if attack_range <= self.longRangeLimit():
            return True
        return False

    def isExtremeRange(self, attack_range):
        if attack_range <= self.extremeRangeLimit():
            return True
        return False

    def rollToBeatAndRangeStr(self, attack_range):
        roll_to_beat = 10
        range = point_blank_range_str
        range_str = ''
        if self.isPointBlankRange(attack_range):
            range_str = f'Point blank ({self.pointBlankLimit()}m)'
        elif self.isCloseRange(attack_range):
            range = close_range_str
            range_str = f'Close ({self.closeRangeLimit()}m)'
            roll_to_beat = 15
        elif self.isMidRange(attack_range):
            range = medium_range_str
            range_str = f'Medium ({self.midRangeLimit()}m)'
            roll_to_beat = 20
        elif self.isLongRange(attack_range):
            range = long_range_str
            range_str = f'Long ({self.longRangeLimit()}m)'
            roll_to_beat = 25
        elif self.isExtremeRange(attack_range):
            range = extreme_range_str
            range_str = f'Extreme ({self.extremeRangeLimit()}m)'
            roll_to_beat = 30
        elif attack_range < self.extremeRangeLimit():
            range = impossible_range_str
            range_str = range
            roll_to_beat = 999999

        return (roll_to_beat, range_str, range)

    def pointBlankLimit(self) -> int:
        return 1

    def closeRangeLimit(self) -> int:
        if self.weapon_type == t_shotgun:
            return 3
        else:
            return math.floor(self.range / 4)

    def midRangeLimit(self) -> int:
        if self.weapon_type == t_shotgun:
            return 5
        else:
            return math.floor(self.range / 2)

    def longRangeLimit(self) -> int:
        if self.weapon_type == t_shotgun:
            return 10
        else:
            return self.range

    def extremeRangeLimit(self) -> int:
        return self.range * 2


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

        (dice, die, bonus) = askForRoll()

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
    if weapon_t == t_shotgun:
        return 10
    elif weapon_t == t_handgun:
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
