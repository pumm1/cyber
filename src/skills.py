from colorama import Fore, Style

from src.gameHelper import safeCastToInt, printGreenLine, coloredText, list_skills_helper_str, printRedLine, COOL, INT, REF
from src.character import Character
from src.logger import Log, log_pos, log_neg, log_event, log_neutral
from src.roles import roleSpecialAbility, solo, rocker, netrunner, media, nomad, fixer, cop, corp, techie, meditechie
from src.skill import SkillInfo

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


def character_special_atr_bonus_on_skill(character: Character) -> (int, str):
    role = character.role
    atr_bonus = 0
    atr = INT
    if role == solo:
        atr_bonus = 0
        atr = REF
    elif role == rocker:
        atr_bonus = character.attributes[COOL]
        atr = COOL
    elif role == netrunner:
        atr_bonus = character.attributes[INT]
        atr = INT
    elif role == media:
        atr_bonus = character.attributes[INT]
        atr = INT
    elif role == nomad:
        atr_bonus = character.attributes[INT]
        atr = INT
    elif role == fixer:
        atr_bonus = character.attributes[COOL]
        atr = COOL
    elif role == cop:
        atr_bonus = character.attributes[COOL]
        atr = COOL
    elif role == corp:
        atr_bonus = character.attributes[INT]
        atr = INT
    elif role == techie:
        atr_bonus = 0
        atr = INT
    elif role == meditechie:
        atr_bonus = 0
        atr = INT

    return (atr_bonus, atr)


def printCharSkillInfo(skills):
    if len(skills) > 0:
        for s in skills:
            (atr, lvl) = (s.attribute, s.lvl)
            print(f"{s.skill} - {lvl} [{atr}]")
    else:
        print(f'No skills found')
