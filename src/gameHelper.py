inputIndicator = "> "
split_at = ' '
roll_str = '/roll'
list_str = '/list'

exit_commands = ['/e', '/q', '/exit', '/quit']
help_commands = ['/help', '/halp', '/h']
rep_roll_str = 'rep'
add_char_str = '/add_char'
add_char_help_str = f'{add_char_str} <name>'
explain_str = '/explain'
add_reputation_str = '/add_rep'


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
