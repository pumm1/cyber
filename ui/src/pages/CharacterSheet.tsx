import { Character, Attributes, listSkills } from './CyberClient'
import React, { useState, useEffect } from "react"
import './CharacterSheet.css'

//test foo bar afsfaf
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


const textField = (fieldName: string, value: string) => {
    return(
        <div className='fieldContainer'>
            <span>
                <label>{fieldName}</label>
                <div className='fieldValue'>{value}</div>
            </span>
        </div>
    )
}

const roleFiled = (value: string) => {
    return(
        <div className='roleContainer'>
            <label>ROLE</label>
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
        </div>
    )
}

const stats = (attributes: Attributes) => {
    const statValue = (field: string, value: number, outOf?: number) => 
        <> <b>{field}</b> <b>[ {value} ]</b></>

    return (
        <div className='statContainer'>
             <label>STATS</label>
            <div>
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
    allSkills?: any[]
}

const CharacterSheet = ({character}: CharacterSheetProps) => {
    return(
        <div>
            <div>
                {textField('HANDLE', character.name)}
                {roleFiled(character.role)}
                {stats(character.attributes)}
            </div>
        </div>
    )
}

export default CharacterSheet