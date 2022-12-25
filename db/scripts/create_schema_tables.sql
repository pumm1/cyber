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
    atr_tech integer not null,
    dmg_taken integer not null,
    humanity integer not null
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
    character_id bigint not null UNIQUE,
    initiative integer not null,
    current boolean not null
);

alter table cyberpunk.combat_session
    add constraint combat_session__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);


create table cyberpunk.skills(
    id bigserial not null primary key,
    skill varchar not null,
    attribute varchar not null,
    description varchar not null
);

create table cyberpunk.character_reputation(
    character_id bigint not null,
    known_for varchar not null,
    rep_level integer not null
);

alter table cyberpunk.character_reputation
    add constraint character_reputation__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);

create table cyberpunk.character_sp(
    character_id bigint not null UNIQUE,
    head integer not null,
    body integer not null,
    r_arm integer not null,
    l_arm integer not null,
    r_leg integer not null,
    l_leg integer not null
);

alter table cyberpunk.character_sp
    add constraint character_sp__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);


create table cyberpunk.character_armor(
    character_id bigint not null,
    item varchar not null,
    sp integer not null,
    body_parts varchar[] not null
);

alter table cyberpunk.character_armor
    add constraint character_armor__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);


create type cyberpunk.weapon_type as enum ('melee', 'handgun', 'smg', 'shotgun', 'rifle', 'throwing');

create table cyberpunk.character_weapons(
    id bigserial not null PRIMARY KEY,
    character_id bigint not null,
    item varchar not null,
    weapon_type cyberpunk.weapon_type not null,
    is_chrome boolean not null,
    dice_number integer not null,
    dice_dmg integer not null,
    dmg_bonus integer not null,
    range integer not null,
    rof integer not null,
    clip_size integer not null,
    shots_left integer not null,
);

alter table cyberpunk.character_weapons
    add constraint character_weapon__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);

create table cyberpunk.character_chrome(
    id bigserial not null PRIMARY KEY,
    humanity_cost integer not null,
    character_id bigint not null,
    item varchar not null,
    description varchar not null
);

alter table cyberpunk.character_chrome
    add constraint character_weapon__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);

create table cyberpunk.events(
     id bigserial not null PRIMARY KEY,
    event varchar not null
);

COMMIT;