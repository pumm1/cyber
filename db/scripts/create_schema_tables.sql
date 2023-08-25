BEGIN;

CREATE TABLE cyberpunk.characters(
    id BIGSERIAL not null primary key,
    name varchar not null,
    role varchar not null,
    special_ability integer not null,
    body_type_modifier integer not null,
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
    skill_id bigint not null,
    skill_lvl integer not null,
    CONSTRAINT unique_char_skill UNIQUE (character_id, skill_id)
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
    head_max integer not null,
    body integer not null,
    body_max integer not null,
    r_arm integer not null,
    r_arm_max integer not null,
    l_arm integer not null,
    l_arm_max integer not null,
    r_leg integer not null,
    r_leg_max integer not null,
    l_leg integer not null,
    l_leg_max integer not null
);

alter table cyberpunk.character_sp
    add constraint character_sp__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);


create table cyberpunk.character_armor(
    id bigserial not null primary key,
    character_id bigint not null,
    item varchar not null,
    sp integer not null,
    body_parts varchar[] not null,
    ev integer not null,
    item_bonus_id bigint
);

alter table cyberpunk.character_armor
    add constraint character_armor__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);


create type cyberpunk.weapon_type as enum ('melee', 'handgun', 'smg', 'shotgun', 'rifle', 'throwing', 'heavy');

create type cyberpunk.concealability as enum ('P', 'J', 'L', 'N');

create type cyberpunk.reliability as enum ('VR', 'ST', 'UR');

create table cyberpunk.character_weapons(
    id bigserial not null PRIMARY KEY,
    character_id bigint not null,
    item varchar not null,
    weapon_type cyberpunk.weapon_type not null,
    wa integer not null,
    con cyberpunk.concealability not null,
    is_chrome boolean not null,
    dice_number integer not null,
    dice_dmg integer not null,
    divide_by integer not null
    dmg_bonus integer not null,
    range integer not null,
    effect_radius integer not null,
    rof integer not null,
    clip_size integer not null,
    shots_left integer not null,
    reliability cyberpunk.reliability not null,
    weight integer not null default 3,
    item_bonus_id bigint
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
    description varchar not null,
    item_bonus_id bigint
);

alter table cyberpunk.character_chrome
    add constraint character_chrome__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);

create table cyberpunk.events(
     id bigserial not null PRIMARY KEY,
     event varchar not null
);

create table cyberpunk.character_statuses(
    id bigserial not null primary key,
    character_id bigint not null,
    status varchar not null,
    effect varchar not null
);

create table cyberpunk.character_notice_quick_checks(
    character_id bigint not null
);

alter table cyberpunk.character_notice_quick_checks
    add constraint character_notice__character_fk
        foreign key(character_id)
        references cyberpunk.characters(id);

create table cyberpunk.item_atr_bonuses(
    id bigserial not null primary key,
    atr_int integer not null DEFAULT 0,
    atr_ref integer not null DEFAULT 0,
    atr_cool integer not null DEFAULT 0,
    atr_ma integer not null DEFAULT 0,
    atr_attr integer not null DEFAULT 0,
    atr_body integer not null DEFAULT 0,
    atr_luck integer not null DEFAULT 0,
    atr_emp integer not null DEFAULT 0,
    atr_tech integer not null DEFAULT 0,
    body_type_modifier integer not null DEFAULT 0
);


create table cyberpunk.item_bonuses(
    id bigserial not null PRIMARY KEY,
    item_atr_id bigint not null
);

alter table cyberpunk.item_bonuses
    add constraint item_bonus__item_atr_fk
        foreign key(item_atr_id)
        references cyberpunk.item_atr_bonuses(id);

create table cyberpunk.item_skill_bonus(
    item_bonus_id bigint not null,
    skill_id bigint not null,
    skill_bonus integer not null
);


alter table cyberpunk.item_skill_bonus
    add constraint item_skill_bonus__skill_fk
        foreign key(skill_id)
        references cyberpunk.skills(id);

alter table cyberpunk.item_skill_bonus
    add constraint item_skill_bonus__item_bonus_fk
        foreign key(item_bonus_id)
        references cyberpunk.item_bonuses(id);


CREATE TABLE cyberpunk.statuses(
    id bigserial not null primary key,
    status_name varchar not null,
    description varchar not null,
    item_atr_id bigint not null
);

alter table cyberpunk.statuses
    add constraint status__item_atr_id_fk
        foreign key(item_atr_id)
        references cyberpunk.item_atr_bonuses(id);

ALTER TABLE cyberpunk.characters
ADD COLUMN ip INTEGER NOT NULL DEFAULT 0;

ALTER TABLE cyberpunk.characters
ALTER COLUMN ip DROP DEFAULT;

ALTER TABLE cyberpunk.character_armor
RENAME COLUMN id TO armor_id;

ALTER TABLE cyberpunk.characters
ADD COLUMN initiative_bonus integer NOT NULL DEFAULT 0;

ALTER TABLE cyberpunk.item_atr_bonuses
ADD COLUMN initiative_bonus integer NOT NULL DEFAULT 0;

ALTER TABLE cyberpunk.characters
ADD COLUMN money integer NOT NULL DEFAULT 0;

ALTER TABLE cyberpunk.character_chrome
RENAME COLUMN id TO chrome_id;

COMMIT;
