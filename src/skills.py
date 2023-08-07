from colorama import Fore, Style

import dice, cyberdao as DAO
from gameHelper import safeCastToInt, printGreenLine, coloredText, list_skills_helper_str
from src.logger import Log, log_pos, log_neg

skill_athletics = 'athletics'
skill_first_aid = 'first aid'

easy_check = 10
average_check = 15
difficult_check = 20
very_difficult_check = 25
nearly_impossible_check = 30

def difficultyCheckInfo():
    print(f"""Difficulty checks:
{coloredText(Fore.GREEN, "Easy")} ({easy_check}+)
Average ({average_check}+)
{coloredText(Fore.YELLOW, "Difficult")} ({difficult_check}+)
{coloredText(Fore.LIGHTRED_EX, "Very difficult")} ({very_difficult_check}+)
{coloredText(Fore.RED, "Nearly impossible")} ({nearly_impossible_check}+)""")


def skillBonusForSkill(skills, skill):
    skill_bonus = 0
    for s in skills:
        if s.skill == skill:
            print(f'Skill {skill} found (level = {s.lvl})')
            skill_bonus = s.lvl

    if skill_bonus == 0:
        print(f'{skill} not found in character skills')
    return skill_bonus

def printSkillInfo(skills):
    for s in skills:
        skillInfo = skills[s]
        print(f"({s}) {skillInfo['skill']} [{skillInfo['attribute']}]: {skillInfo['description']}")


def rollCharacterMeleeDef(name, roll):
    character = DAO.getCharacterByName(name)
    if character is not None:
        skill = DAO.getSkillByName('dodge/escape')
        if skill is not None:
            die_roll = safeCastToInt(roll)
            if die_roll <= 0:
                die_roll = dice.rollWithCrit(True)

            atr_bonus = character.attributes[skill['attribute']]

            char_dodge_skill = None
            for s in character.skills:
                if s.id == skill['id']:
                    char_dodge_skill = s
                    break
            char_dodge_lvl = 0
            if char_dodge_skill is not None:
                char_dodge_lvl = char_dodge_skill.lvl
            roll = die_roll + atr_bonus + char_dodge_lvl
            print(f"""(die roll = {die_roll} atr_bonus = {atr_bonus} dodge = {char_dodge_lvl})""")
            printGreenLine(f"Melee def total: {roll} (hopefully the attacker rolled lower..)")


def rollCharacterSkillById(id, skill_num, roll, modifier, added_luck):
    character = DAO.getCharacterById(id)
    return rollCharacterSkill(character, skill_num, roll, modifier, added_luck)


def rollCharactersKillByName(name, skill_num, roll, modifier):
    character = DAO.getCharacterByName(name)
    rollCharacterSkill(character, skill_num, roll, modifier, added_luck=None)


def rollCharacterSkill(character, skill_num, roll, modifier, added_luck):
    skill_name = ''
    roll_modifier = safeCastToInt(modifier)
    skill_id = safeCastToInt(skill_num)
    skill = DAO.getSkillById(skill_id)
    if skill is not None:
            skill_name = skill['skill']
    if character is not None:
        t_roll = safeCastToInt(roll)
        atr_bonus = 0
        char_skill_lvl = 0
        die_roll = 0
        if t_roll <= 0:
            if added_luck == None:
                added_luck = dice.handleLuck()
            die_roll = dice.rollWithCritAndGivenLuck(added_luck) + roll_modifier
        else:
            die_roll = t_roll + roll_modifier
        skill = [s for s in character.skills if s.skill == skill_name]
        if len(skill) > 0:
            char_skill = skill[0]
            char_skill_lvl = char_skill.lvl
            skill_atr = char_skill.attribute
            atr_bonus = character.attributes[skill_atr]
            roll = die_roll + char_skill_lvl + atr_bonus
        else:
            skill = DAO.getSkillByName(skill_name)
            if skill is not None:
                skill_atr = skill['attribute']
                atr_bonus = character.attributes[skill_atr]
                roll = die_roll + atr_bonus

        printGreenLine(f"""{character.name} rolled {roll} for {skill_name}""")
        print(f"""(die roll = {die_roll} atr_bonus = {atr_bonus} skill_level = {char_skill_lvl} modifier = {roll_modifier})""")
        return roll

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


def awarenessSkill():
    return DAO.skillByName('awareness')


def fetchAllSkils():
    skills = allSkills().values()
    return list(skills)

def listAllSkills():
    all_skills = allSkills()
    printSkillInfo(all_skills)

def udpateCharacterSkill(character, skill_id, lvl_up_amount) -> [Log]:
    event_logs = []
    t_skill = safeCastToInt(skill_id)
    if t_skill >= 0:
        if character is not None:
            if t_skill == 0:
                DAO.updateCharSpecial(character.id, lvl_up_amount)
                special_log = Log(f'{character.name} special updated (+{lvl_up_amount})', log_pos)
                event_logs.append(special_log.toJson())
            else:
                skill = DAO.getSkillById(skill_id)
                if skill is not None:
                    DAO.updateCharSkill(character.id, skill, lvl_up_amount)
                    skill_updated_log = Log(f"Skill {skill['skill']} (+{lvl_up_amount}) updated for {character.name}", log_pos)
                    event_logs.append(skill_updated_log.toJson())
                else:
                    not_found_log = Log(f'Skill not found by id ({skill_id})', log_neg)
                    event_logs.append(not_found_log.toJson())
    else:
        not_valid_skill_log = Log(f"'{skill_id}' not a valid skill id", log_neg)
        event_logs.append(not_valid_skill_log.toJson())

    return event_logs


def updateCharSkillById(char_id, skill_id, lvl_up_amount):
    character = DAO.getCharacterById(char_id)
    return udpateCharacterSkill(character, skill_id, lvl_up_amount)


def updateCharSkill(name, skill_id, lvl_up_amount):
    character = DAO.getCharacterByName(name)
    return udpateCharacterSkill(character, skill_id, lvl_up_amount)


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


def listSkills(command):
    match command:
        case[_]:
            listAllSkills()
        case[_, 'atr', atr]:
            listSkillsByAttribute(atr)
        case[_, 'fuzzy', str]:
            findSkillsByString(str)
        case[_, 'char', name]:
            printCharacterSkills(name)
        case _:
            print(list_skills_helper_str)
