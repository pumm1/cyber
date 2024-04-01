import { useState, useEffect } from "react"
import { getCharacter , Character, Log, Attributes, CharacterSP, Skill, Initiative, CharacterShort, listCharacters, sortedCharacters, deleteCharacter, AddToCombatReq, rollInitiative, addToCombat} from './CyberClient'
import './SearchCharacter.css'
import CharacterSheet from "./CharacterSheet"
import Hideable from "./Hideable"
import { Button } from "./Common"
import ListInitiative from "./ListInitiative"

const initialStat = 5

const initialAttributes: Attributes = {
    ATTR: initialStat,
    BODY: initialStat,
    COOL: initialStat,
    EMP: initialStat,
    INT: initialStat,
    LUCK: initialStat,
    MA: initialStat,
    REF: initialStat,
    TECH: initialStat,
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
    statuses: [],
    sp: initialSp,
    reputation: 0,
    humanity: initialAttributes.EMP * 10,
    money: 0
}

interface SearchCharacterProps {
    skills: Skill[]
    initiatives: Initiative[]
    updateLogs: (s: Log[]) => void
    updateInitiatives: () => Promise<void>
}

interface ListCharactersProps {
    characters: CharacterShort[]
    setCharacterById: (i: number) => Promise<void>
    updateLogs: (l: Log[]) => void
    updateCharacters: () => void
    setAllCharacters: (c: CharacterShort[]) => void
    initiatives: Initiative[]
    updateInitiatives: () => Promise<void>
    updateCharacterList: () => Promise<void>
}

interface CharacterListRowProps {
    character: CharacterShort
    setCharacterById: (i: number) => void
    addToCombatReq: (i: number, ini: number) => AddToCombatReq
    removeCharacter: (i: number) => Promise<Log[]>
    updateLogs: (l: Log[]) => void
    updateCharacters: () => void
    updateInitiatives: () => void
    isAlreadyInCombat: (i: number) => boolean
}
const CharacterListRow = ({character: c, isAlreadyInCombat, setCharacterById, addToCombatReq, removeCharacter, updateLogs, updateCharacters, updateInitiatives}: CharacterListRowProps) => {
    const [initiative, setInitiative] = useState<number | undefined>(undefined)
    //const initiativeToUse = c.initiative ?? initiative
    const initiativeIsValid = (i: number | undefined): boolean =>
        i !== undefined && i > 0
    const addToCombatFn = () => 
        (initiativeIsValid(initiative) && !isAlreadyInCombat(c.id)) 
        ? //initiativeToUse is now ok but for some reason I get warning initiativeToUse could be undefined
            addToCombat(addToCombatReq(c.id, initiative ?? 0)).then(() => updateInitiatives()) 
        : 
            undefined
    const handleManualIniativeInput = (v: string) => {
        const value = parseInt(v)
        if (isNaN(value)) {
            return undefined
        } else {
            return value
        }

    }
    return(
        <tr key={c.id}>
                <td>{c.name}</td>
                <td>{c.role}</td>
                <td>
                    <span>
                        <input className='valueBox' type="text" value={initiative} onChange={e => setInitiative(handleManualIniativeInput(e.target.value))}/>
                        <Button label='Roll' variant='LessSpaceLeft' onClick={() => rollInitiative({charId: c.id}).then(i => setInitiative(i))}/>
                    </span>
                    </td>
                <td>
                    <Button label='Add' disabled={!initiativeIsValid(initiative) || isAlreadyInCombat(c.id)} onClick={() => addToCombatFn()}/></td>
                <td>
                    <Button label='Show' onClick={() => setCharacterById(c.id)}/>
                </td>
                <td>
                    <Button label='Delete' onClick={() => {
                        removeCharacter(c.id).then(updateLogs).then(() => updateCharacters())
                    }}/>
                </td>
            </tr> 
    )
}

const ListCharacters = ({characters, setCharacterById, updateLogs, setAllCharacters, updateCharacters, initiatives, updateInitiatives, updateCharacterList}: ListCharactersProps) => {
    const [nameFilter, setNameFilter] = useState('')
    const charactersSorted = sortedCharacters(characters)
    const filteredCharacters = 
        nameFilter.length > 0 ? 
            charactersSorted.filter(c => c.name.toLocaleLowerCase().startsWith(nameFilter)) 
            : charactersSorted
    const removeCharacter = (charId: number) => 
        deleteCharacter({charId})

    const addToCombatReq = (charId: number, initiative: number): AddToCombatReq => {
        return {
            charId,
            initiative
        }
    }

    const isAlreadyInCombat = (charId: number): boolean =>
        !!initiatives.find(i => i.charId === charId)

    const characterTable = 
        <>
            <input placeholder='Search by...' className='filter' value={nameFilter} onChange={e => setNameFilter(e.target.value)}/>
            <Button label='Update characters' variant='SpaceLeft' onClick={() => updateCharacterList()}/>
            <table>
                <tbody>
                    <tr>
                        <th>Name</th>
                        <th>Role</th>
                        <th>Roll ini.</th>
                        <th>Add to combat</th>
                        <th>Show</th>
                        <th>Remove</th>
                    </tr>
                </tbody>
                {filteredCharacters.map(c => 
                    <CharacterListRow character={c} isAlreadyInCombat={isAlreadyInCombat} updateCharacters={updateCharacters} updateLogs={updateLogs} removeCharacter={removeCharacter} updateInitiatives={updateInitiatives} setCharacterById={setCharacterById} addToCombatReq={addToCombatReq}/>
                )}
            </table>
        </>
    return(
        <div className='listCharacters'>
            <Hideable text='characters' props={characterTable} />
        </div>
    )
}

const SearchOrCreateCharacter = ({updateLogs, initiatives, skills, updateInitiatives}: SearchCharacterProps) => {
    const [characterEditable, setCharacterEditable] = useState(false)
    const [character, setCharacter] = useState<undefined | null | Character>(undefined)
    const [allSkills, setAllSkills] = useState<Skill[] | undefined>(undefined)
    const [allCharacters, setAllCharacters] = useState<CharacterShort[] | undefined>(undefined)

    const updateCharacterList = () => 
        listCharacters().then(setAllCharacters)

    useEffect(() => {
        updateCharacterList().then(_ => setAllSkills(skills))
    }, [skills])

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
            <ListInitiative setCharacterById={setCharacterFn} initiatives={initiatives} updateInitiatives={updateInitiatives}/>
            <ListCharacters updateCharacters={updateCharacterList} updateCharacterList={updateCharacterList} updateInitiatives={updateInitiatives} initiatives={initiatives} characters={allCharacters ?? []} setCharacterById={setCharacterFn} updateLogs={updateLogs} setAllCharacters={setAllCharacters}/>
            <div className="search">
                <Button label='Create' onClick={() => createCharacter()}/>
                {character && <Button label='Hide character' className='withLeftSpace' onClick={() => setCharacter(undefined)}/>}
            </div>
            {!!character &&
                 <div><CharacterSheet updateCharacterList={updateCharacterList} allowAddingToInitiative={allowAddingToInitiative} editCharacter={setCharacter} edit={characterEditable} updateCharacter={updateCharacter} character={character} allSkills={allSkills} updateLogs={updateLogs}/></div>
            }
        </>
    )
}

export default SearchOrCreateCharacter
