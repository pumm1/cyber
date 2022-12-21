BEGIN;

CREATE TABLE cyberpunk.characters(
    id BIGSERIAL not null primary key primary key,
    name varchar not null,
    role varchar not null,
    special_ability integer not null,
    body_type_modifier varchar not null,
    atr_int integer not null,
    atr_ref integer not null,
    atr_cool integer not null,
    atr_ma integer not null,
    atr_attr integer not null,
    atr_body integer not null,
    atr_luck integer not null,
    atr_emp integer not null,
    atr_tech integer not null
);

CREATE TABLE cyberpunk.character_skills(
    character_id bigint not null,
    skill varchar not null,
    skill_value integer,
    attribute varchar not null,
    CONSTRAINT unique_char_skill UNIQUE (character_id, skill)
);

alter table cyberpunk.character_skills
    add constraint character_skill__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);

select nextval('cyberpunk.characters_id_seq');

create table cyberpunk.combat_session(
    character varchar not null,
    initiative integer not null,
    current boolean not null
);

create table cyberpunk.skills(
    id bigserial not null primary key,
    skill varchar not null,
    attribute varchar not null,
    description varchar not null
);

create table cyberpunk.character_reputation(
    character_id bigint not null,
    known_for varchar not null,
    reputation_value integer not null
);

COMMIT;