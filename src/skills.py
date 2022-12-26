import dice, cyberdao as DAO
from gameHelper import safeCastToInt


def printSkillInfo(skills):
    for s in skills:
        skillInfo = skills[s]
        print(f"({s}) {skillInfo['skill']} [{skillInfo['attribute']}]: {skillInfo['description']}")


def rollCharacterSkill(name, skill_name, modifier):
    character = DAO.getCharacterByName(name)
    roll_modifier = safeCastToInt(modifier)
    if character is not None:
        roll = 0
        atr_bonus = 0
        char_skill_lvl = 0
        die_roll = dice.rollWithCrit()
        roll = die_roll + roll_modifier
        skill = [s for s in character.skills if s.skill == skill_name]
        if len(skill) > 0:
            char_skill = skill[0]
            char_skill_lvl = char_skill.lvl
            skill_atr = char_skill.attribute
            atr_bonus = character.attributes[skill_atr]
            roll = roll + char_skill_lvl + atr_bonus
        else:
            skill = DAO.getSkillByName(skill_name)
            if skill is not None:
                skill_atr = skill['attribute']
                atr_bonus = character.attributes[skill_atr]
                roll = roll + atr_bonus

        print(f"""{name} rolled {roll} for {skill_name}
(die roll = {die_roll} atr_bonus = {atr_bonus} skill_level = {char_skill_lvl} modifier = {roll_modifier})
""")


def printCharSkillInfo(skills):
    if len(skills) > 0:
        for s in skills:
            (atr, lvl) = (s.attribute, s.lvl)
            print(f"{s.skill} - {lvl} [{atr}]")
    else:
        print(f'No skills found')
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


def printCharacterSkills(name):
    skills = characterSkills(name)
    printCharSkillInfo(skills)


def characterSkills(name):
    character = DAO.getCharacterByName(name)
    if character is not None:
        skills = DAO.getCharacterSkillsById(character.id)
        return skills
    else:
        print(f'{name} Not found')
        return list()

def allSkills():
    skills = DAO.listSkills()
    return skills

def skillsByAttribute(atr):
    skills = DAO.listSkillsByAttribute(atr)
    return skills