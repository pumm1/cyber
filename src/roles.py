ability = 'ability'
abilityDesc = 'ability description'
role_skills = 'skills'

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
        abilityDesc: 'Add the combat sense value to your awareness and initiative rolls',
        role_skills: ['handgun', 'rifle', 'smg', 'stealth', 'intimidate', 'dodge/escape']
    },
    rocker: {
        ability: 'Charismatic leadership',
        abilityDesc: 'Take control of a crowd (of your fans). Possible size of the crowd is increased by the skill level',
        role_skills: ['handgun', 'play instrument', 'streetwise', 'perform', 'wardrobe and style', 'seduction', 'persuasion']
    },
    netrunner: {
        ability: 'Interface',
        abilityDesc: 'Manipulate interface programs and go into the NET. ', #TODO: mieti house rulet tähän
        role_skills: ['handgun', 'programming', 'dodge/escape', 'system knowledge', 'electronic security', 'cyberdeck design']
    },
    cop: {
        ability: 'Authority',
        abilityDesc: 'Ability to intimidate and control others through your position as a lawman. Also some access to police resources (e.g. information, equipment, weapons...)',
        role_skills: ['handgun', 'rifle', 'smg', 'driving', 'interrogation', 'streetwise']
    },
    media: {
        ability: 'Credibility',
        abilityDesc: 'Ability to be believed. Allows one to convince others to give information',
        role_skills: ['handgun', 'persuasion', 'streetwise', 'interview', 'dodge/escape', 'education', 'human perception', 'photography']
    },
    nomad: {
        ability: 'Family',
        abilityDesc: 'Get help from your tribal family. Quality/amount of backup, information, cash, resources is based on the level',
        role_skills: ['handgun', 'streetwise', 'driving', 'motorcycle', 'rifle', 'basic tech', 'wilderness survival']
    },
    meditechie: {
        ability: 'Medical tech',
        abilityDesc: 'Ability to perform surgeries and medical repairs - used also to install chrome. Small bonus to firs aid. See info on trauma team for more info.',
        role_skills: ['handgun', 'first aid', 'chemistry', 'diagnose illness', 'driving', 'piloting', 'cryotank operation', 'pharmaceuticals']
    },
    corp: {
        ability: 'Resources',
        abilityDesc: 'Ability to command corporate resources (e.g. Bodyguards, weapons, vehicles, buildings, money)',
        role_skills: ['handgun', 'stock market', 'human perception', 'social', 'personal grooming', 'wardrobe and style', 'oratory', 'intimidate']
    },
    fixer: {
        ability: 'Streetdeal',
        abilityDesc: 'Ability to deal with underground information (Locate missing people, rumors, put gossip out, pick up clues, score big deals)',
        role_skills: ['handgun', 'streetwise', 'social', 'persuasion', 'pick lock', 'pick pocket', 'motorcycle', 'dodge/escape']
    },
    techie: {
        ability: 'Jury rig',
        abilityDesc: 'Allow repairing anything for 1D6 turns per level (Not permanent repairs!)',
        role_skills: ['handgun', 'basic tech', 'electronics', 'system knowledge', 'education', 'pick lock', 'rifle', 'driving', 'electronic security']
    }
}

def roleSpecialAbility(role):
    return roleDict[role][ability]

def roleSpecialAbilityDecription(role):
    return roleDict[role][abilityDesc]
