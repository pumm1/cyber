from src.body import resolve_btm_from_body

def test_btm():
    assert resolve_btm_from_body(1) == 0
    assert resolve_btm_from_body(3) == 1
    assert resolve_btm_from_body(4) == 1
    assert resolve_btm_from_body(6) == 2
    assert resolve_btm_from_body(8) == 3
    assert resolve_btm_from_body(10) == 4
    assert resolve_btm_from_body(20) == 5
