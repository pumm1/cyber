import { Character, Attributes, listSkills, Skill, CharacterSkill, Attribute, CharacterSP, rollSkill, RollSkill, Weapon, attack, AttackReq, AttackType, isGun, ReloadReq, reload, Log, WeaponType, repair, lvlUp, heal } from './CyberClient'
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

interface UpdateCharacter {
    updateCharacter: () => Promise<void>
}

interface UpdateCharacterAndLogs extends UpdateCharacter {
    updateLogs: (s: Log[]) => void
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

export interface CharacterSheetProps extends UpdateCharacterAndLogs{
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

interface SkillProps {
    skill: Skill
    characterSkills: CharacterSkill[]
    charId: number
    updateCharacter: () => Promise<void>
}

const SkillRow = ({skill, characterSkills, charId, updateCharacter}: SkillProps) => {
    const [rollResult, setRollResult] = useState<undefined | number>(undefined)
    const charSkillLvl = characterSkills.find(s => s.id === skill.id)?.lvl ?? 0
    const roll: RollSkill = {
        charId: charId,
        skillId: skill.id,
        addedLuck: 0
    }

    return (
    <div className='skill' key={skill.id}>
        <span>
            {<button className='skillBtn' disabled={charSkillLvl >= 10 } onClick={() => lvlUp(charId, skill.id).then(updateCharacter)}>+</button>}
            <button className='skillBtn' onClick={() => rollSkill(roll).then(res => setRollResult(res))}>Roll</button>
            {skill.skill.padEnd(36, '.')}[{charSkillLvl ?? ''}]
            {rollResult && <>({rollResult})</>}
        </span>
    </div>
    )
}

interface SkillsProps {
    skills: Skill[]
    characterSkills: CharacterSkill[]
    charId: number
    updateCharacter: () => Promise<void>
}

interface SkillsByAttributeProps extends SkillsProps{
    attribute: Attribute
}

const SkillsByAttribute = ({attribute, skills, characterSkills, charId, updateCharacter}: SkillsByAttributeProps) => {
    return (
       <span key={attribute}>
            <b>{attribute}</b>
            {skills.filter(s => s.attribute === attribute).map(s => <SkillRow skill={s} characterSkills={characterSkills} charId={charId} updateCharacter={updateCharacter}/>)}
       </span>
    )
}

const SkillsByAttributes = ({skills, characterSkills, charId, updateCharacter}: SkillsProps ) => {
   return (
    <>
        <label>Skills</label>
        <div className='fieldContainer'>
            <div className='skills'>
                {attributesInOrder.map(atr => <SkillsByAttribute updateCharacter={updateCharacter} attribute={atr} skills={skills} characterSkills={characterSkills} charId={charId}/>)}
            </div>
        </div>
    </>
   )
}

interface RangeProps {
    weaponIsGun: boolean
    attackRange: number
    setAttackRange: (n: number) => void
}

const Range = ({weaponIsGun, attackRange, setAttackRange}: RangeProps) => 
        weaponIsGun && <>Range <input className='range' type='text' disabled={false} value={attackRange} onChange={e => setAttackRange(parseInt(e.target.value) || 1)}/></>

interface WeaponProps extends UpdateCharacterAndLogs {
    weapon: Weapon, 
    characterId: number
}

const WeaponRow = ({weapon, characterId, updateLogs, updateCharacter}: WeaponProps) => {
    const isMelee = weapon.weaponType === 'melee'
    const weaponIsGun: boolean = isGun(weapon.weaponType)
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
            <InputRow show={isFullAuto} onClick={() => setAttackType(AttackType.FullAuto)} checked={attackType === AttackType.FullAuto} label='FA' />
        </span>

    const defaultAttackRange = weaponIsGun ? 10 : 1
    const [attackRange, setAttackRange] = useState(defaultAttackRange)

    const attackReq: AttackReq = {
        charId: characterId,
        weaponId: weapon.id,
        attackType,
        attackRange, //TODO
        attackModifier: 0 //TODO
    }

    const reloadReq: ReloadReq = {
        weaponId: weapon.id,
        shots: weapon.clipSize
    }

    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter()
    }

    const Dmg = ({}) => {
        const possibleBonusDmg = weapon.dmgBonus ? <>{`+${weapon.dmgBonus}`}</> : <></>
        return(<>[{weapon.diceNum}D{weapon.dmg}{possibleBonusDmg}]</>)
    }    

