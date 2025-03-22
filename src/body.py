def resolve_btm_from_body(body: int) -> int:
    btm = 0
    if 3 <= body <= 4:
        btm = 1
    elif 5 <= body <= 7:
        btm = 2
    elif 8 <= body <= 9:
        btm = 3
    elif body == 10:
        btm = 4
    elif body > 10:
        btm = 5

    return btm
