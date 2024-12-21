very_weak = 'very weak'
weak = 'weak'
average = 'average'
strong = 'strong'
very_strong = 'very strong'
superhuman = 'superhuman'

label = 'label'
value = 'value'

available_modifiers = [very_weak, weak, average, strong, very_strong]
all_modifiers = [very_weak, weak, average, strong, very_strong, superhuman]


def listAvailableModifiers():
    t_modifiers = map(lambda mod: (
        f'{mod} ({available_modifiers.index(mod)})'
    ), available_modifiers)
    print(list(t_modifiers), sep='\n')


def listAllModifiers():
    print(all_modifiers, sep='\n')


def meleeDmgBonusByModifier(modifier) -> int:
    modifier_str = bodyTypeModifiersByValue(modifier)
    print(f'Determining melee DMG bonus for {modifier_str} ({modifier})')
    if modifier <= 4:
        return modifier - 2
    elif 4 < modifier <= 6:
        return 4
    elif 6 < modifier <= 8:
        return 6
    else:
        return 8

def bodyTypeByValue(body):
    if body <= 2:
        return very_weak
    elif 3 <= body <= 4:
        return weak
    elif 5 <= body <= 7:
        return average
    elif 8 <= body <= 9:
        return strong
    else:
        return strong


def bodyTypeModifiersByValue(modifier):
    if modifier == 0:
        return very_weak
    elif modifier == 1:
        return weak
    elif modifier == 2:
        return average
    elif modifier == 3:
        return strong
    elif modifier == 4:
        return very_strong
    else:
        return superhuman


def btm_as_value(body_type_modifier: str) -> int:
    if body_type_modifier == very_weak:
        return 0
    elif body_type_modifier == weak:
        return 1
    elif body_type_modifier == average:
        return 2
    elif body_type_modifier == strong:
        return 3
    elif body_type_modifier == very_strong:
        return 4
    else:
        return 5

