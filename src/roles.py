ability = 'ability'
abilityDesc = 'ability description'

#Roles
solo = 'Solo'
cop = 'Cop'
rocker = 'Rocker'
techie = 'Techie'
meditechie = 'Medtechie'
netrunner = 'Netrunner'
media = 'Media'
nomad = 'Nomad'
fixer = 'Fixer'
corp = 'Corp'

allRoles = [solo, cop, rocker, techie, media, meditechie, netrunner, nomad, fixer, corp]

roleDict = {
    solo: {
        ability: 'Combat sense',
        abilityDesc: 'Add the combat sense value to your awareness and initiative rolls'
    },
    rocker: {
        ability: 'Charismatic leadership',
        abilityDesc: 'Take control of a crowd (of your fans). Possible size of the crowd is increased by the skill level'
    },
    netrunner: {
        ability: 'Interface',
        abilityDesc: 'Manipulate interface programs and go into the NET. ' #TODO: mieti house rulet tähän
    },
    cop: {
        ability: 'Authority',
        abilityDesc: 'Ability to intimidate and control others through your position as a lawman. Also some access to police resources (e.g. information, equipment, weapons...)'
    },
    media: {
        ability: 'Credibility',
        abilityDesc: 'Ability to be believed. Allows one to convince others to give information'
    },
    nomad: {
        ability: 'Family',
        abilityDesc: 'Get help from your tribal family. Quality/amount of backup, information, cash, resources is based on the level'
    },
    meditechie: {
        ability: 'Medical tech',
        abilityDesc: 'Ability to perform surgeries and medical repairs - used also to install chrome. Small bonus to firs aid. See info on trauma team for more info.'
    },
    corp: {
        ability: 'Resources',
        abilityDesc: 'Ability to command corporate resources (e.g. Bodyguards, weapons, vehicles, buildings, money)'
    },
    fixer: {
        ability: 'Streetdeal',
        abilityDesc: 'Ability to deal with underground information (Locate missing people, rumors, put gossip out, pick up clues, score big deals)'
    },
    techie: {
        ability: 'Jury rig',
        abilityDesc: 'Allow repairing anything for 1D6 turns per level (Not permanent repairs!)'
    }
}

def roleSpecialAbility(role):
    return roleDict[role][ability]

def roleSpecialAbilityDecription(role):
    return roleDict[role][abilityDesc]
