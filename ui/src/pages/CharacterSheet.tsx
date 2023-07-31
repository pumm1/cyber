import { Character, Attributes, listSkills, Skill, CharacterSkill, Attribute, CharacterSP } from './CyberClient'
import React, { useState, useEffect } from "react"
import './CharacterSheet.css'

const roles = {
    solo: 'Solo',
    rocker: 'Rocker',
    netrunner: 'Netrunner',
    media: 'Media',
    nomad: 'Nomad',
    fixer: 'Fixer',
    cop: 'Cop',
    corp: 'Corp',
    techie: 'Techie',
    medtechie: 'Medtechie'
}


const DisabledInput = ({value, name, checked}) => 
    <input type="radio" value={value} name={name} checked={checked} disabled={true}/>


const TextField = ({fieldName, value}: {fieldName: string, value: string}) => {
    return(
        <div className='fieldContainer'>
            <span className='fieldContent'>
                <label>{fieldName}</label>
                <div className='fieldValue'>{value}</div>
            </span>
        </div>
    )
}

const RoleFiled = ({value}: {value: string}) => {
    return(
        <div className='fieldContainer'>
            <label>ROLE</label>
            <span className='roles'>
                <DisabledInput value={roles.solo} name={roles.solo} checked={value === roles.solo} /> Solo
                <DisabledInput value={roles.rocker} name={roles.rocker} checked={value === roles.rocker} /> Rocker
                <DisabledInput value={roles.netrunner} name={roles.netrunner} checked={value === roles.netrunner} /> Netrunner
                <DisabledInput value={roles.media} name={roles.media} checked={value === roles.media} /> Media
                <DisabledInput value={roles.nomad} name={roles.nomad} checked={value === roles.nomad} /> Nomad
                <DisabledInput value={roles.fixer} name={roles.fixer} checked={value === roles.fixer} /> Fixer
                <DisabledInput value={roles.cop} name={roles.cop} checked={value === roles.cop} /> Cop
                <DisabledInput value={roles.corp} name={roles.solo} checked={value === roles.corp} /> Corp
                <DisabledInput value={roles.techie} name={roles.techie} checked={value === roles.techie} /> Techie
                <DisabledInput value={roles.medtechie} name={roles.medtechie} checked={value === roles.medtechie} /> Medtechie
            </span>
        </div>
    )
}

const Stats = ( {attributes}: {attributes: Attributes}) => {
    const statValue = (field: string, value: number, outOf?: number) => 
        <> <b>{field} [ {value} ]</b></>

    return (
        <div className='fieldContainer'>
             <label>STATS</label>
            <div className='stats'>
                {statValue('INT', attributes.INT)}
                {statValue('REF', attributes.REF)}
                {statValue('TECH', attributes.TECH)}
                {statValue('COOL', attributes.COOL)}
                {statValue('ATTR', attributes.ATTR)}
                {statValue('LUCK', attributes.LUCK)}
                {statValue('MA', attributes.MA)}
                {statValue('BODY', attributes.BODY)}
                {statValue('EMP', attributes.EMP)}
            </div>
        </div>
    )
}

export interface CharacterSheetProps {
    character: Character
    allSkills?: Skill[]
}

const attributesInOrder = [
    Attribute.ATTR,
    Attribute.BODY,
    Attribute.COOL,
    Attribute.EMP,
    Attribute.INT,
    Attribute.REF,
    Attribute.TECH,
]

const SkillField = ({skill, characterSkills}: {skill: Skill, characterSkills: CharacterSkill[]}) => {
    const charSkillLvl = characterSkills.find(s => s.id === skill.id)?.lvl

    return (
    <div>
        {skill.skill}......[{charSkillLvl ?? ''}]
    </div>
    )
}

const SkillsByAttribute = (
    {attribute, skills, characterSkills}: {attribute: Attribute, skills: Skill[], characterSkills: CharacterSkill[]} 
) => {
    return (
       <span className='skill'>
            <b>{attribute}</b>
            {skills.filter(s => s.attribute === attribute).map(s => <SkillField skill={s} characterSkills={characterSkills}/>)}
       </span>
    )
}

const SkillsByAttributes = (
    {skills, characterSkills}: {skills: Skill[], characterSkills: CharacterSkill[]} 
) => {
   return (
    <div className='fieldContainer'>
        
        <div className='skills'>
            {attributesInOrder.map(atr => <SkillsByAttribute attribute={atr} skills={skills} characterSkills={characterSkills}/>)}
        </div>
    </div>
   )
}

const CharacterSPField = ({sp}: {sp: CharacterSP}) => {
    const Label = ({label}: {label: string}) => <label className='armorLabel'><i>{label}</i></label>
    const GridBox = ({value, bolden}: {value: number | string, bolden?: boolean}) => 
        <div className='foo'>
            {!!bolden ? <b><i>{value}</i></b> : value}
        </div>

    return(
        <div className='armorSection'>
            <span className='armorRowContainer'>
               <Label label='Location'/>
                <div className='armorContent'>
                    <GridBox value='Head' bolden={true}/>
                    <GridBox value='Torso' bolden={true}/>
                    <GridBox value='R.Arm' bolden={true}/>
                    <GridBox value='L.Arm' bolden={true}/>
                    <GridBox value='R.Leg' bolden={true}/>
                    <GridBox value='L.Leg' bolden={true}/>
                </div>
            </span>
            <span className='armorRowContainer'>
                <Label label='Armor SP'/>
                <div className='armorContent'>
                    <GridBox value={sp.head}/>
                    <GridBox value={sp.body}/>
                    <GridBox value={sp.r_arm}/>
                    <GridBox value={sp.l_arm}/>
                    <GridBox value={sp.r_leg}/>
                    <GridBox value={sp.l_leg}/>
                </div>
            </span>
        </div>
    )
}


const CharacterSheet = ({character, allSkills}: CharacterSheetProps) => {
    return(
        <div>
            <TextField fieldName='HANDLE' value={character.name} />
            <RoleFiled value={character.role}/>
            <Stats attributes={character.attributes}/>
            <CharacterSPField sp={character.sp}/>
            {allSkills && <SkillsByAttributes skills={allSkills} characterSkills={character.skills}/>}
        </div>
    )
}

export default CharacterSheet