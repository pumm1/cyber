import dice
import combat
from character import Character
import cyberdao as DAO
import game

#TODO:
#tallenna hahmo kantaan
#hae hahmo kannasta
#päivitä hahmoa
#rollaa osumakohtaa

#test_file = 'testChar.json'
#test_char = Character(test_file)

#awareness = test_char.findSkill('awareness')
#pooping = test_char.findSkill('pooping')

#roll_awareness = test_char.rollSkill('awareness', 0)

# print(f'... name: {test_char.name} '
#       f'\n... role: {test_char.role} '
#       f'\n... attributes: {test_char.attributes}'
#       f'\n... skills: {test_char.skills}'
#       f'\n... find skill awareness: {awareness}'
#       f'\n... find pooping: {pooping}'
#       f'\n... roll awareness: {roll_awareness}')

# combat.stunCheck(test_char)
# combat.stunCheck(test_char)
# combat.stunCheck(test_char)
# print('*************')
# combat.damageCharacter(test_char, 1)
# combat.damageCharacter(test_char, 5)
# combat.damageCharacter(test_char, 12)

char = DAO.getCharacterByName('Test')

if char is None:
    print('Not found')
else:
    print(f'character: {char.name}, atrributes: {char.attributes}, skills: {char.skills}')
    combat.stunCheckToBeat(char.dmg_taken, char.attributes['BODY'])
    char.takeDmg(39)

    combat.stunCheckToBeat(char.dmg_taken, char.attributes['BODY'])
    # DAO.getAllCharacters()

game.start()
