import cyberdao as DAO

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