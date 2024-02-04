from src.gameHelper import not_hideable, con_jacket, con_pocket, t_handgun, t_smg, t_rifle, t_shotgun, t_melee, \
    wep_standard_reliability, con_long_coat, body_part_body, body_part_l_arm, body_part_r_arm, body_part_l_leg, \
    body_part_r_leg, body_part_head

ability = 'ability'
abilityDesc = 'ability description'
role_skills = 'skills'
role_guns = 'guns'
role_armors = 'armors'

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

#generic guns

dice_str = 'dice'
die_str = 'die'
divide_by_str = 'divideBy'
bonus_str = 'bonus'
weapon_name_str = 'weaponName'
clip_size_str = 'clipSize'
rof_str = 'rof'
humanity_cost_str = 'humanityCost'
weapon_type_str = 'weaponType'
wa_str = 'wa'
con_str = 'con'
weight_str = 'weight'
reliability_str = 'reliability'
effect_radius_str = 'effectRadius'
custom_range_str = 'customRange'

generic_lt_pistol = {
    dice_str: 2,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Light pistol',
    clip_size_str: 10,
    rof_str: 2,
    humanity_cost_str: 0,
    weapon_type_str: t_handgun,
    wa_str: 0,
    con_str: con_pocket,
    weight_str: 2,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}

generic_hvy_pistol = {
    dice_str: 3,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Heavy pistol',
    clip_size_str: 8,
    rof_str: 2,
    humanity_cost_str: 0,
    weapon_type_str: t_handgun,
    wa_str: 0,
    con_str: con_pocket,
    weight_str: 2,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}

generic_smg = {
    dice_str: 2,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'SMG',
    clip_size_str: 30,
    rof_str: 30,
    humanity_cost_str: 0,
    weapon_type_str: t_smg,
    wa_str: 0,
    con_str: con_jacket,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}

generic_bolt_rifle = {
    dice_str: 5,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Rifle',
    clip_size_str: 5,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_rifle,
    wa_str: 1,
    con_str: not_hideable,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}

generic_assault_rifle = {
    dice_str: 4,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Rifle',
    clip_size_str: 30,
    rof_str: 25,
    humanity_cost_str: 0,
    weapon_type_str: t_rifle,
    wa_str: 0,
    con_str: not_hideable,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}
generic_melee = {
    dice_str: 2,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Knife (AP)',
    clip_size_str: 1,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_melee,
    wa_str: 0,
    con_str: con_pocket,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}


generic_shotgun = {
    dice_str: 4,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Shotgun',
    clip_size_str: 6,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_shotgun,
    wa_str: 0,
    con_str: con_long_coat,
    weight_str: 4,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}

generic_sawed_off_shotgun = {
    dice_str: 4,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Sawed off shotgun',
    clip_size_str: 2,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_shotgun,
    wa_str: 0,
    con_str: con_long_coat,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0
}
armor_name_str = 'armor'
ev_str = 'ev'
sp_str = 'sp'
covered_parts_str = 'coveredParts'
atr_bonuses_str = 'atrBonuses'
skill_bonuses_str = 'skillBonuses'

generic_leather_armor = {
    armor_name_str: 'Heavy leather jacket',
    ev_str: 0,
    humanity_cost_str: 0,
    sp_str: 8,
    covered_parts_str: [body_part_body, body_part_l_arm, body_part_r_arm],
    atr_bonuses_str: [],
    skill_bonuses_str: []
}

generic_leather_pants = {
    armor_name_str: 'Leather jacket',
    ev_str: 0,
    humanity_cost_str: 0,
    sp_str: 4,
    covered_parts_str: [body_part_l_leg, body_part_r_leg],
    atr_bonuses_str: [],
    skill_bonuses_str: []
}


generic_kevlar_armor = {
    armor_name_str: 'Kevlar armor',
    ev_str: 0,
    humanity_cost_str: 0,
    sp_str: 10,
    covered_parts_str: [body_part_body],
    atr_bonuses_str: [],
    skill_bonuses_str: []
}

generic_skin_weave = {
    armor_name_str: 'Skin weave',
    ev_str: 0,
    humanity_cost_str: 5,
    sp_str: 4,
    covered_parts_str: [body_part_body, body_part_l_arm, body_part_r_arm, body_part_l_leg, body_part_r_leg, body_part_head],
    atr_bonuses_str: [],
    skill_bonuses_str: []
}

generic_helmet = {
    armor_name_str: 'Helmet',
    ev_str: 0,
    humanity_cost_str: 0,
    sp_str: 10,
    covered_parts_str: [body_part_head],
    atr_bonuses_str: [],
    skill_bonuses_str: []
}
#TODO: move generic gear to own file

allRoles = [solo, cop, rocker, techie, media, meditechie, netrunner, nomad, fixer, corp]

