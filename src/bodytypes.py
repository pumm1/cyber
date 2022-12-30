very_weak = 'very weak'
weak = 'weak'
average = 'average'
strong = 'strong'
very_strong = 'very_strong'
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
        return modifier -2
    elif 4 < modifier <= 6:
        return 4
    elif 6 < modifier <= 8:
        return  6
    else:
        return 8


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

