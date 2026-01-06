BEGIN;

CREATE TABLE cyberpunk.campaign_mind_map_nodes (
    id VARCHAR NOT NULL PRIMARY KEY,
    campaign_id BIGINT NOT NULL,
    title VARCHAR NOT NULL,
    info VARCHAR NOT NULL,
    pos_x INTEGER NOT NULL,
    pos_y INTEGER NOT NULL,
    CONSTRAINT fk_campaign_id
      FOREIGN KEY (campaign_id)
        REFERENCES cyberpunk.campaigns (id)
);

CREATE TABLE cyberpunk.mind_map_node_connections (
    node_from VARCHAR NOT NULL,
    node_to VARCHAR NOT NULL,
    CONSTRAINT fk_mind_map_node_from
      FOREIGN KEY (node_from)
        REFERENCES cyberpunk.campaign_mind_map_nodes (id),
    CONSTRAINT fk_mind_map_node_to
      FOREIGN KEY (node_to)
        REFERENCES cyberpunk.campaign_mind_map_nodes (id)
);

UPDATE cyberpunk.system_version SET version = 7 WHERE version = 6;

DO $$
    BEGIN
    IF EXISTS (SELECT version FROM cyberpunk.system_version WHERE version = 7)
    THEN RAISE INFO 'Version is set right';
    ELSE
    RAISE EXCEPTION 'Version wrong, expected 7';
    END IF;
END $$;

COMMIT;
