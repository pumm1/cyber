import { useState, useEffect } from "react"
import { getCharacter , Character, listSkills} from './CyberClient'
import './SearchCharacter.css'
import React from "react"
import CharacterSheet from "./CharacterSheet"
import Window from "floating-window-ui";

const SearchCharacter = () => {
    const [name, setName] = useState('')
    const [character, setCharacter] = useState<undefined | null | Character>(undefined)
    const [allSkills, setAllSkills] = useState<any[] | undefined>(undefined)

    useEffect(() => {
        listSkills().then(setAllSkills)
    }, [])

    const titleBarProps = (c: Character) => ({
        title: c.name,
        buttons: {
            close: () => setCharacter(undefined)
        }
    })
    
    return(
        <div>
            <div className="search">
                <label>Search</label>
                <input type="text" onChange={(event) => {
                            setName(event.target.value);
                        }}/>
                <button onClick={() => getCharacter(name).then(setCharacter)}>Search</button>
            </div>
            {!!character &&
            <Window id={'character' + character.id} height={1300} width={900} resizable={true} titleBar={titleBarProps(character)}>
                <div className="sheetContainer"><CharacterSheet character={character} allSkills={allSkills}/></div>
            </Window>}
        </div>
    )
}

export default SearchCharacter