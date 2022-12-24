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



exit_commands = ['/e', '/q', '/exit', '/quit']
help_commands = ['/help', '/halp', '/h']

t_melee = 'melee'
t_handgun = 'handgun'
t_smg = 'smg'
t_rifle = 'rifle'
t_thrown = 'throwing'
t_shotgun = 'shotgun'
weapon_types = [t_melee, t_smg, t_handgun, t_shotgun, t_thrown, t_rifle]
guns = [t_handgun, t_smg, t_rifle, t_shotgun]


rep_roll_str = 'rep'
hit_location_roll_str = 'hit_loc'
hit_str = 'hit'
roll_help_str = f'{roll_str} <{rep_roll_str}> / <{hit_str}> / <{hit_location_roll_str}> / char <character_name> <skill> <optional modifier>'

very_reliables = ['very reliable', 'vr', 'VR']
reliables = ['reliable', 'r', 'R']
unreliables = ['unreliable', 'ur', 'UR']

fumble_str = '/fumble'
fumble_help_str = f'{fumble_str} <combat | ref | tech | emp | int>'
jam_str = '/jam'
jam_help_str = f'{jam_str} <reliability>'

body_part_head = 'head'
body_part_body = 'body'
body_part_r_arm = 'r. arm'
body_part_l_arm = 'l. arm'
body_part_r_leg = 'r. leg'
body_part_l_leg = 'l. leg'

body_parts = [body_part_head, body_part_body, body_part_r_arm, body_part_l_arm, body_part_r_leg, body_part_l_leg]

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
add_char_skill_str = '/add_char_skill'
add_char_skill_help_str = f'{add_char_skill_str} <character_name> <skill_id> <skill_level 1-10> '
add_armor_str = '/add_armor'
add_armor_help_str = f'{add_armor_str} <character_name>'
explain_str = '/explain'
add_reputation_str = '/add_rep'
add_reputation_help_str = f'{add_reputation_str} <character_name> <|1-10|>'
advance_combat_initiative_str = '/aci'
list_combat_initiative_str = '/lci'
new_combat_initiative_str = '/nci'
new_combat_initiative_help_str = f'{new_combat_initiative_str} <character_name> <initiative>'
clear_combat_str = '/cc'
character_str = '/char'
list_rep_str = '/l_rep'
l_rep_help_str = f'{list_rep_str} <character_name>'
character_helper_str = f'{character_str} <name>'
list_skills_str = '/l_skill'
list_skills_helpeer_str = f"{list_skills_str} | optional 'atr' <attribute> | optional 'fuzzy' <string> | optional <character_name>"
stun_check_str = '/sc'
stun_check_help_str = f'{stun_check_str} <character_name>'
dmg_str = '/dmg'
dmg_helper_str = f'{dmg_str} <character_name> <body_part> <amount>'
add_event_str = '/add_event'
add_weapon_str = '/add_weapon'
add_weapon_help_str = f'{add_weapon_str} <character_name>'

def askInput() -> str:
    i = input(inputIndicator)
    return i

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
        return 'All ok'
    elif stun_penalty == 0:
        return 'Just a scratch'
    elif stun_penalty == 1:
        return 'Bleeding a bit'
    elif stun_penalty == 2:
        return 'Wounded quite badly'
    elif dmg_taken < 40:
        return 'Start rolling those death saves..'
    else:
        return 'Flatlined'


def safeCastToInt(text):
    val = 0
    try:
        val = int(text)
    except (ValueError, TypeError):
        val = 0
    return val


def checkListCommand(cmnd: str) -> bool:
    return cmnd.lower().startswith(list_str)


def checkRollCommand(cmnd: str) -> bool:
    return cmnd.lower().startswith(roll_str)
