SELECT 'Running init';

do
$$
begin
  if NOT EXISTS (SELECT * FROM pg_user WHERE usename = 'cyber') then
     CREATE USER cyber WITH password 'cyber1';
  end if;
end
$$
;

CREATE SCHEMA cyberpunk AUTHORIZATION cyber;
