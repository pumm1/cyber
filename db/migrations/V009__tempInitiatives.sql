BEGIN;

ALTER TABLE cyberpunk.combat_session
ADD COLUMN bonus_turns integer,
ADD COLUMN bonus_initiative integer;

UPDATE cyberpunk.system_version SET version = 6 WHERE version = 5;

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 6)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 6';
    END IF;
END $$;

COMMIT;
