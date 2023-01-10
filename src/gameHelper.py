from math import floor

inputIndicator = "> "
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


exit_commands = ['/e', '/q', '/exit', '/quit']
help_commands = ['/help', '/halp', '/h']
help_info = f"""<help> <optional combat / info / modify>"""

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

rep_roll_str = 'rep'
hit_location_roll_str = 'hit_loc'
hit_str = 'hit'
face_off_str = 'face_off'
roll_help_str = \
f"""{roll_str} <dice> / <{rep_roll_str}> / <{hit_str}> / <{hit_location_roll_str}> 
/ <{face_off_str}> <character_name> / <skill> <character_name> <skill_num> <optional modifier>"""

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

#these are for gear, including atr and body type modifiers
modifier_list = [atr_int, atr_ref, atr_tech, atr_cool, atr_attr, atr_luck, atr_ma, atr_body, atr_emp, body_type_mod]
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
char_name = '<character_name>'
add_char_str = '/add_char'
roll_all_str = 'roll_all'
roll_atr_str = 'roll_atr'
add_char_help_str = f'{add_char_str} <name> <optional {roll_all_str} / {roll_atr_str}>'
add_char_skill_str = '/add_char_skill'
add_char_skill_help_str = f'{add_char_skill_str} {char_name} <skill_id> <skill_level 1-10> '
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
list_skills_helpeer_str = f"{list_skills_str} | optional 'atr' <attribute> | optional 'fuzzy' <string> | optional <character_name>"
stun_check_str = '/sc'
stun_check_help_str = f'{stun_check_str} {char_name}'
dmg_str = '/dmg'
dmg_helper_str = f'{dmg_str} {char_name} <body_part> <amount> <optional ap>'
melee_dmg_str = '/melee_dmg'
melee_dmg_help_str = f'{melee_dmg_str} <attacker_name> <optional dmg>'
suppressive_fire_def_str = '/sup_def'
suppressive_fire_def_help_str = f'{suppressive_fire_def_str} {char_name} <rounds> <area>'
add_event_str = '/add_event'
list_event_str = '/l_events'
add_weapon_str = '/add_weapon'
add_weapon_help_str = f'{add_weapon_str} {char_name}'
add_chrome_str = '/add_chrome'
add_chrome_help_str = f'{add_chrome_str} {char_name}'
attack_str = '/attack'
attack_help_str = f'{attack_str} <char> <attack_type melee | single | burst | fa> <range_for_guns> <optional roll>'
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
remove_armor_help_str = f'{remove_armor_str} <character_name> <armor_id>'
add_status_str = '/add_status'
add_status_help_str = f'{add_status_str} <character_name>'

no_dmg = 'No damage'
light_dmg = 'Light damage'
serious_dmg = 'Serious damage'
critical_dmg = 'Critical damage'
mortally_wounded = 'Mortally wounded'
flatlined = 'Flatlined'

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


def askInput() -> str:
    return askInputCaseSensitive().lower()

def askInputCaseSensitive() -> str:
    i = input(inputIndicator).replace("'", "’")
    return i


def askForRoll() -> (int, int, int):
    print('Give roll (e.g. 2D6+1 = 2-6-1, 1D6 = 1-6)')
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
