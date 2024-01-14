BEGIN;

CREATE TABLE cyberpunk.campaigns(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    name VARCHAR NOT NULL,
    info VARCHAR
);

CREATE TABLE cyberpunk.gigs(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    campaign_id BIGINT NOT NULL,
    name VARCHAR NOT NULL,
    is_completed BOOLEAN NOT NULL,
    info VARCHAR
);

ALTER TABLE cyberpunk.gigs
ADD CONSTRAINT gig_campaign__fk FOREIGN KEY (campaign_id) REFERENCES cyberpunk.campaigns (id);

CREATE TABLE cyberpunk.gig_characters(
    gig_id BIGINT NOT NULL,
    character_id BIGINT NOT NULL,
    info VARCHAR
);

ALTER TABLE cyberpunk.gig_characters
ADD CONSTRAINT gig_characters_gig_id__fk FOREIGN KEY (gig_id) REFERENCES cyberpunk.gigs (id);

ALTER TABLE cyberpunk.gig_characters
ADD CONSTRAINT gig_characters_characer_id__fk FOREIGN KEY (character_id) REFERENCES cyberpunk.characters (id);

CREATE TABLE cyberpunk.events(
    id BIGSERIAL PRIMARY KEY NOT NULL,
    campaign_id BIGINT NOT NULL,
    info VARCHAR
);

ALTER TABLE cyberpunk.events
ADD CONSTRAINT event_campaing_id__fk FOREIGN KEY (campaign_id) REFERENCES cyberpunk.campaigns (id);

CREATE TABLE cyberpunk.event_characters(
    event_id BIGINT NOT NULL,
    character_id BIGINT NOT NULL,
    info VARCHAR
);


ALTER TABLE cyberpunk.event_characters
ADD CONSTRAINT event_characters_event_id__fk FOREIGN KEY (event_id) REFERENCES cyberpunk.events (id);

ALTER TABLE cyberpunk.event_characters
ADD CONSTRAINT event_characters_character_id__fk FOREIGN KEY (character_id) REFERENCES cyberpunk.characters (id);

UPDATE cyberpunk.system_version SET version = 2 WHERE version = 1;

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 2)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 2';
    END IF;
END $$;


COMMIT;
