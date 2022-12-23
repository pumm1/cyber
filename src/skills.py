import cyberdao as DAO


def printSkillInfo(skills):
    for s in skills:
        skillInfo = skills[s]
        print(f"({s}) {skillInfo['skill']} [{skillInfo['attribute']}]: {skillInfo['description']}")

def printCharSkillInfo(skills):
    for s in skills:
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
        return dict([])

def allSkills():
    skills = DAO.listSkills()
    return skills

def skillsByAttribute(atr):
    skills = DAO.listSkillsByAttribute(atr)
    return skills