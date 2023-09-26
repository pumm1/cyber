import { useState, useEffect } from "react"
import { getCharacter , Character, listSkills, Log, Attributes, CharacterSP, Skill, Initiative, CharacterShort, listCharacters, sortedCharacters, deleteCharacter} from './CyberClient'
import './SearchCharacter.css'
import React from "react"
import CharacterSheet from "./CharacterSheet"
import Hideable from "./Hideable"

const initialAttributes: Attributes = {
    ATTR: 1,
    BODY: 1,
    COOL: 1,
    EMP: 1,
    INT: 1,
    LUCK: 1,
    MA: 1,
    REF: 1,
    TECH: 1,
}

const initialSp: CharacterSP = {
    head: 0,
    body: 0,
    r_arm: 0,
    l_arm: 0,
    r_leg: 0,
    l_leg: 0
}

const characterToCreate: Character = {
    id: -1,
    role: '',
    name: '',
    specialAbility: '',
    specialAbilityLvl: 0,
    bodyType: 'average',
    btm: 0,
    attributes: initialAttributes,
    woundState: 'No damage',
    dmgTaken: 0,
    ip: 0,
    armor: [],
    skills: [],
    weapons: [],
    chrome: [],
    sp: initialSp,
    reputation: 0,
    humanity: initialAttributes.EMP * 10,
    money: 0
}

interface SearchCharacterProps {
    initiatives: Initiative[]
    updateLogs: (s: Log[]) => void
}

interface ListCharactersProps {
    characters: CharacterShort[]
    setCharacterById: (i: number) => Promise<void>
    updateLogs: (l: Log[]) => void
    setAllCharacters: (c: CharacterShort[]) => void
}

const ListCharacters = ({characters, setCharacterById, updateLogs, setAllCharacters}: ListCharactersProps) => {
    const [nameFilter, setNameFilter] = useState('')
    const charactersSorted = sortedCharacters(characters)
    const filteredCharacters = 
        nameFilter.length > 0 ? 
            charactersSorted.filter(c => c.name.toLocaleLowerCase().startsWith(nameFilter)) 
            : charactersSorted
    const removeCharacter = (charId: number) => 
        deleteCharacter({charId})

    const characterTable = 
        <>
            <input placeholder='Search by...' className='filter' value={nameFilter} onChange={e => setNameFilter(e.target.value)}/>
            <table>
                    <tr>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Show</th>
                    <th>Remove</th>
                </tr>
                {filteredCharacters.map(c => 
                    <tr>
                        <td>{c.name}</td>
                        <td>{c.role}</td>
                        <td>
                            <button onClick={() => setCharacterById(c.id)}>Show</button>
                        </td>
                        <td>
                        <button onClick={() => {
                                removeCharacter(c.id).then(updateLogs).then(() => listCharacters().then(setAllCharacters))
                            }}>Delete</button>  
                        </td>
                    </tr>    
                )}
            </table>
        </>
    return(
        <div className='listCharacters'>
            <Hideable text='characters' props={characterTable} />
        </div>
    )
}

const SearchOrCreateCharacter = ({updateLogs, initiatives}: SearchCharacterProps) => {
    const [characterEditable, setCharacterEditable] = useState(false)
    const [character, setCharacter] = useState<undefined | null | Character>(undefined)
    const [allSkills, setAllSkills] = useState<Skill[] | undefined>(undefined)
    const [allCharacters, setAllCharacters] = useState<CharacterShort[] | undefined>(undefined)

    useEffect(() => {
        listSkills().then(setAllSkills).then(() => 
            listCharacters().then(setAllCharacters)
        )
        
    }, [])

    const updateCharacter = (i: number): Promise<void> => {
        setCharacterEditable(false)
        return getCharacter(i).then(setCharacter)
    }


    const createCharacter = () => {
        setCharacter(characterToCreate)
        setCharacterEditable(true)
    }

    const setCharacterFn = (i: number) => 
         getCharacter(i).then(char => {
            setCharacter(char)
            setCharacterEditable(false)
        })

    const allowAddingToInitiative = character ? !initiatives.find(i => i.charId === character.id) : false

    const updateCharacterList = () => 
        listCharacters().then(setAllCharacters)
    
    //why using form breaks this in backend?
    return(
        <>
            <ListCharacters characters={allCharacters ?? []} setCharacterById={setCharacterFn} updateLogs={updateLogs} setAllCharacters={setAllCharacters}/>
            <div className="search">
                <button className='searchOrCreate' onClick={() => createCharacter()}>Create</button>
                {character && <button className='searchOrCreate' onClick={() => setCharacter(undefined)}>Hide character</button>}
            </div>
            {!!character &&
                 <div><CharacterSheet updateCharacterList={updateCharacterList} allowAddingToInitiative={allowAddingToInitiative} editCharacter={setCharacter} edit={characterEditable} updateCharacter={updateCharacter} character={character} allSkills={allSkills} updateLogs={updateLogs}/></div>
            }
        </>
    )
}

export default SearchOrCreateCharacter
