import math
from math import floor
from colorama import Fore, Style


def coloredText(color, text):
    return f"""{color}{text}{Style.RESET_ALL}"""


def printRedLine(text):
    printColorLine(text, 'red')


def printGreenLine(text):
    printColorLine(text, 'green')


def printColorLine(text: str, color=''):
    t_color = Fore.WHITE
    if color == 'red':
        t_color = Fore.RED
    elif color == 'green':
        t_color = Fore.GREEN
    else:
        t_color = Fore.WHITE
    text = text + f'{Style.RESET_ALL}'
    print(t_color, text)



inputIndicator = coloredText(Fore.LIGHTMAGENTA_EX, "> ")
split_at = ' '
roll_str = '/roll'
list_str = '/list'

max_health = 40

INT = 'INT'
REF = 'REF'
TECH = 'TECH'
COOL = 'COOL'
ATTR = 'ATTR'
LUCK = 'LUCK'
MA = 'MA'
BODY = 'BODY'
EMP = 'EMP'

BODY_TYPE_MOD = 'BTM'
INIT_BONUS = 'INIT_BONUS'

GEAR_TIER_LOW = 'LOW'
GEAR_TIER_MID = 'MID'
GEAR_TIER_HIGH = 'HIGH'

GEAR_TIER_COMMON = 'COMMON'


def gear_is_allowed(wep_gear_tier, requested_tier):
    if requested_tier is None:
        return True
    else:
        gear_tier_matches = (gear_tiers_allowed(requested_tier).__contains__(wep_gear_tier))
        return gear_tier_matches


def gear_tiers_allowed(tier):
    if tier == GEAR_TIER_LOW:
        return [GEAR_TIER_LOW, GEAR_TIER_COMMON]
    elif tier == GEAR_TIER_MID:
        return [GEAR_TIER_MID, GEAR_TIER_COMMON]
    elif tier == GEAR_TIER_HIGH:
        return [GEAR_TIER_HIGH, GEAR_TIER_MID, GEAR_TIER_COMMON]
    else:
        return [GEAR_TIER_COMMON]

exit_commands = ['/e', '/q', '/exit', '/quit']
help_commands = ['/help', '/halp', '/h']
help_info = f"""<help> <optional combat / info / modify>"""
char_name = '<character_name>'

t_taser = 'taser'

t_melee = 'melee'
t_handgun = 'handgun'
t_smg = 'smg'
t_rifle = 'rifle'
t_thrown = 'throwing'
t_shotgun = 'shotgun'
t_heavy_weapon = 'heavy'
weapon_types = [t_melee, t_smg, t_handgun, t_shotgun, t_thrown, t_rifle, t_heavy_weapon]
guns = [t_handgun, t_smg, t_rifle, t_shotgun, t_heavy_weapon]

con_pocket = 'P'
con_jacket = 'J'
con_long_coat = 'L'
not_hideable = 'N'

all_con = [con_pocket, con_jacket, con_long_coat, not_hideable]

wep_very_reliable = 'VR'
wep_standard_reliability = 'ST'
wep_unreliable = 'UR'

wep_all_reliabilities = [wep_very_reliable, wep_standard_reliability, wep_unreliable]

notice_roll_str = '/notice'
notice_roll_help_str = f'{notice_roll_str} <roll_to_beat>'
add_character_for_notice_str = '/add_notice'
add_character_for_notice_help_str = f'{add_character_for_notice_str} {char_name}'
clear_notice_str = '/clear_notice'
rep_roll_str = 'rep'
hit_location_roll_str = 'hit_loc'
face_off_str = 'face_off'
roll_help_str = f"""{roll_str} <dice> / <{rep_roll_str}> / <{hit_location_roll_str}> 
/ <{face_off_str}> <character_name> / <skill> <character_name> <skill_num> <optional roll> <optional modifier>"""

very_reliables = ['very reliable', 'vr', 'VR']
reliables = ['reliable', 'r', 'R']
unreliables = ['unreliable', 'ur', 'UR']

fumble_str = '/fumble'
fumble_help_str = f'{fumble_str} <combat | ref | tech | emp | int>'
jam_str = '/jam'
jam_help_str = f'{jam_str} <reliability>'

body_part_head = 'head'
body_part_body = 'body'
body_part_r_arm = 'r_arm'
body_part_l_arm = 'l_arm'
body_part_r_leg = 'r_leg'
body_part_l_leg = 'l_leg'

body_parts = [body_part_head, body_part_body, body_part_l_arm, body_part_r_arm, body_part_r_leg, body_part_l_leg]

