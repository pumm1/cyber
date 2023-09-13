BEGIN;

CREATE TABLE cyberpunk.system_version (version INTEGER NOT NULL);

ALTER TABLE cyberpunk.characters ADD COLUMN emp_max INTEGER;

UPDATE cyberpunk.characters SET emp_max = 7; --some reasonable default for existing characters

ALTER TABLE cyberpunk.characters ALTER COLUMN emp_max SET NOT NULL;

INSERT INTO cyberpunk.system_version (version) VALUES (1);

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 1)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 1';
    END IF;
END $$;

COMMIT;
