import { useState, useEffect } from "react"
import { getCharacter , Character, listSkills, Log, Attributes, CharacterSP} from './CyberClient'
import './SearchCharacter.css'
import React from "react"
import CharacterSheet from "./CharacterSheet"
import Window from "floating-window-ui";

interface SearchCharacterProps {
    updateLogs: (s: Log[]) => void
}

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
    role: 'solo',
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
    humanity: initialAttributes.EMP * 10
}

const SearchOrCreateCharacter = ({updateLogs}: SearchCharacterProps) => {
    const [name, setName] = useState('')
    const [characterEditable, setCharacterEditable] = useState(false)
    const [character, setCharacter] = useState<undefined | null | Character>(undefined)
    const [allSkills, setAllSkills] = useState<any[] | undefined>(undefined)

    useEffect(() => {
        listSkills().then(setAllSkills)
    }, [])

    const windowName = characterEditable ? 'New character' : character?.name ?? ''

    const titleBarProps = () => ({
        title: windowName,
        buttons: {
            close: () => setCharacter(undefined)
        }
    })
    
    const updateCharacter = (): Promise<void> => {
        setCharacterEditable(false)
        return getCharacter(name).then(setCharacter)
    }

    const createCharacter = () => {
        setCharacter(characterToCreate)
        setCharacterEditable(true)
    }

    return(
        <div>
            <div className="search">
                <label>Search</label>
                <input type="text" onChange={(event) => {
                            setName(event.target.value);
                        }}/>
                <button className='searchOrCreate' onClick={() => updateCharacter()}>Search</button>
                <button className='searchOrCreate' onClick={() => createCharacter()}>Create</button>
            </div>
            {!!character &&
                <Window id={'character' + character.id} height={1400} width={950} resizable={true} titleBar={titleBarProps()}>
                    <div className="sheetContainer"><CharacterSheet editCharacter={setCharacter} edit={characterEditable} updateCharacter={updateCharacter} character={character} allSkills={allSkills} updateLogs={updateLogs}/></div>
                </Window>
            }
        </div>
    )
}

export default SearchOrCreateCharacter