atr_int = 'atr_int'
atr_ref = 'atr_ref'
atr_tech = 'atr_tech'
atr_cool = 'atr_cool'
atr_attr = 'atr_attr'
atr_luck = 'atr_luck'
atr_ma = 'atr_ma'
atr_body = 'atr_body'
atr_emp = 'atr_emp'

body_type_mod = 'body_type_modifier'
init_bonus = 'initiative_bonus'

#these are for gear, including atr and body type modifiers
modifier_list = [INT, REF, TECH, COOL, ATTR, LUCK, MA, BODY, EMP, body_type_mod]
atr_info = f"""1 - {INT}
2 - {REF}
3 - {TECH}
4 - {COOL}
5 - {ATTR}
6 - {LUCK}
7 - {MA}
8 - {BODY}
9 - {EMP}
10 - {BODY_TYPE_MOD}
"""

body_parts_armor_info = f"""1 - {body_part_head}
2 - {body_part_body}
3 - {body_part_r_arm}
4 - {body_part_l_arm}
5 - {body_part_r_leg}
6 - {body_part_l_leg}
"""
add_char_str = '/add_char'
roll_all_str = 'roll_all'
roll_atr_str = 'roll_atr'
add_char_help_str = f'{add_char_str} <name> <optional {roll_all_str} / {roll_atr_str}>'
lvl_up_skill_str = '/lvl_up'
lvl_up_skill_help_str = f'{lvl_up_skill_str} {char_name} <skill_id (0 = special)> <skill_level 1-10> '
add_armor_str = '/add_armor'
add_armor_help_str = f'{add_armor_str} {char_name}'
explain_str = '/explain'
add_reputation_str = '/add_rep'
add_reputation_help_str = f'{add_reputation_str} {char_name} <|1-10|>'
advance_combat_initiative_str = '/aci'
list_combat_initiative_str = '/lci'
new_combat_initiative_str = '/nci'
new_combat_initiative_help_str = f'{new_combat_initiative_str} {char_name} <initiative>'
clear_combat_str = '/cc'
character_str = '/char'
list_rep_str = '/l_rep'
l_rep_help_str = f'{list_rep_str} {char_name}'
character_helper_str = f'{character_str} {char_name}'
list_skills_str = '/l_skill'
list_skills_helper_str = f"{list_skills_str} | optional 'atr' <attribute> | optional 'fuzzy' <string> | optional <character_name>"
stun_check_str = '/sc'
stun_check_help_str = f'{stun_check_str} {char_name}'
dmg_str = '/dmg'
dmg_helper_str = f'{dmg_str} {char_name} <body_part> <amount> <optional ap>'
melee_dmg_str = '/melee_dmg'
melee_dmg_help_str = f'{melee_dmg_str} {char_name} <optional dmg>'
suppressive_fire_def_str = '/sup_def'
suppressive_fire_def_help_str = f'{suppressive_fire_def_str} {char_name} <rounds> <area>'
add_weapon_str = '/add_weapon'
add_weapon_help_str = f'{add_weapon_str} {char_name}'
add_chrome_str = '/add_chrome'
add_chrome_help_str = f'{add_chrome_str} {char_name}'
attack_str = '/attack'
attack_help_str = f'{attack_str} <char> <attack_type melee | single | burst | fa> <range_for_guns except for full auto (fa)> <optional roll except for full auto (fa)>'
reload_str = '/reload'
reload_help_str = f'{reload_str} <weapon_id> <num_of_shots>'
medical_check_str = '/med_check'
medical_check_help_str = f'{medical_check_str} {char_name} <optional roll> [for the doctor]'
heal_str = '/heal'
heal_help_str = f'{heal_str} {char_name} <amount_healed> [for the patient]'
heal_calc_str = '/heal_calc'
heal_calc_help_str = f'{heal_calc_str} <days>'
repair_sp_str = '/repair_sp'
repair_sp_help_str = f'{repair_sp_str} <character_name>'
remove_armor_str = '/remove_armor'
remove_armor_help_str = f'{remove_armor_str} {char_name} <armor_id>'
add_status_str = '/add_status'
add_status_help_str = f'{add_status_str} {char_name}'
remove_status_str = '/rmv_status'
remove_status_help_str = f'{remove_status_str} {char_name} <status_id>'

difficulty_check_str = '/diff'

no_dmg_str = 'No damage'
light_dmg_str = 'Lightly damaged'
serious_dmg_str = 'Seriously damaged'
critical_dmg_str = 'Critically damaged'
mortally_wounded_str = 'Mortally wounded'
flatlined_str = 'Flatlined'

