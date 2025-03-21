BEGIN;
SELECT 'Running update V005';

ALTER TABLE cyberpunk.characters
DROP COLUMN body_type_modifier; --this gets resolved dynamically

UPDATE cyberpunk.system_version SET version = 5 WHERE version = 4;

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 5)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 3';
    END IF;
END $$;

COMMIT;
