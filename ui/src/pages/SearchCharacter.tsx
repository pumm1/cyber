import { useState, useEffect } from "react"
import { getCharacter , Character, listSkills} from './CyberClient'
import './SearchCharacter.css'
import React from "react"
import Head from './character_parts/head.svg'
import CharacterSheet from "./CharacterSheet"

const SearchCharacter = () => {
    const [name, setName] = useState('')
    const [character, setCharacter] = useState<undefined | null | Character>(undefined)
    const [allSkills, setAllSkills] = useState<any[] | undefined>(undefined)

    useEffect(() => {
        listSkills().then(setAllSkills)
    }, [])
    
    return(
        <div>
            <div className="search">
                <label>Search</label>
                <input type="text" onChange={(event) => {
                            setName(event.target.value);
                        }}/>
                <button onClick={() => getCharacter(name).then(setCharacter)}>Search</button>
            </div>
            {!!character ? <CharacterSheet character={character} allSkills={allSkills}/> : character === null ? <CharacterNotFound /> : ''} 
        </div>
    )
}

const field = (fieldName: string, value: string) => {
    return(
        <span>
            <label>{fieldName}: </label>
            <>{value}</>
        </span>
    )
}

const skills = (c: Character) => {
    return (
        <>{c.skills.map(s => <span>{s}</span>)}</>
    )
}

const CharacterNotFound = () => <div>Not found</div>

const CharacterInfo = (char: Character): JSX.Element => {
    //TODO: attributes
    //TODO: make character info look closer to original character sheet
    //TODO: figure out svgs
    return (
        <div className='CharacterInfo'>
            {field('handle', char.name)}
            {field('role', char.role)}
            {field('body type', char.bodyType)}
            {field('BTM', char.bodyTypeModifier)}
            {field('skills', "")}
            {skills(char)}
        </div>
    )
}

export default SearchCharacter