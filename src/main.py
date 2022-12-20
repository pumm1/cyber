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
