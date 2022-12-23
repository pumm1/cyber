BEGIN;

CREATE TEMPORARY table t_char AS (
    select  currval('cyberpunk.characters_id_seq') + 1 as char_id
);

INSERT INTO cyberpunk.characters
    (name, role, body_type_modifier, special_ability, atr_int, atr_ref, atr_cool,
    atr_ma, atr_attr, atr_body, atr_luck, atr_emp, atr_tech)
VALUES ('Test', 'Solo', 'average', 6, 9, 9, 8, 8, 7, 8, 7, 5, 4);

INSERT INTO cyberpunk.character_skills (character_id, skill, skill_value, attribute)
SELECT t.char_id, 'melee', 5, 'REF' FROM t_char t;

INSERT INTO cyberpunk.character_skills (character_id, skill, skill_value, attribute)
SELECT t.char_id, 'handgun', 3, 'REF' FROM t_char t;

INSERT INTO cyberpunk.character_skills (character_id, skill, skill_value, attribute)
SELECT t.char_id, 'awareness', 3, 'INT' FROM t_char t;

INSERT INTO cyberpunk.character_skills (character_id, skill, skill_value, attribute)
SELECT t.char_id, 'interrogation', 3, 'COOL' FROM t_char t;

INSERT INTO cyberpunk.character_skills (character_id, skill, skill_value, attribute)
SELECT t.char_id, 'personal grooming', 3, 'ATTR' FROM t_char t;


DROP TABLE t_char;

COMMIT;
