import cyberdao as DAO
from src import dice


def printSkillInfo(skills):
    for s in skills:
        skillInfo = skills[s]
        print(f"({s}) {skillInfo['skill']} [{skillInfo['attribute']}]: {skillInfo['description']}")


def rollCharacterSkill(name, skill_name):
    character = DAO.getCharacterByName(name)
    roll = 0
    skill = [s for s in character.skills if s.skill == skill_name]
    if len(skill) > 0:
        char_skill = skill[0]
        char_skill_lvl = char_skill.lvl
        skill_atr = char_skill.attribute
        atr_bonus = character.attributes[skill_atr]
        roll = dice.rollWithCrit() + char_skill_lvl + atr_bonus
    else:
        roll = dice.rollWithCrit()

    print(f'{name} rolled {roll} for {skill_name}')


def printCharSkillInfo(skills):
    print(f'... skills : {skills}')
    for s in skills:
        print(f'... skill: {s}')
        (atr, lvl) = skills[s]
        print(f"{s} ({atr}, {lvl})")
def listSkillsByAttribute(atr: str):
    atr_skills = skillsByAttribute(atr)
    printSkillInfo(atr_skills)

def findSkillsByString(string: str):
    skills = DAO.skillsByFuzzyLogic(string)
    printSkillInfo(skills)

def listAllSkills():
    all_skills = allSkills()
    printSkillInfo(all_skills)

def addCharacterSkill(name, skill_id, skill_level):
    character = DAO.getCharacterByName(name)
    if character is not None:
        skill = DAO.getSkillById(skill_id)
        if skill is not None:
            DAO.addCharacterSkill(character.id, skill, skill_level)
            print(f"Skill {skill['skill']} ({skill_level}) added for {name}")
        else:
            print(f'Skill not found by id ({skill_id})')
    else:
        print(f'{character} Not found')


def printCharacterSkills(name):
    skills = characterSkills(name)
    printCharSkillInfo(skills)


def characterSkills(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        skills = DAO.getCharacterSkillsById(character.id)
        return skills
    else:
        print(f'{character} Not found')
        return list()

def allSkills():
    skills = DAO.listSkills()
    return skills

def skillsByAttribute(atr):
    skills = DAO.listSkillsByAttribute(atr)
    return skills