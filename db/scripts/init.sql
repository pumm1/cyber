create user cyber with password 'cyber1';

create schema cyberpunk authorization cyber;

grant select on all tables in schema cyberpunk to cyber;
grant USAGE on SCHEMA cyberpunk to cyber ;
grant select, insert, update, delete on all tables in schema cyberpunk to cyber;
GRANT USAGE, SELECT ON SEQUENCE cyberpunk.characters_id_seq TO cyber;
