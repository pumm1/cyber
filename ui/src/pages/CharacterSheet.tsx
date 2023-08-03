import { Character, Attributes, listSkills, Skill, CharacterSkill, Attribute, CharacterSP, rollSkill, RollSkill, Weapon, attack, AttackReq, AttackType } from './CyberClient'
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
    updateLogs: (s: string[]) => void
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

const SkillField = ({skill, characterSkills, charId}: {skill: Skill, characterSkills: CharacterSkill[], charId: number}) => {
    const [rollResult, setRollResult] = useState<undefined | number>(undefined)
    const charSkillLvl = characterSkills.find(s => s.id === skill.id)?.lvl
    const roll: RollSkill = {
        charId: charId,
        skillId: skill.id,
        addedLuck: 0
    }

    return (
    <div className='skill' key={skill.id}>
        <span>
            <button className='skillBtn' onClick={() => rollSkill(roll).then(res => setRollResult(res))}>Roll</button>
            {skill.skill}......[{charSkillLvl ?? ''}]
            {rollResult && <>({rollResult})</>}
        </span>
    </div>
    )
}

const SkillsByAttribute = (
    {attribute, skills, characterSkills, charId}: {attribute: Attribute, skills: Skill[], characterSkills: CharacterSkill[], charId: number} 
) => {
    return (
       <span key={attribute}>
            <b>{attribute}</b>
            {skills.filter(s => s.attribute === attribute).map(s => <SkillField skill={s} characterSkills={characterSkills} charId={charId}/>)}
       </span>
    )
}

const SkillsByAttributes = (
    {skills, characterSkills, charId}: {skills: Skill[], characterSkills: CharacterSkill[], charId: number} 
) => {
   return (
    <div className='fieldContainer'>
        
        <div className='skills'>
            {attributesInOrder.map(atr => <SkillsByAttribute attribute={atr} skills={skills} characterSkills={characterSkills} charId={charId}/>)}
        </div>
    </div>
   )
}

const WeaponRow = ({weapon, characterId, updateLogs}: {weapon: Weapon, characterId: number, updateLogs: (s: string[]) => void}) => {
    const isMelee = weapon.weaponType === 'melee'
    const defaultAttackType = isMelee ? AttackType.Melee : AttackType.Single
    const ammoInfo = isMelee ? '' : `(${weapon.shotsLeft} / ${weapon.clipSize})`
    const [attackType, setAttackType] = useState<AttackType>(defaultAttackType)
    const isFullAuto: boolean = !isMelee && weapon.rof >= 3

    const InputRow = ({show, onClick, checked, label}: {show: boolean, onClick: () => void, checked: boolean, label: string}) => {
       const inputId = label + weapon.id

       return (
            show && <><input key={weapon.id} type='radio' onChange={() => {}} onClick={onClick} checked={checked} value={inputId} name={inputId}/> {label}</>
       )
    }

    const AttackTypes = ({}) => 
        <span>
            <InputRow show={isMelee} onClick={() => setAttackType(AttackType.Melee)} checked={attackType === AttackType.Melee} label='Melee' />
            <InputRow show={!isMelee} onClick={() => setAttackType(AttackType.Single)} checked={attackType === AttackType.Single} label='Single' />
            <InputRow show={isFullAuto} onClick={() => setAttackType(AttackType.Burst)} checked={attackType === AttackType.Burst} label='Burst' />
            <InputRow show={isFullAuto} onClick={() => setAttackType(AttackType.FullAuto)} checked={attackType === AttackType.FullAuto} label='Full auto' />
        </span>

    const attackReq: AttackReq = {
        charId: characterId,
        weaponId: weapon.id,
        attackType,
        attackRange: 10, //TODO
        attackModifier: 0 //TODO
    }

    return (
        <div className='weapon' key={`${characterId} ${weapon.id}`}>
            {weapon.item} {ammoInfo} [{weapon.weaponType}]
            <button onClick={() => attack(attackReq).then(resLogs => updateLogs(resLogs))}>Attack</button>
            <AttackTypes />
        </div>
    )
}

const CharacterWeapons = (
    {weapons, characterId, updateLogs}: {weapons: Weapon[], characterId: number, updateLogs: (s: string[]) => void}
) => {
    return (
    <div key={characterId} className='fieldContainer'>
        <div className='weapons'>
            {weapons.map(w => <WeaponRow key={`${characterId} ${w.id}`} weapon={w} characterId={characterId} updateLogs={updateLogs} />)}
        </div>
    </div>
    )
}

const CharacterSPField = ({sp}: {sp: CharacterSP}) => {
    const Label = ({label}: {label: string}) => <label className='armorLabel'><i>{label}</i></label>
    const GridBox = ({value, bolden}: {value: number | string, bolden?: boolean}) => 
        <div className='sp'>
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


const CharacterSheet = ({character, allSkills, updateLogs}: CharacterSheetProps) => {
    return(
        <div className='main'>
            <TextField fieldName='HANDLE' value={character.name} />
            <RoleFiled value={character.role}/>
            <Stats attributes={character.attributes}/>
            <CharacterSPField sp={character.sp}/>
            {allSkills && <SkillsByAttributes skills={allSkills} characterSkills={character.skills} charId={character.id}/>}
            <CharacterWeapons weapons={character.weapons} characterId={character.id} updateLogs={updateLogs}/>
        </div>
    )
}

export default CharacterSheet