BEGIN;
SELECT 'Running update V003';

CREATE TYPE cyberpunk.character_status_type AS ENUM(
 'Negative', 'Neutral', 'Positive'
);

ALTER TABLE cyberpunk.character_statuses
ADD COLUMN status_type cyberpunk.character_status_type;

UPDATE cyberpunk.character_statuses SET status_type = 'Neutral';

ALTER TABLE cyberpunk.character_statuses ALTER COLUMN status_type SET NOT NULL;

ALTER TABLE cyberpunk.character_statuses
ADD CONSTRAINT character_statuses_character_id__fk FOREIGN KEY (character_id) REFERENCES cyberpunk.characters (id);

UPDATE cyberpunk.system_version SET version = 3 WHERE version = 2;

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 3)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 3';
    END IF;
END $$;

COMMIT;
