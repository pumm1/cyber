import math

from colorama import Fore

from src.gameHelper import weapon_types, t_shotgun, askInput, safeCastToInt, t_handgun, t_smg, t_rifle, t_thrown, BODY, \
    guns, point_blank_range_str, close_range_str, medium_range_str, long_range_str, extreme_range_str, \
    impossible_range_str, askForRoll, all_con, wep_all_reliabilities, yes_no, coloredText, con_pocket, \
    wep_standard_reliability
import src.dice as dice
from src.logger import Log, log_event, log_pos, log_neg, log_neutral


class Weapon:
    def __init__(self, row, custom_range: int | None):
        self.weapon_id = row['id']
        self.character_id = row['character_id']
        self.item = row['item']
        self.weapon_type = row['weapon_type']
        self.is_chrome = row['is_chrome']
        self.dice_num = row['dice_number']
        self.dice_dmg = row['dice_dmg']
        self.divide_by = row['divide_by']
        self.dmg_bonus = row['dmg_bonus']
        self.weight = row['weight']
        if custom_range is None:
            self.range = row['range']
        else:
            self.range = custom_range
        self.rof = row['rof']
        self.clip_size = row['clip_size']
        self.shots_left = row['shots_left']
        self.effect_radius = row['effect_radius']
        self.wa = row['wa']
        self.con = row['con']
        self.reliability = row['reliability']


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
            return 5
        else:
            return math.floor(self.range / 4)

    def midRangeLimit(self) -> int:
        if self.weapon_type == t_shotgun:
            return 8
        else:
            return math.floor(self.range / 2)

    def longRangeLimit(self) -> int:
        if self.weapon_type == t_shotgun:
            return 10
        else:
            return self.range

    def extremeRangeLimit(self) -> int:
        if self.weapon_type == t_shotgun:
            return 15
        else:
            return self.range * 2


    def asJson(self):
        resJson = {
            'id': self.weapon_id,
            'characterId': self.character_id,
            'item': self.item,
            'range': self.range,
            'dmg': self.dice_dmg,
            'divideBy': self.divide_by,
            'diceNum': self.dice_num,
            'weight': self.weight,
            'clipSize': self.clip_size,
            'rof': self.rof,
            'shotsLeft': self.shots_left,
            'reliability': self.reliability,
            'con': self.con,
            'isChrome': self.is_chrome,
            'effectRadius': self.effect_radius,
            'weaponType': self.weapon_type,
            'dmgBonus': self.dmg_bonus,
            'extremeRangeLimit': self.extremeRangeLimit(),
            'longRangeLimit:': self.longRangeLimit(),
            'midRangeLimit': self.midRangeLimit(),
            'closeRangeLimit': self.closeRangeLimit(),
            'pointBlankLimit': self.pointBlankLimit()
        }

        return resJson


    def toStr(self):
        cybernetic_str = ''
        if self.is_chrome:
            cybernetic_str = ' [cybernetic]'
        str = f'(id: {self.weapon_id}) {coloredText(Fore.LIGHTCYAN_EX ,self.item)} ({self.weapon_type}{cybernetic_str}) [{self.shots_left} / {self.clip_size}] - {dice.diceToStr(self.dice_num, self.dice_dmg, self.divide_by, self.dmg_bonus)} | WA: {self.wa} | range {self.range}m | #ROF: {self.rof} | REL: {self.reliability} | CON: {self.con}'
        return str

    def isGun(self) -> bool:
        return guns.__contains__(self.weapon_type)

    def isThrown(self) -> bool:
        return self.weapon_type == t_thrown

def manualWeaponFromReq(weapon_type, wa, rof, clip_size, shots_left, custom_range: int | None, item=None, body=5):
    row = {
        'id': 0,
        'character_id': 0,
        'item': 'weapon check tool',
        'weapon_type': weapon_type,
        'wa': wa,
        'is_chrome': False,
        'dice_number': 4,
        'dice_dmg': 6,
        'divide_by': 1,
        'dmg_bonus': 0,
        'weight': 1,
        'range': rangeByType(5, weapon_type, custom_range),
        'custom_range': custom_range,
        'rof': rof,
        'clip_size': clip_size,
        'shots_left': shots_left,
        'effect_radius': 0,
        'con': con_pocket,
        'reliability': wep_standard_reliability
    }

    return Weapon(row, custom_range)


def askRof() -> int:
    print(f'Weapon ROF: (ROF > 0)')
    rof = 0
    while True:
        input = askInput()
        rof = safeCastToInt(input)
        if rof > 0:
            break
    return rof


def rangeByType(body, weapon_t, custom_range=None) -> int:
    range = 1
    if custom_range is not None and custom_range > 0:
        return custom_range
    if weapon_t == t_shotgun:
        return 10
    elif weapon_t == t_handgun:
        range = 50
    elif weapon_t == t_smg:
        range = 150
    elif weapon_t == t_rifle:
        range = 400
    elif weapon_t == t_thrown:
        range = 10 * body

    print(f'{weapon_t} range: {range}m')

    return range


def askForChrome() -> bool:
    is_chrome = False
    print(f'Is the weapon chrome? {yes_no}')
    while True:
        input = askInput()
        if input == 'y':
            is_chrome = True
            break
        elif input == 'n':
            is_chrome = False
            break
        else:
            print('Invalid answer')
    return is_chrome

def askCon():
    con_opt = ', '.join(all_con)
    print(f'Give con: ({con_opt})')
    con = ''
    while True:
        i = askInput().upper()
        if all_con.__contains__(i):
            con = i
            break
    return con


def askWeight():
    print('Give weapon weight')
    i = askInput()
    weight = safeCastToInt(i)
    return weight


def askReliability():
    rel_opts = ','.join(wep_all_reliabilities)
    rel = ''
    print(f'Give reliability: ({rel_opts})')
    while True:
        i = askInput().upper()
        if wep_all_reliabilities.__contains__(i):
            rel = i
            break
    return rel



def askWa():
    print('Give WA:')
    i = askInput()
    wa = safeCastToInt(i)
    return wa


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
