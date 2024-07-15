# Cyberpunk 2020 Referee tool 

## In progress

The goal of this project is to have a tool for the referee of Cyberpunk 2020 game
that helps to keep track of things in a better way than just pen and paper. Different helpful 
things are e.g. quick rolls for characters (especially NPC characters and keeping track of them), 
keeping track of character statuses and equipment. 

This project also contains some changes to the game logic from the original rules - 
mostly to simplify some things for the tool itself. I've tried to make things so that a referee can
use their own judgement to decide how to change e.g. character health, improvement points,
level up character skills etc., while also trying to keep track of some things automatically
based on other factors (e.g. character taking hit to a leg and seeing the result on SP/health 
right away or seeing if character gets stunned).

This is not a replacement for the original game's source books.

Cyberpunk 2020 is written by Mike Pondsmith and published by R. Talsorian Games.

## Example images
### Initiatives
![image](https://github.com/pumm1/cyber/assets/22749461/0ddd5ffb-2a65-4b4f-b776-e3ff09aa7706)
### Showing character info
![image](https://github.com/pumm1/cyber/assets/22749461/e614dab3-3288-4fae-8fe3-91c44c947879)
### Skills
![image](https://github.com/pumm1/cyber/assets/22749461/03a51e62-c5da-4b62-bc8b-7ee9ac68eaa2)

### Equipment and chrome
![image](https://github.com/pumm1/cyber/assets/22749461/641c309c-cfd5-4e5b-befa-e5e632075336)



## Feature examples:

- Create characters by hand or generate them randomly
- Get character info by name (health, SP, skills, weapons..)
- Stun checks based on damage
- Roll stun effect
- Damage calculation
    * First reduce character SP based on hit location
    * Reduce damage by modifier
    * Calculate AP attack effects in some manner
- Determine random hit locations
- Keep track of combat sequence order for one combat session
- Roll skill checks for character
- Add reputation for character
- Add some notable events and list them for campaign
- Medical check rolls
  * Add characters to quick notice check table
  * With one command, see if they clear some awareness check
- Attack rolls (completely automated for guns for the most part or give manual rolls, some of these are not supported in the UI version yet)
  * Single
  * Burst
  * Full auto
  * Suppressive fire save check
  * Melee
- Add weapons (can be chrome, included in weapons), gear and chrome
    * For chrome, reduce humanity and empathy automatically

# Setup
## Docker setup (Easier quick setup)

- Make sure you have Docker installed
- Include `.env` file to root project
  - Example contents for `.env` file:
```
DATABASE_URL=postgresql://cyber:cyber1@db:5432/postgres
FLASK_APP=app.py
FLASK_RUN_HOST=0.0.0.0
DB_HOST=cyber_db
DB_PORT=5432
DB_NAME=postgres
DB_USER=cyber
DB_PASSWORD=cyber1
```
- Create and run container from the project root with `docker-compose up -d --build` (wait for `cyber_db`, `cyber_backend` and `cyber_ui` to be complete)
- In your browser go to `localhost:3000` to use the UI
- To stop the app, run `docker-compose stop` (to keep the data in your current container)
- To restart the app, run `docker-compose start`


## Manual setup (Easier to migrate data with updates, but more configuration needed)
* Install python 3.10+
  * You can use pip to install dependencies 
    * For windows one might need to run the following for psycopg: 
      * `pip install "psycopg[binary,pool]"`
  * Python dependencies:
    - colorama
    - psycopg
    - Flask
    - Flask-Cors
    
* NPM for the Web UI

After setting up the PSQL database, run the following migration scripts:
  * `init.sql`
  * `create_schema_tables.sql`
  * `add_basic_skills.sql`
  * `grant_access.sql`

Also run all the versioned update sql-scripts in order inside `updates` 
directory (`V001_..`, `V002_..`, etc.)

## secrets.json in /src for (PSQL) db config:
```
{
    "DB_HOST": "<host>", //most likely 127.0.0.1 for local setup
    "DB_SCHEMA": "cyberpunk", //need to update migration script(s) if changed..
    "DB_NAME": "<db_name>",
    "DB_USER": "cyber", //check init.sql and grant_access.sql for user or edit as you wish
    "DB_PASSWORD": "<db_user_pw>" //most likely cyber1 as in init.sql
}
```

# Usage

**Start Web UI:**
  * Backend: ``/src $ flask --app net/app run`` 
    * if you see the following in logs when trying to start backend,
    you can try to start from project root `/cyber`
    ``/cyber $ flask --app src/net/app.py run``.
    Behaviour might change a little depending on the OS you run this from - 
    first example was tested on Windows 10, the latter on Ubuntu.
    ```
    //the mentioned logs on start up
    db = secrets['DB_NAME']
    KeyError: 'DB_NAME'
    ```
  * NET: ``/ui $ npm start``
    * If that doesn't work, run first `npm install`
  * Go to `http://localhost:8000/`
  
**Start terminal version:**
* ``\src $ python main.py``
