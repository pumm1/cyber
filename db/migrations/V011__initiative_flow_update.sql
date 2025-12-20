BEGIN;

ALTER TABLE cyberpunk.combat_session
    ALTER COLUMN character_id DROP NOT NULL,
    ALTER COLUMN initiative DROP NOT NULL,
    ADD COLUMN temp_character VARCHAR;

UPDATE cyberpunk.system_version SET version = 8 WHERE version = 7;

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 8)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 8';
    END IF;
END $$;

COMMIT;
