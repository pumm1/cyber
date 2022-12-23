from math import floor

inputIndicator = "> "
split_at = ' '
roll_str = '/roll'
list_str = '/list'

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



rep_roll_str = 'rep'
hit_location_roll_str = 'hit_loc'
hit_str = 'hit'
roll_help_str = f'{roll_str} <{rep_roll_str}> / <{hit_str}> / <{hit_location_roll_str}> / char <character_name> <skill> <optional modifier>'

very_reliables = ['very reliable', 'vr', 'VR']
reliables = ['reliable', 'r', 'R']
unreliables = ['unreliable', 'ur', 'UR']

fumble_str = '/fumble'
fumble_help_str = f'{fumble_str} combat | ref | tech | emp | int'
jam_str = '/jam'
jam_help_str = f'{jam_str} <reliability>'

add_char_str = '/add_char'
roll_all_str = 'roll_all'
roll_atr_str = 'roll_atr'
add_char_help_str = f'{add_char_str} <name> <optional {roll_all_str} / {roll_atr_str}>'
add_char_skill_str = '/add_char_skill'
add_char_skill_help_str = f'{add_char_skill_str} <character_name> <skill_id> <skill_level 1-10> '
explain_str = '/explain'
add_reputation_str = '/add_rep'
advance_combat_initiative_str = '/aci'
list_combat_initiative_str = '/lci'
new_combat_initiative_str = '/nci'
new_combat_initiative_help_str = f'{new_combat_initiative_str} <character_name> <initiative>'
clear_combat_str = '/cc'
character_str = '/char'
character_helper_str = f'{character_str} <name>'
list_skills_str = '/l_skill'
list_skills_helpeer_str = f"{list_skills_str} | optional 'atr' <attribute> | optional 'fuzzy' <string> | optional <character_name>"
stun_check_str = '/sc'
stun_check_help_str = f'{stun_check_str} <character_name>'
dmg_str = '/dmg'
dmg_helper_str = f'{dmg_str} <character_name> <amount>'


def askInput() -> str:
    i = input(inputIndicator)
    return i


def stunPenalty(dmg: int):
    return floor(dmg / 4)


def woundState(dmg_taken: int):
    stun_penalty = stunPenalty(dmg_taken)
    if dmg_taken == 0:
        return 'At least physically healthy!'
    elif stun_penalty == 0:
        return 'Just a scratch'
    elif stun_penalty == 1:
        return 'Bleeding a bit'
    elif stun_penalty == 2:
        return 'Wounded quite badly'
    elif dmg_taken <= 40:
        return 'Start rolling those death saves..'
    else:
        return 'Flatlined.'


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
