import pytest

from src.combat import resolveDmgPassingSP, resolveDmgDoneToCharacter, resolveApDmg, resolveFullAutoRangeBonus, \
    resolveFullAutoTargetHits
from src.gameHelper import point_blank_range_str, close_range_str, medium_range_str


def testDmgNotPassingSP():
    dmg_to_character, armor_damaged = resolveDmgPassingSP(10, 5)
    assert armor_damaged == False
    assert dmg_to_character == 0

    dmg_to_character, armor_damaged = resolveDmgPassingSP(10, 10)
    assert armor_damaged == False
    assert dmg_to_character == 0

def testDmgPassingSP():
    dmg_to_character, armor_damaged = resolveDmgPassingSP(10, 11)
    assert armor_damaged == True
    assert dmg_to_character == 1

    dmg_to_character, armor_damaged = resolveDmgPassingSP(10, 15)
    assert armor_damaged == True
    assert dmg_to_character == 5

def testDmgNotPassingSPWithAPHit():
    dmg_done = resolveApDmg(10, 4)
    assert dmg_done == 0
    dmg_done = resolveApDmg(10, 5)
    assert dmg_done == 0

def testDmgPassingSpWithAPHit():
    dmg_done = resolveApDmg(10, 6)
    assert dmg_done == 1
    dmg_done = resolveApDmg(8, 6)
    assert dmg_done == 1
    dmg_done = resolveApDmg(8, 10)
    assert dmg_done == 3

def testDmgDoneNotToCharacter():
    total_dmg, body_part_destroyed = resolveDmgDoneToCharacter(2, 2)

    assert total_dmg == 0
    assert body_part_destroyed == False

def testDmgDoneToCharacter():
    total_dmg, body_part_destroyed = resolveDmgDoneToCharacter(4, 2)
    assert total_dmg == 2
    assert body_part_destroyed == False

    total_dmg, body_part_destroyed = resolveDmgDoneToCharacter(9, 2)
    assert total_dmg == 7
    assert body_part_destroyed == False

    total_dmg, body_part_destroyed = resolveDmgDoneToCharacter(10, 2)
    assert total_dmg == 8
    assert body_part_destroyed == True

def testFullAutoRangeBonus():
    bonus = resolveFullAutoRangeBonus(5, point_blank_range_str)
    assert bonus == 0
    bonus = resolveFullAutoRangeBonus(10, point_blank_range_str)
    assert bonus == 1
    bonus = resolveFullAutoRangeBonus(10, close_range_str)
    assert bonus == 1
    bonus = resolveFullAutoRangeBonus(10, medium_range_str)
    assert bonus == -1
    bonus = resolveFullAutoRangeBonus(20, medium_range_str)
    assert bonus == -2

def testFullAutoTargetHits():
    target_hit, num_of_hits = resolveFullAutoTargetHits(10, 15, 5)
    assert target_hit == False
    assert num_of_hits == 0

    target_hit, num_of_hits = resolveFullAutoTargetHits(15, 15, 5)
    assert target_hit == True
    assert num_of_hits == 1

    target_hit, num_of_hits = resolveFullAutoTargetHits(20, 15, 5)
    assert target_hit == True
    assert num_of_hits == 5

    target_hit, num_of_hits = resolveFullAutoTargetHits(25, 15, 5)
    assert target_hit == True
    assert num_of_hits == 5

    target_hit, num_of_hits = resolveFullAutoTargetHits(25, 15, 8)
    assert target_hit == True
    assert num_of_hits == 8
