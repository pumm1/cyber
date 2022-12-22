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
    print(available_modifiers, sep='\n')

def listAllModifiers():
    print(all_modifiers, sep='\n')

def checkBodyTypeFromStr(str):
    if all_modifiers.__contains__(str):
        return str
    else:
        return None

bodyTypeModifiersDict = {
    very_weak: 0,
    weak: 1,
    average: 2,
    strong: 3,
    very_strong: 4,
    superhuman: 5
}
