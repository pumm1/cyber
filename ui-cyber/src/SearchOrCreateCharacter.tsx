import { useState, useEffect } from "react"
import { getCharacter , Character, listSkills, Log, Attributes, CharacterSP, Skill, Initiative, CharacterShort, listCharacters, sortedCharacters, deleteCharacter, AddToCombatReq, rollInitiative, addToCombat} from './CyberClient'
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
    updateInitiatives: () => Promise<void>
}

interface ListCharactersProps {
    characters: CharacterShort[]
    setCharacterById: (i: number) => Promise<void>
    updateLogs: (l: Log[]) => void
    setAllCharacters: (c: CharacterShort[]) => void
    initiatives: Initiative[]
    updateInitiatives: () => Promise<void>
    updateCharacterList: () => Promise<void>
}

interface CharacterListRowProps {
    character: CharacterShort
    setCharacterById: (i: number) => void
    addToCombatReq: (i: number, ini: number) => AddToCombatReq
    updateCharIni: (i: number, ini: number) => void
    removeCharacter: (i: number) => Promise<Log[]>
    updateLogs: (l: Log[]) => void
    updateCharacters: () => void
    updateInitiatives: () => void
    isAlreadyInCombat: (i: number) => boolean
}
const CharacterListRow = ({character: c, isAlreadyInCombat, setCharacterById, addToCombatReq, updateCharIni, removeCharacter, updateLogs, updateCharacters, updateInitiatives}: CharacterListRowProps) => {
    const [initiative, setInitiative] = useState<number | undefined>(undefined)

    return(
        <tr>
                        <td>{c.name}</td>
                        <td>{c.role}</td>
                        <td>
                            <span>
                                <input className='valueBox' type="text" onChange={e => setInitiative(parseInt(e.target.value))}/>
                                <button onClick={() => rollInitiative({charId: c.id, initiative}).then(i => updateCharIni(c.id, i))}>Roll</button> 
                            </span>
                           </td>
                        <td>{c.initiative ?? ''}</td>
                        <td>
                            <button onClick={() => c.initiative && addToCombat(addToCombatReq(c.id, c.initiative)).then(() => updateInitiatives())} disabled={!c.initiative || isAlreadyInCombat(c.id)}>
                                Add
                            </button></td>
                        <td>
                            <button onClick={() => setCharacterById(c.id)}>Show</button>
                        </td>
                        <td>
                        <button onClick={() => {
                                removeCharacter(c.id).then(updateLogs).then(() => updateCharacters())
                            }}>Delete</button>  
                        </td>
                    </tr>    
    )
}

const ListCharacters = ({characters, setCharacterById, updateLogs, setAllCharacters, initiatives, updateInitiatives, updateCharacterList}: ListCharactersProps) => {
    const [nameFilter, setNameFilter] = useState('')
    const charactersSorted = sortedCharacters(characters)
    const filteredCharacters = 
        nameFilter.length > 0 ? 
            charactersSorted.filter(c => c.name.toLocaleLowerCase().startsWith(nameFilter)) 
            : charactersSorted
    const removeCharacter = (charId: number) => 
        deleteCharacter({charId})

    const updateCharacters = () => 
        listCharacters().then(setAllCharacters)

    const addToCombatReq = (charId: number, initiative: number): AddToCombatReq => {
        return {
            charId,
            initiative
        }
    }

    const updateCharIni = (charId: number, init: number) => {
        const updatedCharacters = characters.map(c => {
            if (charId === c.id) {
                const res: CharacterShort = {initiative: init, ...c}
                console.log(`${init} and res ${JSON.stringify(res)}`)
                return res
            } else {
                return c
            }
        })

        setAllCharacters(updatedCharacters)
    }

    const isAlreadyInCombat = (charId: number): boolean =>
        !!initiatives.find(i => i.charId === charId)

    const characterTable = 
        <>
            <input placeholder='Search by...' className='filter' value={nameFilter} onChange={e => setNameFilter(e.target.value)}/>
            <button className='withLeftSpace' onClick={() => updateCharacterList()}>Reset</button>
            <table>
                    <tr>
                    <th>Name</th>
                    <th>Role</th>
                    <th>Roll ini.</th>
                    <th>Initiative</th>
                    <th>Add to combat</th>
                    <th>Show</th>
                    <th>Remove</th>
                </tr>
                {filteredCharacters.map(c => 
                    <CharacterListRow character={c} isAlreadyInCombat={isAlreadyInCombat} updateCharacters={updateCharacters} updateLogs={updateLogs} removeCharacter={removeCharacter} updateCharIni={updateCharIni} updateInitiatives={updateInitiatives} setCharacterById={setCharacterById} addToCombatReq={addToCombatReq}/>
                )}
            </table>
        </>
    return(
        <div className='listCharacters'>
            <Hideable text='characters' props={characterTable} />
        </div>
    )
}

const SearchOrCreateCharacter = ({updateLogs, initiatives, updateInitiatives}: SearchCharacterProps) => {
    const [characterEditable, setCharacterEditable] = useState(false)
    const [character, setCharacter] = useState<undefined | null | Character>(undefined)
    const [allSkills, setAllSkills] = useState<Skill[] | undefined>(undefined)
    const [allCharacters, setAllCharacters] = useState<CharacterShort[] | undefined>(undefined)

    const updateCharacterList = () => 
        listCharacters().then(setAllCharacters)

    useEffect(() => {
        listSkills().then(setAllSkills).then(() => 
            updateCharacterList()
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
    
    //why using form breaks this in backend?
    return(
        <>
            <ListCharacters updateCharacterList={updateCharacterList} updateInitiatives={updateInitiatives} initiatives={initiatives} characters={allCharacters ?? []} setCharacterById={setCharacterFn} updateLogs={updateLogs} setAllCharacters={setAllCharacters}/>
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