roleDict = {
    solo: {
        ability: 'Combat sense',
        abilityDesc: 'Add the combat sense value to your awareness and initiative rolls',
        role_skills: ['handgun', 'rifle', 'smg', 'stealth', 'intimidate', 'dodge/escape'],
        role_guns: [generic_assault_rifle, generic_sawed_off_shotgun, generic_melee, generic_smg, generic_hvy_pistol, generic_bolt_rifle],
        role_armors: [generic_helmet, generic_kevlar_armor, generic_leather_pants, generic_leather_armor, generic_skin_weave]
    },
    rocker: {
        ability: 'Charismatic leadership',
        abilityDesc: 'Take control of a crowd (of your fans). Possible size of the crowd is increased by the skill level',
        role_skills: ['handgun', 'smg', 'play instrument', 'streetwise', 'perform', 'wardrobe and style', 'seduction', 'persuasion'],
        role_guns: [generic_melee, generic_smg, generic_hvy_pistol, generic_lt_pistol],
        role_armors: [generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave]
    },
    netrunner: {
        ability: 'Interface',
        abilityDesc: 'Manipulate interface programs and go into the NET. ', #TODO: mieti house rulet tähän
        role_skills: ['handgun', 'programming', 'dodge/escape', 'system knowledge', 'electronic security', 'cyberdeck design'],
        role_guns: [generic_hvy_pistol, generic_melee],
        role_armors: [generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave]
    },
    cop: {
        ability: 'Authority',
        abilityDesc: 'Ability to intimidate and control others through your position as a lawman. Also some access to police resources (e.g. information, equipment, weapons...)',
        role_skills: ['handgun', 'rifle', 'smg', 'driving', 'interrogation', 'streetwise'],
        role_guns: [generic_assault_rifle, generic_sawed_off_shotgun, generic_melee, generic_smg, generic_hvy_pistol, generic_bolt_rifle],
        role_armors: [generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave, generic_kevlar_armor]
    },
    media: {
        ability: 'Credibility',
        abilityDesc: 'Ability to be believed. Allows one to convince others to give information',
        role_skills: ['handgun', 'persuasion', 'streetwise', 'interview', 'dodge/escape', 'education', 'human perception', 'photography'],
        role_guns: [generic_lt_pistol, generic_melee, generic_hvy_pistol],
        role_armors: [generic_leather_armor, generic_leather_pants, generic_skin_weave]
    },
    nomad: {
        ability: 'Family',
        abilityDesc: 'Get help from your tribal family. Quality/amount of backup, information, cash, resources is based on the level',
        role_skills: ['handgun', 'streetwise', 'driving', 'motorcycle', 'rifle', 'basic tech', 'wilderness survival'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_bolt_rifle, generic_sawed_off_shotgun],
        role_armors: [generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave]
    },
    meditechie: {
        ability: 'Medical tech',
        abilityDesc: 'Ability to perform surgeries and medical repairs - used also to install chrome. Small bonus to firs aid. See info on trauma team for more info.',
        role_skills: ['handgun', 'first aid', 'chemistry', 'diagnose illness', 'driving', 'piloting', 'cryotank operation', 'pharmaceuticals'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_lt_pistol],
        role_armors: [generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave, generic_kevlar_armor]
    },
    corp: {
        ability: 'Resources',
        abilityDesc: 'Ability to command corporate resources (e.g. Bodyguards, weapons, vehicles, buildings, money)',
        role_skills: ['handgun', 'stock market', 'human perception', 'social', 'personal grooming', 'wardrobe and style', 'oratory', 'intimidate'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_lt_pistol],
        role_armors: [generic_skin_weave]
    },
    fixer: {
        ability: 'Streetdeal',
        abilityDesc: 'Ability to deal with underground information (Locate missing people, rumors, put gossip out, pick up clues, score big deals)',
        role_skills: ['handgun', 'streetwise', 'social', 'persuasion', 'pick lock', 'pick pocket', 'motorcycle', 'dodge/escape'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_lt_pistol],
        role_armors: [generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave]
    },
    techie: {
        ability: 'Jury rig',
        abilityDesc: 'Allow repairing anything for 1D6 turns per level (Not permanent repairs!)',
        role_skills: ['handgun', 'basic tech', 'electronics', 'system knowledge', 'education', 'pick lock', 'rifle', 'driving', 'electronic security'],
        role_guns: [generic_melee, generic_hvy_pistol, generic_bolt_rifle, generic_sawed_off_shotgun],
        role_armors: [generic_helmet, generic_leather_armor, generic_leather_pants, generic_skin_weave, generic_kevlar_armor]
    }
}

def roleSpecialAbility(role):
    return roleDict[role][ability]

def roleSpecialAbilityDecription(role):
    return roleDict[role][abilityDesc]