no_dmg = coloredText(Fore.GREEN, no_dmg_str)
light_dmg = coloredText(Fore.WHITE, light_dmg_str)
serious_dmg = coloredText(Fore.YELLOW, serious_dmg_str)
critical_dmg = coloredText(Fore.LIGHTRED_EX, critical_dmg_str)
mortally_wounded = coloredText(Fore.RED, mortally_wounded_str)
flatlined = coloredText(Fore.RED, flatlined_str)

attack_type_single = 'single'
attack_type_burst = 'burst'
attack_type_full_auto = 'full auto'
attack_type_melee = 'melee'

point_blank_range_str = 'Point blank'
close_range_str = 'Close'
medium_range_str = 'Medium'
long_range_str = 'Long'
extreme_range_str = 'Extreme'
impossible_range_str = 'Impossible'

unarmed = 'unarmed'

yes_no = '[Y/N]'


def infoStr(label: str, info: str):
    str = f"""********** {label} **********
{info}    
"""
    return str


def fieldName(field):
    return coloredText(Fore.LIGHTMAGENTA_EX, field)


def calculateModifierBonus(armors, cybernetics, modifier):
    bonus = 0
    uniq_atr_bonuses = []
    def contains(item):
        contains = False
        for i in uniq_atr_bonuses:
            if i.id == item.id:
                contains = True
                break

        return contains

    for armor in armors:
        if not contains(armor.atr_bonuses):
            uniq_atr_bonuses.append(armor.atr_bonuses)

    for cybernetic in cybernetics:
        if not contains(cybernetic.atr_bonuses):
            uniq_atr_bonuses.append(cybernetic.atr_bonuses)

    for atr_bonus in uniq_atr_bonuses:
        bonus += atr_bonus.attributes[modifier]

    return bonus


def divBy(val, div):
    return math.ceil(val / div)


def woundEffect(dmg_taken, ref, int, cool):
    r = ref
    i = int
    c = cool

    wnd_state = woundState(dmg_taken)
    if wnd_state == no_dmg:
        r = ref
        i = int
        c = cool
    elif wnd_state == light_dmg:
        r = ref
        i = int
        c = cool
    elif wnd_state == serious_dmg:
        r = ref - 2
        if r <= 0:
            r = 1
        i = int
        c = cool
    elif wnd_state == critical_dmg:
        r = divBy(ref, 2)
        i = divBy(int, 2)
        c = divBy(cool, 2)
    else:
        r = divBy(ref, 3)
        i = divBy(int, 3)
        c = divBy(cool, 3)

    return (r, i, c)


def askInput() -> str:
    return askInputCaseSensitive().lower().strip()


def askInputCaseSensitive() -> str:
    i = input(inputIndicator).replace("'", "’")
    return i


def askForRoll() -> (int, int, int, int):
    print('Give roll (e.g. 2D6+1 = 2-6-1-1, 1D6 = 1-6-1-0, 3D6/2+1 = 3-6-2-1)')
    input = askInput()
    parts = input.split('-')
    match parts:
        case [dice_s, die_s, divide_s, bonus_s]:
            dice = safeCastToInt(dice_s)
            die = safeCastToInt(die_s)
            divide_by = safeCastToInt(divide_s)
            if divide_by == 0:
                divide_by = 1
            bonus = safeCastToInt(bonus_s)
            return (dice, die, divide_by, bonus)
        case _:
            print('Invalid input')
            return askForRoll()


def uniqueArr(arr):
    print(f'arr: {arr}')
    uniq_arr = []
    for x in arr:
        if x not in uniq_arr:
            uniq_arr.append(x)
    return uniq_arr


def stunPenalty(dmg: int):
    return floor(dmg / 4)

def woundStatePlain(dmg_taken: int):
    stun_penalty = stunPenalty(dmg_taken)
    if dmg_taken == 0:
        return no_dmg_str
    elif stun_penalty == 0:
        return light_dmg_str
    elif stun_penalty == 1:
        return serious_dmg_str
    elif stun_penalty == 2:
        return critical_dmg_str
    elif dmg_taken < 40:
        return mortally_wounded_str
    else:
        return flatlined_str

def woundState(dmg_taken: int):
    stun_penalty = stunPenalty(dmg_taken)
    if dmg_taken == 0:
        return no_dmg
    elif stun_penalty == 0:
        return light_dmg
    elif stun_penalty == 1:
        return serious_dmg
    elif stun_penalty == 2:
        return critical_dmg
    elif dmg_taken < 40:
        return mortally_wounded
    else:
        return flatlined


def safeCastToInt(text):
    val = 0
    try:
        val = int(text)
    except (ValueError, TypeError):
        val = 0
    return val


def checkListCommand(cmnd: str) -> bool:
    return cmnd.startswith(list_str)


def checkRollCommand(cmnd: str) -> bool:
    return cmnd.startswith(roll_str)
