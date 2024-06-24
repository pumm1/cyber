from src.gameHelper import not_hideable, con_jacket, con_pocket, t_handgun, t_smg, t_rifle, t_shotgun, t_melee, \
    wep_standard_reliability, con_long_coat, body_part_body, body_part_l_arm, body_part_r_arm, body_part_l_leg, \
    body_part_r_leg, body_part_head, t_thrown, GEAR_TIER_LOW, GEAR_TIER_MID, GEAR_TIER_HIGH, GEAR_TIER_COMMON

# generic guns

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
tier_str = 'tier'

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
    custom_range_str: 0,
    tier_str: GEAR_TIER_LOW
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
    custom_range_str: 0,
    tier_str: GEAR_TIER_LOW
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
    custom_range_str: 0,
    tier_str: GEAR_TIER_MID
}


generic_hvy_smg = {
    dice_str: 3,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 1,
    weapon_name_str: 'Heavy SMG',
    clip_size_str: 30,
    rof_str: 25,
    humanity_cost_str: 0,
    weapon_type_str: t_smg,
    wa_str: 0,
    con_str: con_jacket,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0,
    tier_str: GEAR_TIER_HIGH
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
    custom_range_str: 0,
    tier_str: GEAR_TIER_MID
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
    custom_range_str: 0,
    tier_str: GEAR_TIER_HIGH
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
    custom_range_str: 0,
    tier_str: GEAR_TIER_LOW
}

generic_melee_2 = {
    dice_str: 3,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Spiked baseball bat',
    clip_size_str: 1,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_melee,
    wa_str: 0,
    con_str: con_pocket,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0,
    tier_str: GEAR_TIER_LOW
}

generic_katana = {
    dice_str: 4,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Katana (AP)',
    clip_size_str: 1,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_melee,
    wa_str: 0,
    con_str: con_pocket,
    weight_str: 3,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0,
    tier_str: GEAR_TIER_LOW
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
    custom_range_str: 0,
    tier_str: GEAR_TIER_MID
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
    custom_range_str: 0,
    tier_str: GEAR_TIER_LOW
}

generic_auto_shotgun = {
    dice_str: 4,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Auto shotgun',
    clip_size_str: 10,
    rof_str: 5,
    humanity_cost_str: 0,
    weapon_type_str: t_shotgun,
    wa_str: 0,
    con_str: con_long_coat,
    weight_str: 4,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0,
    tier_str: GEAR_TIER_HIGH
}

generic_molotov = {
    dice_str: 4,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Molotov cocktail',
    clip_size_str: 1,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_thrown,
    wa_str: 0,
    con_str: con_long_coat,
    weight_str: 2,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 5,
    custom_range_str: 0,
    tier_str: GEAR_TIER_LOW
}

generic_grenade = {
    dice_str: 6,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Grenade (HE)',
    clip_size_str: 1,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_thrown,
    wa_str: 0,
    con_str: con_long_coat,
    weight_str: 2,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 5,
    custom_range_str: 0,
    tier_str: GEAR_TIER_HIGH
}

generic_emp = {
    dice_str: 0,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'EMP grenade',
    clip_size_str: 1,
    rof_str: 1,
    humanity_cost_str: 0,
    weapon_type_str: t_thrown,
    wa_str: 0,
    con_str: con_long_coat,
    weight_str: 2,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 5,
    custom_range_str: 0,
    tier_str: GEAR_TIER_HIGH
}

generic_mantis_blades = {
    dice_str: 4,
    die_str: 6,
    divide_by_str: 1,
    bonus_str: 0,
    weapon_name_str: 'Mantis blades (AP)',
    clip_size_str: 1,
    rof_str: 1,
    humanity_cost_str: 9,
    weapon_type_str: t_melee,
    wa_str: 0,
    con_str: con_pocket,
    weight_str: 2,
    reliability_str: wep_standard_reliability,
    effect_radius_str: 0,
    custom_range_str: 0,
    tier_str: GEAR_TIER_MID
}

# generic armor

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
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_LOW
}

generic_leather_pants = {
    armor_name_str: 'Leather pants',
    ev_str: 0,
    humanity_cost_str: 0,
    sp_str: 4,
    covered_parts_str: [body_part_l_leg, body_part_r_leg],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_LOW
}

generic_kevlar_armor = {
    armor_name_str: 'Kevlar armor',
    ev_str: 0,
    humanity_cost_str: 0,
    sp_str: 10,
    covered_parts_str: [body_part_body],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_MID
}

generic_skin_weave = {
    armor_name_str: 'Skin weave',
    ev_str: 0,
    humanity_cost_str: 5,
    sp_str: 4,
    covered_parts_str: [body_part_body, body_part_l_arm, body_part_r_arm, body_part_l_leg, body_part_r_leg,
                        body_part_head],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_MID
}

generic_helmet = {
    armor_name_str: 'Helmet',
    ev_str: 0,
    humanity_cost_str: 0,
    sp_str: 10,
    covered_parts_str: [body_part_head],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_MID
}

#generic armor that is also chrome

generic_cyber_arm_l = {
    armor_name_str: 'Cyber arm (L)',
    ev_str: 0,
    humanity_cost_str: 4,
    sp_str: 4,
    covered_parts_str: [body_part_l_arm],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_cyber_arm_r = {
    armor_name_str: 'Cyber arm (R)',
    ev_str: 0,
    humanity_cost_str: 4,
    sp_str: 4,
    covered_parts_str: [body_part_r_arm],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_cyber_leg_r = {
    armor_name_str: 'Cyber leg (R)',
    ev_str: 0,
    humanity_cost_str: 4,
    sp_str: 4,
    covered_parts_str: [body_part_r_leg],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_cyber_leg_l = {
    armor_name_str: 'Cyber leg (L)',
    ev_str: 0,
    humanity_cost_str: 4,
    sp_str: 4,
    covered_parts_str: [body_part_l_leg],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_torso_plate = {
    armor_name_str: 'Torso plate',
    ev_str: 0,
    humanity_cost_str: 4,
    sp_str: 25,
    covered_parts_str: [body_part_body],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_MID
}

generic_face_plate = {
    armor_name_str: 'Face plate',
    ev_str: 0,
    humanity_cost_str: 3,
    sp_str: 10,
    covered_parts_str: [body_part_head],
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_MID
}

#generic chrome

chrome_name_str = 'chromeName'
chrome_descr_str = 'chromeDescr'

generic_chip_slot = {
    chrome_name_str: 'Chip slot',
    chrome_descr_str: 'Allow using data chips',
    humanity_cost_str: 3,
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_smart_gun_link = {
    chrome_name_str: 'Smart gun link',
    chrome_descr_str: '+1 with smart gun link weapons',
    humanity_cost_str: 5,
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_cyber_contacts = {
    chrome_name_str: 'Color changing eyes',
    chrome_descr_str: 'Eyes change color',
    humanity_cost_str: 2,
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_nanosurgeons = {
    chrome_name_str: 'Nanosurgeons',
    chrome_descr_str: 'Doubles healing rate',
    humanity_cost_str: 5,
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_HIGH
}

generic_infra_red = {
    chrome_name_str: 'Infrared',
    chrome_descr_str: 'Allow seeing in dark',
    humanity_cost_str: 6,
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}

generic_scrambler = {
    chrome_name_str: 'Scrambler',
    chrome_descr_str: 'Mess with near by wireless communications',
    humanity_cost_str: 5,
    atr_bonuses_str: [],
    skill_bonuses_str: [],
    tier_str: GEAR_TIER_COMMON
}
