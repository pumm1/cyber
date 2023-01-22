from gameHelper import INT, REF, TECH, COOL, ATTR, MA, BODY, LUCK, EMP, BODY_TYPE_MOD


class Bonus:
    def __init__(self, atr_row, skill_bonuses):
        self.attributes = {
            INT: atr_row['atr_int'],
            REF: atr_row['atr_ref'],
            TECH: atr_row['atr_tech'],
            COOL: atr_row['atr_ref'],
            ATTR: atr_row['atr_attr'],
            MA: atr_row['atr_ma'],
            BODY: atr_row['atr_body'],
            LUCK: atr_row['atr_luck'],
            EMP: atr_row['atr_emp'],
            BODY_TYPE_MOD: atr_row['body_type_modifier']
        }
        self.skills = skill_bonuses
