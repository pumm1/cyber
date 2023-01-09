# Cyberpunk 2020 Referee tool 

## In progress

Basic idea for this project is to have some kind of tool for
the referee of Cyberpunk 2020 game to keep track of things
in easier way, roll results/effects quickly and
have some quick way to check info on e.g. skills.

## Features:

- Get character info by name (health, SP, skills, weapons..)
- Stun checks based on damage
- Roll stun effect
- Damage calculation
    * First reduce character SP based on hit location
    * Reduce damage by modifier
- Determine hit locations
- Fetch character info from DB
- Keep track of combat sequence order for one combat session
- Roll skill checks for character
- Add reputation for character
- Add some notable events and list them
- Medical check rolls
- Attack rolls (completely automated for guns for the most part)
  * Single
  * Burst
  * Full auto
  * Suppressive fire save check
  * Melee
- Add weapons (can be chrome, included in weapons), gear and chrome
    * For chrome, reduce humanity and empathy automatically

## TODO:
- Damage effect for AP 
- Healing logic updates for e.g. drugs and some better healing technologies

## secrets.json in src for db config:
```
{
    "DB_HOST": "<host>",
    "DB_SCHEMA": "<db_schema>,
    "DB_NAME": "<db_name>",
    "DB_USER": "<db_user>",
    "DB_PASSWORD": "<db_user_pw>",
}
```