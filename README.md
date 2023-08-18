# Cyberpunk 2020 Referee tool 

## In progress

The goal of this project is to have a tool for the referee of Cyberpunk 2020 game
that helps to keep track of things in a better way than just pen and paper.
Different helpful things are e.g. quick rolls for characters 
(especially NPC characters and keeping track of them), 
keeping track of character statuses and equipment. This project also contains
some changes to the game logic from the original rules.

This is not a replacement for the original game's source books.

Cyberpunk 2020 is written by Mike Pondsmith and published by R. Talsorian Games.


## Feature examples:

- Get character info by name (health, SP, skills, weapons..)
- Stun checks based on damage
- Roll stun effect
- Damage calculation
    * First reduce character SP based on hit location
    * Reduce damage by modifier
    * Calculate AP attack effects in some manner
- Determine random hit locations
- Fetch character info from DB
- Keep track of combat sequence order for one combat session
- Roll skill checks for character
- Add reputation for character
- Add some notable events and list them
- Medical check rolls
- Quick notice checks
  * Add characters to quick notice check table
  * With one command, see if they clear some awareness check
- Attack rolls (completely automated for guns for the most part or give manual rolls)
  * Single
  * Burst
  * Full auto
  * Suppressive fire save check
  * Melee
- Add weapons (can be chrome, included in weapons), gear and chrome
    * For chrome, reduce humanity and empathy automatically

# Setup

* Install python 3.10+
  * Python dependencies:
    - colorama
    - psycopg2
    - Flask
    - Flask-Cors
    
* NPM for the Web UI

After setting up the PSQL database, run the following migration scripts:
  * `init.sql`
  * `create_schema_tables.sql`
  * `add_basic_skills.sql`
  * `grant_access.sql`

## secrets.json in /src for (PSQL) db config:
```
{
    "DB_HOST": "<host>",
    "DB_SCHEMA": "<db_schema>", //a need to update migration script(s) if changed..
    "DB_NAME": "<db_name>",
    "DB_USER": "<db_user>",
    "DB_PASSWORD": "<db_user_pw>"
}
```

# Usage

**Start terminal version:**
* ``\src $ python main.py``

**Start Web UI:**
  * Backend: ``\src $ flask --app net/app run``
  * NET: ``\ui $ npm start``
  * Go to `http://localhost:8000/`
  