    return (
        <div className='weapon' key={`${characterId} ${weapon.id}`}>
            {weapon.item} {ammoInfo} [{weapon.weaponType}] <Dmg />
            <button onClick={() => attack(attackReq).then(updateLogsAndCharacter)}>Attack</button>
            <Range weaponIsGun={weaponIsGun} attackRange={attackRange} setAttackRange={setAttackRange}/>
            {weaponIsGun && 
            <button onClick={() => reload(reloadReq).then(updateLogsAndCharacter)}>
                Reload
            </button>}
            <AttackTypes />
        </div>
    )
}

const CharacterWeapons = (
    {weapons, characterId, updateLogs, updateCharacter}: 
    {weapons: Weapon[], characterId: number, updateLogs: (s: Log[]) => void, updateCharacter: () => Promise<void>}
) => {
    return (
    <div key={characterId} className='fieldContainer'>
        <div className='weapons'>
            {weapons.map(w => <WeaponRow key={`${characterId} ${w.id}`} weapon={w} characterId={characterId} updateLogs={updateLogs} updateCharacter={updateCharacter} />)}
        </div>
    </div>
    )
}

interface SPFieldProps {
    characterId: number
    sp: CharacterSP
    updateCharacter: () => Promise<void>
}

interface GridBoxProps {
    value: number | string
    bolden?: boolean
    otherValue?: number | string
}

const CharacterSPField = ({sp, characterId, updateCharacter}: SPFieldProps) => {
    const Label = ({label}: {label: string}) => <label className='armorLabel'><i>{label}</i></label>
    const BoldenVal = ({value}: GridBoxProps) => 
        <div><b><i>{value}</i></b></div>

    const GridBox = ({value, otherValue, bolden}: GridBoxProps) => 
        <div className='sp'>
            <div>{!!bolden ? <BoldenVal value={value}/> : value}</div>
            {otherValue && !!bolden && <div><BoldenVal value={otherValue}/> </div>}
        </div>

    return(
        <div className='armorSection'>
            <span className='armorRowContainer'>
               <Label label='Location'/>
                <div className='armorContent'>
                    <GridBox value='Head' otherValue='1' bolden={true}/>
                    <GridBox value='Torso' otherValue='2-4' bolden={true}/>
                    <GridBox value='R.Arm' otherValue='5' bolden={true}/>
                    <GridBox value='L.Arm' otherValue='6' bolden={true}/>
                    <GridBox value='R.Leg' otherValue='7-8' bolden={true}/>
                    <GridBox value='L.Leg' otherValue='9-0' bolden={true}/>
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
                <button className='repair' onClick={() => repair(characterId).then(updateCharacter)}>Repair</button>
            </span>
        </div>
    )
}

interface SaveAndHealthProps extends UpdateCharacterAndLogs{
    character: Character
}

interface DmgBoxSetProps {
    upper: string
    lower: string
    boxesTicked: number
}

const FourDmgBoxes = ({upper, lower, boxesTicked}: DmgBoxSetProps) => {
    return(
        <div className='fourDmgBoxes'>
            <div className='dmgUpperLabel'>{upper}</div>
            <>
                {(() => {
                    const arr = [];

                    for (let i = 1; i <= 4; i++) {
                        arr.push(
                            <div className='dmgBox'>
                                {i <= boxesTicked ? <div key={upper + i} className='dmgTick'></div> : ' '}
                            </div>
                        )
                    }
                    return <div className='dmgBoxSet'>{arr}</div>;
                })()}
        </>
       <div className='dmgStun'>{lower}</div>
    </div>
    )
}

const SaveAndHealthRow = ({character, updateCharacter, updateLogs}: SaveAndHealthProps) => {
    const { dmgTaken, id } = character
    const save = character.attributes.BODY
    const btm = character.btm
    
    const leftOver = dmgTaken % 4

    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter()
    }

    const resolveTicks = (lowerLimit:number, upperLimit: number): number => 
        dmgTaken > lowerLimit ? (dmgTaken >= upperLimit ? 4 : leftOver) : 0

    return(
        <div className='boxContainer'>
             <div className='outerBox'>
                    <div className='boxLabel'>Save</div>
                    <div className='boxValue'>{save}</div>
                </div>
                <div className='outerBox'>
                    <div className='boxLabel'>BTM</div>
                    <div className='boxValue'>{btm ?? ''}</div>
                </div>
                <div className='dmgTakenContainer'>
                    <div className='dmgTakenOuterbox'>
                        <FourDmgBoxes upper='Light' lower='Stun 0' boxesTicked={resolveTicks(0, 4)}/>
                        <FourDmgBoxes upper='Serious' lower='Stun 1' boxesTicked={resolveTicks(4, 8)}/>
                        <FourDmgBoxes upper='Critical' lower='Stun 2' boxesTicked={resolveTicks(8, 12)}/>
                        <FourDmgBoxes upper='Mortal 0' lower='Stun 3' boxesTicked={resolveTicks(12, 16)}/>
                        <FourDmgBoxes upper='Mortal 1' lower='Stun 4' boxesTicked={resolveTicks(16, 20)}/>
                    </div>
                    <div className='dmgTakenOuterbox'>
                        <FourDmgBoxes upper='Mortal 2' lower='Stun 5' boxesTicked={resolveTicks(20, 24)}/>
                        <FourDmgBoxes upper='Mortal 3' lower='Stun 6' boxesTicked={resolveTicks(24, 28)}/>
                        <FourDmgBoxes upper='Mortal 4' lower='Stun 7' boxesTicked={resolveTicks(28, 32)}/>
                        <FourDmgBoxes upper='Mortal 5' lower='Stun 8' boxesTicked={resolveTicks(32, 36)}/>
                        <FourDmgBoxes upper='Mortal 6' lower='Stun 9' boxesTicked={resolveTicks(36, 40)}/>
                    </div>
                    <div><button onClick={() => heal(id).then(updateLogsAndCharacter)}>Heal (1)</button></div>
                </div>
        </div>
    )
}


const CharacterSheet = ({character, allSkills, updateLogs, updateCharacter}: CharacterSheetProps) => {
    return(
        <div className='main'>
            <TextField fieldName='HANDLE' value={character.name} />
            <RoleFiled value={character.role}/>
            <Stats attributes={character.attributes}/>
            <CharacterSPField sp={character.sp} characterId={character.id} updateCharacter={updateCharacter}/>
            <SaveAndHealthRow character={character} updateCharacter={updateCharacter} updateLogs={updateLogs}/>
            {allSkills && <SkillsByAttributes skills={allSkills} characterSkills={character.skills} charId={character.id} updateCharacter={updateCharacter}/>}
            <CharacterWeapons weapons={character.weapons} characterId={character.id} updateLogs={updateLogs} updateCharacter={updateCharacter}/>
        </div>
    )
}

export default CharacterSheet