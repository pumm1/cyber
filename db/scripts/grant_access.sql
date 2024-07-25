--modify depending on your setup and users
SELECT 'Running Grant access';
grant select on all tables in schema cyberpunk to cyber;
grant USAGE on SCHEMA cyberpunk to cyber ;
grant select, insert, update, delete on all tables in schema cyberpunk to cyber;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA cyberpunk TO cyber;
