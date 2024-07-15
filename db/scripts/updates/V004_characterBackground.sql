BEGIN;
SELECT 'Running update V004';

UPDATE cyberpunk.system_version SET version = 4 WHERE version = 3;

ALTER TABLE cyberpunk.characters ADD COLUMN background VARCHAR;

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 4)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 3';
    END IF;
END $$;

COMMIT;
