inputIndicator = "> "
split_at = ' '
roll_str = '/roll'
list_str = '/list'

exit_commands = ['/e', '/q', '/exit', '/quit']
help_commands = ['/help', '/halp', '/h']

rep_roll_str = 'rep'
hit_location_roll_str = 'hit_loc'
hit_str = 'hit'
roll_help_str = f'{roll_str} <{rep_roll_str}> / <{hit_str}> / <{hit_location_roll_str}>'

add_char_str = '/add_char'
add_char_help_str = f'{add_char_str} <name>'
explain_str = '/explain'
add_reputation_str = '/add_rep'
advance_combat_initiative_str = '/aci'
list_combat_initiative_str = '/lci'
new_combat_initiative_str = '/nci'
new_combat_initiative_help_str = f'{new_combat_initiative_str} <character_name> <initiative>'
clear_combat_str = '/cc'
character_str = '/char'
character_helper_str = f'{character_str} <name>'
stun_check = ''


def askInput() -> str:
    i = input(inputIndicator)
    return i


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
