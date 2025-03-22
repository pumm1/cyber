from src.body import resolve_btm_from_body
from src.bodytypes import meleeDmgBonusByBodyType

def test_btm():
    assert resolve_btm_from_body(1) == 0
    assert resolve_btm_from_body(3) == 1
    assert resolve_btm_from_body(4) == 1
    assert resolve_btm_from_body(6) == 2
    assert resolve_btm_from_body(8) == 3
    assert resolve_btm_from_body(10) == 4
    assert resolve_btm_from_body(20) == 5

def test_melee_dmg_bonus():
    assert meleeDmgBonusByBodyType(1) == -2
    assert meleeDmgBonusByBodyType(3) == -1
    assert meleeDmgBonusByBodyType(4) == -1
    assert meleeDmgBonusByBodyType(6) == 0
    assert meleeDmgBonusByBodyType(8) == 1
    assert meleeDmgBonusByBodyType(10) == 2
    assert meleeDmgBonusByBodyType(11) == 4
    assert meleeDmgBonusByBodyType(14) == 6
    assert meleeDmgBonusByBodyType(20) == 8
