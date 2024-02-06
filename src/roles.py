from genericGear import generic_helmet, generic_melee, generic_smg, generic_hvy_pistol, generic_lt_pistol, \
    generic_shotgun, generic_sawed_off_shotgun, generic_skin_weave, generic_kevlar_armor, generic_leather_pants, \
    generic_leather_armor, generic_bolt_rifle, generic_assault_rifle, generic_cyber_arm_l, \
    generic_cyber_arm_r, generic_cyber_leg_r, generic_cyber_leg_l, generic_scrambler, generic_nanosurgeons, \
    generic_cyber_contacts, generic_chip_slot, generic_infra_red, generic_smart_gun_link, generic_molotov, \
    generic_grenade, generic_emp, generic_hvy_smg, generic_katana, generic_face_plate, generic_torso_plate, \
    generic_auto_shotgun, generic_mantis_blades

ability = 'ability'
abilityDesc = 'ability description'
role_skills = 'skills'
role_guns = 'guns'
role_armors = 'armors'
role_chrome = 'chrome'

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
        role_skills: ['handgun', 'rifle', 'smg', 'stealth', 'intimidate', 'dodge/escape'],
        role_guns: [
            generic_assault_rifle, generic_shotgun, generic_sawed_off_shotgun, generic_melee, generic_smg,
            generic_hvy_pistol, generic_bolt_rifle, generic_grenade, generic_molotov, generic_hvy_smg,
            generic_auto_shotgun, generic_katana, generic_mantis_blades
        ],
        role_armors: [
            generic_helmet, generic_kevlar_armor, generic_leather_pants, generic_leather_armor, generic_skin_weave,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l, generic_torso_plate,
            generic_face_plate
        ],
        role_chrome: [
            generic_scrambler, generic_nanosurgeons, generic_cyber_contacts,
            generic_chip_slot, generic_infra_red, generic_smart_gun_link
        ]
    },
    rocker: {
        ability: 'Charismatic leadership',
        abilityDesc: 'Take control of a crowd (of your fans). Possible size of the crowd is increased by the skill level',
        role_skills: ['handgun', 'smg', 'play instrument', 'streetwise', 'perform', 'wardrobe and style', 'seduction', 'persuasion'],
        role_guns: [generic_melee, generic_smg, generic_hvy_pistol, generic_molotov, generic_katana, generic_mantis_blades],
        role_armors: [
            generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_nanosurgeons, generic_cyber_contacts, generic_chip_slot
        ]
    },
    netrunner: {
        ability: 'Interface',
        abilityDesc: 'Manipulate interface programs and go into the NET. ', #TODO: mieti house rulet tähän
        role_skills: ['handgun', 'programming', 'dodge/escape', 'system knowledge', 'electronic security', 'cyberdeck design'],
        role_guns: [generic_hvy_pistol, generic_melee, generic_emp, generic_katana, generic_mantis_blades, generic_smg],
        role_armors: [
            generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_scrambler, generic_cyber_contacts, generic_chip_slot, generic_infra_red
        ]
    },
    cop: {
        ability: 'Authority',
        abilityDesc: 'Ability to intimidate and control others through your position as a lawman. Also some access to police resources (e.g. information, equipment, weapons...)',
        role_skills: ['handgun', 'rifle', 'smg', 'driving', 'interrogation', 'streetwise'],
        role_guns: [
            generic_assault_rifle, generic_sawed_off_shotgun, generic_melee, generic_smg,
            generic_hvy_pistol, generic_bolt_rifle, generic_grenade, generic_hvy_smg,
            generic_auto_shotgun, generic_katana, generic_mantis_blades
        ],
        role_armors: [
            generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave, generic_kevlar_armor,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_nanosurgeons, generic_cyber_contacts,
            generic_infra_red, generic_smart_gun_link
        ]
    },
    media: {
        ability: 'Credibility',
        abilityDesc: 'Ability to be believed. Allows one to convince others to give information',
        role_skills: ['handgun', 'persuasion', 'streetwise', 'interview', 'dodge/escape', 'education', 'human perception', 'photography'],
        role_guns: [generic_lt_pistol, generic_melee, generic_hvy_pistol, generic_katana, generic_mantis_blades, generic_smg],
        role_armors: [
            generic_leather_armor, generic_leather_pants, generic_skin_weave, generic_cyber_leg_r, generic_cyber_leg_l,
            generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_scrambler, generic_cyber_contacts
        ]
    },
    nomad: {
        ability: 'Family',
        abilityDesc: 'Get help from your tribal family. Quality/amount of backup, information, cash, resources is based on the level',
        role_skills: ['handgun', 'streetwise', 'driving', 'motorcycle', 'rifle', 'basic tech', 'wilderness survival'],
        role_guns: [
            generic_melee, generic_hvy_pistol, generic_bolt_rifle, generic_sawed_off_shotgun,
            generic_molotov, generic_grenade, generic_katana, generic_mantis_blades
        ],
        role_armors: [
            generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_scrambler, generic_nanosurgeons, generic_cyber_contacts
        ]
    },
    meditechie: {
        ability: 'Medical tech',
        abilityDesc: 'Ability to perform surgeries and medical repairs - used also to install chrome. Small bonus to firs aid. See info on trauma team for more info.',
        role_skills: ['handgun', 'first aid', 'chemistry', 'diagnose illness', 'driving', 'piloting', 'cryotank operation', 'pharmaceuticals'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_lt_pistol, generic_grenade, generic_katana, generic_mantis_blades],
        role_armors: [
            generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave, generic_kevlar_armor,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_nanosurgeons, generic_cyber_contacts, generic_chip_slot, generic_infra_red
        ]
    },
    corp: {
        ability: 'Resources',
        abilityDesc: 'Ability to command corporate resources (e.g. Bodyguards, weapons, vehicles, buildings, money)',
        role_skills: ['handgun', 'stock market', 'human perception', 'social', 'personal grooming', 'wardrobe and style', 'oratory', 'intimidate'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_lt_pistol, generic_katana, generic_mantis_blades, generic_smg],
        role_armors: [
            generic_skin_weave, generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_scrambler, generic_cyber_contacts, generic_chip_slot
        ]
    },
    fixer: {
        ability: 'Streetdeal',
        abilityDesc: 'Ability to deal with underground information (Locate missing people, rumors, put gossip out, pick up clues, score big deals)',
        role_skills: ['handgun', 'streetwise', 'social', 'persuasion', 'pick lock', 'pick pocket', 'motorcycle', 'dodge/escape'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_lt_pistol, generic_molotov, generic_katana, generic_mantis_blades],
        role_armors: [
            generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_scrambler, generic_cyber_contacts, generic_chip_slot, generic_smart_gun_link
        ]
    },
    techie: {
        ability: 'Jury rig',
        abilityDesc: 'Allow repairing anything for 1D6 turns per level (Not permanent repairs!)',
        role_skills: ['handgun', 'basic tech', 'electronics', 'system knowledge', 'education', 'pick lock', 'rifle', 'driving', 'electronic security'],
        role_guns: [
            generic_melee, generic_hvy_pistol, generic_bolt_rifle, generic_sawed_off_shotgun,
            generic_molotov, generic_grenade, generic_auto_shotgun, generic_mantis_blades, generic_katana
        ],
        role_armors: [
            generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave, generic_kevlar_armor,
            generic_cyber_leg_r, generic_cyber_leg_l, generic_cyber_arm_r, generic_cyber_arm_l
        ],
        role_chrome: [
            generic_cyber_contacts, generic_chip_slot, generic_infra_red, generic_smart_gun_link
        ]
    }
}

def roleSpecialAbility(role):
    return roleDict[role][ability]

def roleSpecialAbilityDecription(role):
    return roleDict[role][abilityDesc]
