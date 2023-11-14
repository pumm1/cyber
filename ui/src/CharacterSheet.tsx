import { Character, Attributes, Skill, CharacterSkill, Attribute, CharacterSP, rollSkill, Weapon, attack, AttackReq, AttackType, isGun, ReloadReq, reload, Log, WeaponType, repair, lvlUp, heal, RollSkillReq, doDmg, BodyPart, createCharacter, CreateCharacterReq, Chrome, UpdateIPReq, updateIP, Armor, removeArmor, RemoveArmorReq, AddRepReq, addReputation, CharacterReq, UpdateMoneyReq, updateMoney, removeWeapon, RemoveWeaponReq, removeChrome, RemoveChromeReq, MeleeAttackMethod, rollMeleeDmg, MeleeDmgRollReq, faceOffRoll, RestoreEMPReq, restoreCharEMP, stuncheck, updateCharacterName } from './CyberClient'
import { useState } from "react"
import './CharacterSheet.css'
import { AddWeapon } from './AddWeapon'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'
import AddChrome from './AddChrome'
import AddArmor from './AddArmor'


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

//TODO:
//opt LUCK skilleihin
//thrown toimimaan?

interface UpdateCharacter {
    updateCharacter: (i: number) => Promise<void>
}

interface UpdateCharacterAndLogs extends UpdateCharacter {
    updateLogs: (s: Log[]) => void
}

interface RoleInputProps {
    value: number | string
    name: string
    checked: boolean
    edit: boolean
    updateChracterRole: (r: string) => void
}

const RoleInput = ({edit, value, name, checked,  updateChracterRole}: RoleInputProps) => 
    <input type="radio" value={value} name={name} checked={checked} disabled={!edit} onChange={e => updateChracterRole(e.target.value)}/>


interface RoleFieldProps {
    value: string
    edit: boolean
    updateChracterRole: (r: string) => void
}

const RoleFiled = ({value, edit, updateChracterRole}: RoleFieldProps) => {
    return(
        <div className='fieldContainer'>
            <label>ROLE</label>
            <span className='roles'>
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.solo} name={roles.solo} checked={value === roles.solo} /> Solo
                <RoleInput updateChracterRole={updateChracterRole}  edit={edit} value={roles.rocker} name={roles.rocker} checked={value === roles.rocker} /> Rocker
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.netrunner} name={roles.netrunner} checked={value === roles.netrunner} /> Netrunner
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.media} name={roles.media} checked={value === roles.media} /> Media
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.nomad} name={roles.nomad} checked={value === roles.nomad} /> Nomad
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.fixer} name={roles.fixer} checked={value === roles.fixer} /> Fixer
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.cop} name={roles.cop} checked={value === roles.cop} /> Cop
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.corp} name={roles.solo} checked={value === roles.corp} /> Corp
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.techie} name={roles.techie} checked={value === roles.techie} /> Techie
                <RoleInput updateChracterRole={updateChracterRole} edit={edit} value={roles.medtechie} name={roles.medtechie} checked={value === roles.medtechie} /> Medtechie
            </span>
        </div>
    )
}

interface StatValueProps {
    field: string,
    value: number
    outOf?: number //TODO: use outOf?
    props?: JSX.Element
}
const StatValue = ({field, value, props}: StatValueProps) => 
        <span className='statValue'> <b>{field} [{value}{props}]</b></span>


interface StatsProps extends UpdateCharacterAndLogs {
    characterId: number
    attributes: Attributes
    updateCharacterAttributes: (a: Attributes) => void
    edit: boolean
}

const Stats = ( {characterId, attributes, updateCharacter, updateLogs, updateCharacterAttributes, edit}: StatsProps) => {
    
    const run = attributes.MA * 3
    const leap = Math.floor(run / 4)
    const liftKg = attributes.BODY * 40 

    interface EditableStatProps {
        attribute: Attribute
        value: number
    }
    const EditableStat = ({attribute, value}: EditableStatProps) => {
        const updatedAttributes = (change: number) => {
            switch(attribute) {
                case Attribute.ATTR:
                    const {ATTR, ...a} = attributes
                    return {ATTR: value + change, ...a}
                case Attribute.BODY:
                    const {BODY, ...b} = attributes
                    return {BODY: value + change, ...b}
                case Attribute.COOL:
                    const {COOL, ...c} = attributes
                    return {COOL: value + change, ...c}
                case Attribute.EMP:
                    const {EMP, ...d} = attributes
                    return {EMP: value + change, ...d}
                case Attribute.INT:
                    const {INT, ...e} = attributes
                    return {INT: value + change, ...e}
                case Attribute.LUCK:
                    const {LUCK, ...f} = attributes
                    return {LUCK: value + change, ...f}
                case Attribute.MA:
                    const {MA, ...g} = attributes
                    return {MA: value + change, ...g}
                case Attribute.REF:
                    const {REF, ...h} = attributes
                    return {REF: value + change, ...h}
                case Attribute.TECH:
                    const {TECH, ...i} = attributes
                    return {TECH: value + change, ...i}
            }
        }

        return (
            <div className='trianglesSet'>
                <a onClick={() => updateCharacterAttributes(updatedAttributes(+1))}>
                    <div className="triangleUp"></div>
                </a>
                <a onClick={() => updateCharacterAttributes(updatedAttributes(-1))}>
                    <div className="triangleDown"></div>
                </a>
            </div>
         )
    }

    const [empToRestore, setEmpToRestore] = useState(0)
    const empRestoreDisabled: boolean = empToRestore <= 0
    const restoreEMPReq: RestoreEMPReq = {
        charId: characterId,
        emp: empToRestore
    }

    const updateEmpToRestore = (v: number) => updateNumWithLowerLimit(v, 0, setEmpToRestore)
    const updateCharacterAndLogs = (logs: Log[]) => {
        updateLogs(logs)
        updateCharacter(characterId)
    }
    const restoreEMP = () => {
        restoreCharEMP(restoreEMPReq).then(updateCharacterAndLogs)
    }

    return (
        <div className='fieldContainer'>
             <label>STATS</label>
            <div className='stats'>
                <StatValue field='INT' value={attributes.INT} props={edit ?  <EditableStat attribute={Attribute.INT} value={attributes.INT}/> : undefined}/>
                <StatValue field='REF' value={attributes.REF} props={edit ? <EditableStat attribute={Attribute.REF} value={attributes.REF}/> : undefined}/>
                <StatValue field='TECH' value={attributes.TECH} props={edit ? <EditableStat attribute={Attribute.TECH} value={attributes.TECH}/> : undefined}/>
                <StatValue field='COOL' value={attributes.COOL} props={edit ? <EditableStat attribute={Attribute.COOL} value={attributes.COOL}/> : undefined}/>
                <StatValue field='ATTR' value={attributes.ATTR} props={edit ? <EditableStat attribute={Attribute.ATTR} value={attributes.ATTR}/> : undefined}/>
                <StatValue field='LUCK' value={attributes.LUCK} props={edit ? <EditableStat attribute={Attribute.LUCK} value={attributes.LUCK}/> : undefined}/>
                <StatValue field='MA' value={attributes.MA} props={edit ? <EditableStat attribute={Attribute.MA} value={attributes.MA}/> : undefined}/>
                <StatValue field='BODY' value={attributes.BODY} props={edit ? <EditableStat attribute={Attribute.BODY} value={attributes.BODY}/> : undefined}/>
                <StatValue field='EMP' value={attributes.EMP} props={edit ? <EditableStat attribute={Attribute.EMP} value={attributes.EMP}/> : undefined}/>
                <StatValue field='RUN' value={run} />
                <StatValue field='Leap' value={leap} />
                <StatValue field='Lift' value={liftKg} />
            </div>
            {!edit && 
            <span className='valueToAdd'>
                <ValueChanger baseValue={empToRestore} onChange={updateEmpToRestore}/>{empToRestore}
                <button className='withLeftSpace' disabled={empRestoreDisabled} onClick={() => restoreEMP()}>Restore EMP</button>
            </span>}
        </div>
    )
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
    updateCharacter: (i: number) => Promise<void>
    roll?: number
    modifier: number
    updateLogsAndCharacter: (l: Log[]) => void
}

interface SkillRowProps extends UpdateCharacter {
    charId: number
    rollSkill: (r: RollSkillReq) => Promise<Log[]>
    skill: Skill
    charSkillLvl: number
    charOriginalSkillLvl: number
    rollReq: RollSkillReq
    updateLogsAndCharacter: (l: Log[]) => void
}

const SkillRow = ({skill, charSkillLvl, charOriginalSkillLvl, rollReq, charId, updateLogsAndCharacter, updateCharacter}: SkillRowProps) => {
    return(
        <div className='skill' key={skill.id}>
            <span>
                {<button className='withLessRightSpace' disabled={charOriginalSkillLvl >= 10 } onClick={() => lvlUp(charId, skill.id).then(() => updateCharacter(charId))}>+</button>}
                <button className='skillBtn' onClick={() => rollSkill(rollReq).then(updateLogsAndCharacter)}>Roll</button>
                <span className='withLessLeftSpace'>
                    {skill.skill.padEnd(30, '.')}[{charSkillLvl ?? ''}]
                </span>
            </span>
        </div>
    )
}

const SkillRowByCharacterSkills = ({skill, characterSkills, charId, updateCharacter, roll, modifier, updateLogsAndCharacter}: SkillProps) => {
    const charSkillLvl = characterSkills.find(s => s.id === skill.id)?.lvl ?? 0
    const charOriginalSkillLvl = characterSkills.find(s => s.id === skill.id)?.originalLvl ?? 0
    const rollReq: RollSkillReq = {
        charId: charId,
        skillId: skill.id,
        addedLuck: 0, //TODO
        roll,
        modifier
    }

    return (
        <SkillRow updateLogsAndCharacter={updateLogsAndCharacter} charSkillLvl={charSkillLvl} charOriginalSkillLvl={charOriginalSkillLvl} updateCharacter={updateCharacter} skill={skill} charId={charId} rollSkill={rollSkill} rollReq={rollReq} />
    )
}

interface SkillsProps extends UpdateCharacterAndLogs {
    skills: Skill[]
    character: Character
}

interface SkillsByAttributeProps extends SkillsProps {
    attribute: Attribute
    characterSkills: CharacterSkill[]
    roll?: number
    modifier: number
}



const SkillsByAttribute = ({attribute, skills, characterSkills, character, updateCharacter, roll, modifier, updateLogs}: SkillsByAttributeProps) => {
    const updateLogsAndCharacter = (l: Log[]) => {
        updateLogs(l)
        updateCharacter(character.id)
    }
    
    return(
        <span key={attribute + character.id}>
            <b>{attribute}</b>
            {skills.filter(s => s.attribute === attribute).map(s => <SkillRowByCharacterSkills roll={roll} updateLogsAndCharacter={updateLogsAndCharacter} modifier={modifier} skill={s} characterSkills={characterSkills} charId={character.id} updateCharacter={updateCharacter}/>)}
         </span>
    )
}



const SkillsByAttributes = ({skills, character, updateCharacter, updateLogs}: SkillsProps ) => {
    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter(character.id)
    }

    const [roll, setRoll] = useState(0)
    const [rollModifier, setRollModifier] = useState(0)

    const specialSkill: Skill = {
        skill: character.specialAbility,
        attribute:  Attribute.REF, //TODO
        description: '', //TODO
        id: 0
    }

    const specialRollReq: RollSkillReq = {
        charId: character.id,
        skillId: specialSkill.id,
        addedLuck: 0,
        roll,
        modifier: rollModifier
    }

    const [ipToAdd, setIpToadd] = useState(0)
    const [money, setMoney] = useState(character.money)

    const updateMoneyReq: UpdateMoneyReq = {
        charId: character.id,
        money,
    }

    const ipReq: UpdateIPReq = {
        charId: character.id,
        ipAmount: ipToAdd
    }
    const updateIp = () => {
        updateIP(ipReq).then(updateLogsAndCharacter).then(() => setIpToadd(0))
    }

    const [showAddRep, setShowAddRep] = useState(false)
    const [addRep, setAddRep] = useState(0)
    const [repFor, setRepFor] = useState('')
    const addRepReq: AddRepReq = {
        charId: character.id,
        rep: addRep,
        repFor
    }

    const faceOffReq: CharacterReq = {
        charId: character.id
    }

   return (
    <>
        <label>Skills</label>
        <div className='fieldContainer'>
            <div className='skills'>
                <span>
                    <b>Special ability</b>
                    <SkillRow updateLogsAndCharacter={updateLogsAndCharacter} charOriginalSkillLvl={character.specialAbilityLvl} rollReq={specialRollReq} charId={character.id} updateCharacter={updateCharacter} rollSkill={rollSkill} charSkillLvl={character.specialAbilityLvl} skill={specialSkill} />
                </span>
                {attributesInOrder.map(atr => <SkillsByAttribute roll={roll} modifier={rollModifier} key={'atr' + atr} updateCharacter={updateCharacter} updateLogs={updateLogs} attribute={atr} skills={skills} characterSkills={character.skills} character={character}/>)}
                <span className='valueToAdd'>
                    <StatValue field='Given roll' value={roll}/> <ValueChanger onChange={setRoll} baseValue={roll} />
                    <button onClick={() => setRoll(0)} className='withLeftSpace'>Reset</button>
                </span>
                <span className='valueToAdd'>
                    <StatValue field='Roll modifier' value={rollModifier}/> <ValueChanger onChange={setRollModifier} baseValue={rollModifier} />
                    <button onClick={() => setRollModifier(0)} className='withLeftSpace'>Reset</button>
                </span>
                <span className='valueToAdd'>
                    <StatValue field='REP' value={character.reputation}/>
                    <button onClick={() => setShowAddRep(!showAddRep)}>{showAddRep ? 'Hide' : 'Show'} REP form</button>
                    <button onClick={() => faceOffRoll(faceOffReq).then(updateLogsAndCharacter)} className='withLeftSpace'>Roll Faceoff</button>
                </span>
                {showAddRep &&
                    <span className='valueToAdd'>
                        <>{addRep}<ValueChanger onChange={setAddRep} baseValue={addRep} /></>
                        <span className='withLeftSpace'>
                            <textarea placeholder={'Reputation received for...'} value={repFor} onChange={e => setRepFor(e.target.value)}/>
                            <button disabled={addRep === 0} className='withMoreLeftSpace' onClick={() => addReputation(addRepReq).then(updateLogsAndCharacter)}>Add rep</button>
                        </span>
                    </span>   
                }
                <span className='valueToAdd'>
                    <StatValue field='Current IP' value={character.ip}/>
                    ({ipToAdd})
                    <ValueChanger onChange={setIpToadd} baseValue={ipToAdd} />
                    <button className='withLeftSpace' disabled={ipToAdd === 0} onClick={updateIp}>Change IP</button>
                </span>
                <StatValue field='Humanity' value={character.humanity}/>
                <span className='valueToAdd'>
                    <StatValue field='EB' value={character.money}/>
                    <input className='valueBox' value={money} onChange={e => setMoney(parseInt(e.target.value) ?? 0)}/>
                    <button className='withLeftSpace' onClick={() => updateMoney(updateMoneyReq).then(updateLogsAndCharacter)} disabled={character.money === money}>
                        Update
                    </button>
                </span>
            </div>
        </div>
    </>
   )
}

interface InputRowProps {
    show: boolean
    onClick: () => void
    checked: boolean
    label: string
    weapon: Weapon
}

const InputRow = ({weapon, show, onClick, checked, label}: InputRowProps) => {
    const inputId = label + weapon.id

    return (
         show ? <><input key={weapon.id} type='radio' onChange={() => {}} onClick={onClick} checked={checked} value={inputId} name={inputId}/> {label}</> : <></>
    )
 }

 interface DmgProps {
    weapon: Weapon
 }

 const Dmg = ({weapon}: DmgProps) => {
    const possibleBonusDmg = weapon.dmgBonus ? <>{`+${weapon.dmgBonus}`}</> : <></>
    return(<>[{weapon.diceNum}D{weapon.dmg}{possibleBonusDmg}]</>)
}

interface RangeProps {
    show: boolean
    attackRange: number
    setAttackRange: (n: number) => void
}

const Range = ({show, attackRange, setAttackRange}: RangeProps) => 
    show ? <><input className='shortInput' type='text' disabled={false} value={attackRange} onChange={e => setAttackRange(parseInt(e.target.value) || 0)}/></> :<></>

interface WeaponProps extends UpdateCharacterAndLogs {
    weapon: Weapon, 
    characterId: number
}

const weaponIsMelee = (w: Weapon) =>  w.weaponType === WeaponType.Melee

const meleeWeapons = (weapons: Weapon[]) =>
    weapons.filter(weaponIsMelee)

const rangedWeapons = (weapons: Weapon[]) =>
    weapons.filter(w => !weaponIsMelee(w))

const RangedWeaponRow = ({weapon, characterId, updateLogs, updateCharacter}: WeaponProps) => {
    const isMelee = weaponIsMelee(weapon)
    const weaponIsGun: boolean = isGun(weapon.weaponType)
    const defaultAttackType = isMelee ? AttackType.Melee : AttackType.Single
    const ammoInfo = isMelee ? '' : `(${weapon.shotsLeft} / ${weapon.clipSize})`
    const [attackType, setAttackType] = useState<AttackType>(defaultAttackType)
    const isFullAuto: boolean = weaponIsGun && weapon.rof >= 3
    const isShotgunOrAutomatic = weaponIsGun && weapon.weaponType === WeaponType.Shotgun || weapon.rof >= 3
    const defaultTargets = isShotgunOrAutomatic ? 1 : undefined
    const [targets, setTargets] = useState<number | undefined>(defaultTargets)
    const defaultShotsFired = isFullAuto ? 1 : undefined
    const [shotsFired, setShotsFired] = useState<number | undefined>(defaultShotsFired)
    const [givenRoll, setGivenRoll] = useState(0)
    const [attackModifier, setAttackModifier] = useState(0)

    const AttackTypes = ({}) => 
        <span>
            <InputRow weapon={weapon} show={isMelee} onClick={() => setAttackType(AttackType.Melee)} checked={attackType === AttackType.Melee} label='Melee' />
            <InputRow weapon={weapon} show={!isMelee} onClick={() => setAttackType(AttackType.Single)} checked={attackType === AttackType.Single} label='*' />
            <InputRow weapon={weapon} show={isFullAuto} onClick={() => setAttackType(AttackType.Burst)} checked={attackType === AttackType.Burst} label='***' />
            <InputRow weapon={weapon} show={isFullAuto} onClick={() => setAttackType(AttackType.FullAuto)} checked={attackType === AttackType.FullAuto} label='A' />
        </span>

    const defaultAttackRange = weaponIsGun ? 10 : 1
    const [attackRange, setAttackRange] = useState(defaultAttackRange)

    const attackReq: AttackReq = {
        charId: characterId,
        weaponId: weapon.id,
        attackType,
        attackRange,
        attackModifier,
        targets,
        shotsFired,
        givenRoll
    }

    const removeWeaponReq: RemoveWeaponReq = {
        charId: characterId,
        weaponId: weapon.id
    }

    const reloadReq: ReloadReq = {
        weaponId: weapon.id,
        shots: weapon.clipSize
    }

    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter(characterId)
    }

    const updateTargets = (newVal: number) => updateNumWithLowerLimit(newVal, 1, setTargets)
    const updateShots = (newVal: number) => updateNumWithLowerLimit(newVal, 1, setShotsFired)
    const updateGivenRoll = (newVal: number) => updateNumWithLowerLimit(newVal, 0, setGivenRoll)
    const updateModifier = (newVal: number) => updateNumWithLowerLimit(newVal, 0, setAttackModifier) 
    
    return (
        <tr>
            <td>
                {weapon.item} {ammoInfo}
            </td>
            <td>
                {weapon.weaponType}
            </td>
            <td>
                <Dmg weapon={weapon}/>
            </td>
            <td>
                {weapon.reliability}
            </td>
            <td>
                <span className='attackMod'>
                    <button className='withLessRightSpace' onClick={() => attack(attackReq).then(updateLogsAndCharacter).then(() => {
                        setShotsFired(1)
                        setTargets(1)
                        setAttackModifier(0)
                        setGivenRoll(0)
                    })}>
                        Attack
                    </button>
                    {weaponIsGun && 
                        <button className='withLessRightSpace' onClick={() => reload(reloadReq).then(updateLogsAndCharacter)}>
                            Reload
                        </button>
                    }
                </span>
            </td>
            <td>
                <AttackTypes />
            </td>
            <td>
                <Range show={weaponIsGun || weapon.weaponType === WeaponType.Thrown} attackRange={attackRange} setAttackRange={setAttackRange}/>
            </td>
            <td>
                {isShotgunOrAutomatic && targets !== undefined && 
                    <span className='attackMod'>
                        {targets} <ValueChanger onChange={updateTargets} baseValue={targets} />
                    </span>
                }
            </td>
            <td>
                {isFullAuto && shotsFired && 
                    <span className='attackMod'>{shotsFired}<ValueChanger onChange={updateShots} baseValue={shotsFired}/> </span>
                }
            </td>
            <td>
                <span className='attackMod'>
                    <input value={givenRoll} className='valueBox' onChange={e => updateGivenRoll(parseInt(e.target.value))}/>
                </span>
                
            </td>
            <td>
                <span className='attackMod'>
                    {attackModifier} <ValueChanger onChange={updateModifier} baseValue={attackModifier} />
                </span>
            </td>
            <td>
                <button disabled={weapon.item === 'unarmed'} onClick={() => removeWeapon(removeWeaponReq).then(updateLogsAndCharacter)}>Remove</button>
            </td>
        </tr>
    )
}

interface CharacterWeaponsProps extends UpdateCharacterAndLogs{
    weapons: Weapon[]
    characterId: number
}

const CharacterRangedWeapons = (
    {weapons, characterId, updateLogs, updateCharacter}: CharacterWeaponsProps
) => {
    return (
        <table>
            <tbody>
                <tr>
                    <th>Ranged weapon</th>
                    <th>Type</th>
                    <th>DMG</th>
                    <th>Rel.</th>
                    <th>Action</th>
                    <th>Attack Type</th>
                    <th>Attack Range</th>
                    <th>(Opt. targets)</th>
                    <th>(Opt. #shots)</th>
                    <th>(Opt. Roll)</th>
                    <th>(Opt. Modifier)</th>
                    <th>Remove</th>
                </tr>
            </tbody>
            {weapons.map(w => 
                <RangedWeaponRow key={`${characterId} ${w.id}`} weapon={w} characterId={characterId} updateLogs={updateLogs} updateCharacter={updateCharacter} />
            )}
        </table>
    )
}

const MeleeWeaponRow = ({weapon, characterId, updateLogs, updateCharacter}: WeaponProps) => {
    const isMelee = weaponIsMelee(weapon)
    //ammoinfo for weapons with e.g. charges - electric baton etc.
    const ammoInfo = weapon.clipSize <= 1 ? '' : `(${weapon.shotsLeft} / ${weapon.clipSize})`
    const canBeReloaded: boolean = weapon.clipSize > 1
    const [givenRoll, setGivenRoll] = useState(0)
    const [attackModifier, setAttackModifier] = useState(0)
    const isUnarmed = weapon.item.toLowerCase() === 'unarmed'
    const defaultAttackMethod: MeleeAttackMethod = isUnarmed ? MeleeAttackMethod.strike : MeleeAttackMethod.weapon
    const [attackMethod, setAttackMethod] = useState<MeleeAttackMethod>(defaultAttackMethod)

    const updateModifier = (newVal: number) => updateNumWithLowerLimit(newVal, 0, setAttackModifier) 
    const updateGivenRoll = (newVal: number) => updateNumWithLowerLimit(newVal, 0, setGivenRoll)

    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter(characterId)
    }
    
    const removeWeaponReq: RemoveWeaponReq = {
        charId: characterId,
        weaponId: weapon.id
    }

    const reloadReq: ReloadReq = {
        weaponId: weapon.id,
        shots: weapon.clipSize
    }

    const attackReq: AttackReq = {
        charId: characterId,
        weaponId: weapon.id,
        attackType: AttackType.Melee,
        attackRange: 1,
        attackModifier,
        targets: undefined,
        shotsFired: undefined,
        givenRoll
    }

    const meleeDmgRollReq: MeleeDmgRollReq = {
        weaponId: weapon.id,
        charId: characterId,
        method: attackMethod
    }

    const AttackMethods = ({}) => 
        <span>
            <InputRow weapon={weapon} show={isUnarmed} onClick={() => setAttackMethod(MeleeAttackMethod.strike)} checked={attackMethod === MeleeAttackMethod.strike} label='Strike' />
            <InputRow weapon={weapon} show={isUnarmed} onClick={() => setAttackMethod(MeleeAttackMethod.kick)} checked={attackMethod === MeleeAttackMethod.kick} label='Kick' />
            <InputRow weapon={weapon} show={isUnarmed} onClick={() => setAttackMethod(MeleeAttackMethod.choke)} checked={attackMethod === MeleeAttackMethod.choke} label='Choke' />
            <InputRow weapon={weapon} show={!isUnarmed} onClick={() => setAttackMethod(MeleeAttackMethod.weapon)} checked={attackMethod === MeleeAttackMethod.weapon} label='Weapon' />
        </span>

    return (
        <tbody>
            <tr>
                <td>{weapon.item}</td>
                <td><Dmg weapon={weapon} /></td>
                <td>{weapon.reliability}</td>
                <td>
                    <span className='attackMod'>
                        <button className='withLessRightSpace' onClick={() => attack(attackReq).then(updateLogsAndCharacter).then(() => {
                            setAttackModifier(0)
                            setGivenRoll(0)
                        })}>
                            Attack
                        </button>
                        {canBeReloaded && 
                            <button className='withLessRightSpace' onClick={() => reload(reloadReq).then(updateLogsAndCharacter)}>
                                Reload
                            </button>
                        }
                    </span>
                </td>
                <td>
                    <button onClick={() => rollMeleeDmg(meleeDmgRollReq).then(updateLogsAndCharacter)}>Roll DMG</button>
                </td>
                <td><AttackMethods /></td>
                <td>{ammoInfo}</td>
                <td>
                    <span className='attackMod'>
                        <input value={givenRoll} className='valueBox' onChange={e => updateGivenRoll(parseInt(e.target.value))}/>
                    </span>
                </td>
                <td>
                    <span className='attackMod'>
                        {attackModifier} <ValueChanger onChange={updateModifier} baseValue={attackModifier} />
                    </span>
                </td>
                <td>
                    <button disabled={weapon.item === 'unarmed'} onClick={() => removeWeapon(removeWeaponReq).then(updateLogsAndCharacter)}>Remove</button>
                </td>
            </tr>
        </tbody>
    )
}

const CharacterMeleeWeapons = (
    {weapons, characterId, updateLogs, updateCharacter}: CharacterWeaponsProps
) => {
    return(
        <table>
            <tbody>
                <tr>
                    <th>Melee weapon</th>
                    <th>DMG</th>
                    <th>Reliability</th>
                    <th>Action</th>
                    <th>Roll DMG</th>
                    <th>Attack methods</th>
                    <th>(Opt. Shots left)</th>
                    <th>(Opt. Roll)</th>
                    <th>(Opt. Modifier)</th>
                    <th>Remove</th>
                </tr>
            </tbody>
            {weapons.map(w => 
                <MeleeWeaponRow key={`${characterId} ${w.id}`} weapon={w} characterId={characterId} updateLogs={updateLogs} updateCharacter={updateCharacter} />
            )}
        </table>
    )
}

interface CharacterArmorProps {
    characterId: number
    armors: Armor[] 
    updateLogsAndCharacter: (resLogs: Log[]) => void
}

interface ArmorRowProps {
    characterId: number
    armor: Armor
    updateLogsAndCharacter: (resLogs: Log[]) => void
}
const ArmorRow = ({armor, characterId, updateLogsAndCharacter}: ArmorRowProps) => {
    const removeArmorReq: RemoveArmorReq = {
        charId: characterId,
        armorId: armor.id
    }
    
    return (
        <tr>
            <td>
                {armor.item}
            </td>
            <td>
                {armor.sp}
            </td>
            <td>
                [{armor.bodyParts.join(', ')}]
            </td>
            <td>
                <button onClick={() => removeArmor(removeArmorReq).then(updateLogsAndCharacter)}>Remove [{armor.item}]</button>
            </td>
        </tr>
    )
}

const CharacterArmor = ({armors, updateLogsAndCharacter, characterId}: CharacterArmorProps) => {
    return(
        <table>
            <tbody>
                <tr>
                    <th>Armor</th>
                    <th>SP</th>
                    <th>Covers</th>
                    <th>Remove</th>
                </tr>
            </tbody>
            {armors.map(a => <ArmorRow key={'armor' + a.id} characterId={characterId} armor={a} updateLogsAndCharacter={updateLogsAndCharacter}/>)}
        </table>
    )
}

interface DmgSetterProps {
    bodyPart: BodyPart
    characterId: number,
    isAp: boolean
    passSp: boolean
    updateLogsAndCharacter: (l: Log[]) => void
}

const DmgSetter = ({characterId, bodyPart, isAp, passSp, updateLogsAndCharacter}: DmgSetterProps) => {
    const [dmg, setDmg] = useState(0)

    const updateDmg = (newVal: number) => updateNumWithLowerLimit(newVal, 0, setDmg)

    const dmgReq = {
        charId: characterId,
        bodyPart,
        dmg,
        isAp,
        passSp
    }

    const doDmgReq = () => 
        doDmg(dmgReq).then(logs => {
            setDmg(0)
            updateLogsAndCharacter(logs)
        })

    return( //FIX DMG
        <div className='dmgSetter'>
            <ValueChanger onChange={updateDmg} baseValue={dmg}/>
            <button className='dmgSetterButton' disabled={dmg === 0} 
            onClick={() => doDmgReq()}>{dmg} DMG</button>
        </div>
    )
}

interface ChromeRowProps {
    characterId: number
    chrome: Chrome
    updateLogsAndCharacter: (l: Log[]) => void
}

const ChromeRow = ({characterId, chrome, updateLogsAndCharacter}: ChromeRowProps) => {
    const removeReq: RemoveChromeReq = {
        charId: characterId,
        chromeId: chrome.id
    }
    return(
        <tr>
            <td>
                {chrome.item}
            </td>
            <td>
                {chrome.description}
            </td>
            <td>
                <button onClick={() => removeChrome(removeReq).then(updateLogsAndCharacter)}>Remove [{chrome.item}]</button>
            </td>
        </tr>

    )
}
    

interface CharacterChromeProps {
    characterId: number
    charChrome: Chrome[]
    updateLogsAndCharacter: (l: Log[]) => void
}

const CharacterChrome = ({characterId, charChrome, updateLogsAndCharacter}: CharacterChromeProps) => {
    return (
        <>
            <table>
                <tr>
                    <th>Cybernetic</th>
                    <th>Description</th>
                    <th>Remove</th>
                </tr>
                {charChrome.map(c => 
                    <ChromeRow key={'chrome' + c.id} characterId={characterId} chrome={c} updateLogsAndCharacter={updateLogsAndCharacter}/>
                )}
            </table>
        </>
    )
}

interface SPFieldProps extends UpdateCharacterAndLogs {
    characterId: number
    sp: CharacterSP
}

interface GridBoxProps {
    value: number | string
    bolden?: boolean
    otherValue?: number | string
    otherElement?: JSX.Element
}

const BoldenVal = ({value}: GridBoxProps) => 
    <div><b><i>{value}</i></b></div>

const GridBox = ({value, otherValue, bolden, otherElement}: GridBoxProps) => 
    <div className='sp'>
        <div>{!!bolden ? <BoldenVal value={value}/> : value}</div>
        {otherValue && !!bolden && <div><BoldenVal value={otherValue}/> </div>}
        {otherElement && <div>{otherElement}</div>}
    </div>

const CharacterSPField = ({sp, characterId, updateCharacter, updateLogs}: SPFieldProps) => {
    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter(characterId)
    }
    const Label = ({label}: {label: string}) => <label className='armorLabel'><i>{label}</i></label>

    const [isAp, setIsAp] = useState<boolean>(false)
    const [passSp, setPassSp] = useState<boolean>(false)

    const handleApCheckBox = () => {
        setIsAp(!isAp)
        setPassSp(false)
    }

    const handleSpCheckBox = () => {
        setIsAp(false)
        setPassSp(!passSp)
    }

    return(
        <div className='withVerticalSpace'>
            <div className='withVerticalSpace'>
                <input type='radio' checked={isAp} onClick={() => handleApCheckBox()}/> DMG is AP
                <input type='radio' checked={passSp} onClick={() => handleSpCheckBox()}/> DMG passes SP
            </div>
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
                    <GridBox value={sp.head} otherElement={<DmgSetter updateLogsAndCharacter={updateLogsAndCharacter} characterId={characterId} bodyPart={BodyPart.Head} isAp={isAp} passSp={passSp}/>}/>
                    <GridBox value={sp.body} otherElement={<DmgSetter updateLogsAndCharacter={updateLogsAndCharacter} characterId={characterId} bodyPart={BodyPart.Body} isAp={isAp} passSp={passSp}/>}/>
                    <GridBox value={sp.r_arm} otherElement={<DmgSetter updateLogsAndCharacter={updateLogsAndCharacter} characterId={characterId} bodyPart={BodyPart.R_arm} isAp={isAp} passSp={passSp}/>}/>
                    <GridBox value={sp.l_arm} otherElement={<DmgSetter updateLogsAndCharacter={updateLogsAndCharacter} characterId={characterId} bodyPart={BodyPart.L_arm} isAp={isAp} passSp={passSp}/>}/>
                    <GridBox value={sp.r_leg} otherElement={<DmgSetter updateLogsAndCharacter={updateLogsAndCharacter} characterId={characterId} bodyPart={BodyPart.R_leg} isAp={isAp} passSp={passSp}/>}/>
                    <GridBox value={sp.l_leg} otherElement={<DmgSetter updateLogsAndCharacter={updateLogsAndCharacter} characterId={characterId} bodyPart={BodyPart.L_leg} isAp={isAp} passSp={passSp}/>}/>
                </div>
                <button className='withLeftSpace' onClick={() => repair(characterId).then(updateLogsAndCharacter)}>Repair</button>
            </span>
        </div>
    )
}

interface FourDmgBoxesProps {
    upper: string
    lower: string
    boxesTicked: number
}

const FourDmgBoxes = ({upper, lower, boxesTicked}: FourDmgBoxesProps) => {
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
                    return <div key={'dmg'} className='dmgBoxSet'>{arr}</div>;
                })()}
        </>
       <div className='dmgStun'>{lower}</div>
    </div>
    )
}

interface SaveAndHealthProps extends UpdateCharacterAndLogs{
    character: Character
    edit: boolean
    randomize: boolean
    updateCharacterBTM: (n: number) => void
}

const SaveAndHealthRow = ({character, updateCharacter, updateLogs, edit, randomize, updateCharacterBTM}: SaveAndHealthProps) => {
    const { dmgTaken } = character
    const save = character.attributes.BODY
    const btm = character.btm
    
    const leftOver = dmgTaken % 4

    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter(character.id)
    }

    const resolveTicks = (lowerLimit:number, upperLimit: number): number => 
        dmgTaken > lowerLimit ? (dmgTaken >= upperLimit ? 4 : leftOver) : 0
    
    const [healAmount, setHealAmount] = useState(1)

    const healReq = {
        charId: character.id,
        amount: healAmount
    }

    const btmByValue = (btm: number) => {
        switch(btm) {
            case 0:
                return 'V. Weak'
            case 1:
                return 'Weak'
            case 2:
                return 'Average'
            case 3:
                return 'Strong'
            case 4:
                return 'V. strong'
            default:
                return 'Superhuman'
        }
    }


    return(
        <div className='boxContainer'>
             <div className='outerBox'>
                    <div className='boxLabel'>Save</div>
                    <div className='boxValueFlex'>{save}</div>
                </div>
                <div className='outerBox'>
                    <div className='boxLabel'>BTM</div>
                    <div className='boxValue'>
                        <div className='boxValueFlex'>
                            {-1 * btm}
                            {edit && !randomize &&
                                <ValueChanger onChange={updateCharacterBTM} baseValue={btm}/>
                            }
                        </div>
                    </div>
                    <div className='btmLabel'>{btmByValue(btm)}</div>
                </div>
                {!edit && <div className='withMoreLeftSpace'>
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
                    <div className='healContainer'>
                        <ValueChanger onChange={setHealAmount} baseValue={healAmount}/>
                        <button onClick={() => {
                            heal(healReq).then(updateLogsAndCharacter)
                            setHealAmount(1)
                        }}>
                            Heal {healAmount}
                        </button>
                        <button className='withLeftSpace' onClick={() => stuncheck({charId: character.id}).then(updateLogsAndCharacter)}>Stun check</button>
                    </div>
                </div>}
        </div>
    )
}

interface HandleProps {
    characterId?: number
    value: string
    edit: boolean
    onUpdate: (n: string) => void
    updateLogsAndCharacter: (l: Log[]) => void
}

const Handle = ({characterId, value, edit, onUpdate, updateLogsAndCharacter}: HandleProps) => {
    const [nameEditable, setNameEditable] = useState(false)

    const updateName = (charId: number) => 
        updateCharacterName({charId, name: value})

    return(
        <div className='fieldContainer'>
            <span className='fieldContent'>
                <label>Handle</label>
                <input disabled={!edit && !nameEditable} className='fieldValue' value={value} onChange={e => onUpdate(e.target.value)} />
            </span>
            {characterId && <span>
                <input type='checkbox' checked={nameEditable} onClick={() => setNameEditable(!nameEditable)}/> Edit handle
                <button disabled={!nameEditable} onClick={() => updateName(characterId).then(updateLogsAndCharacter)} className='withLeftSpace'>Update handle</button>
            </span>
            }
        </div>
    )
}

export interface CharacterSheetProps extends UpdateCharacterAndLogs{
    edit: boolean
    character: Character
    allSkills?: Skill[]
    editCharacter?: (c: Character) => void
    allowAddingToInitiative: boolean
    updateCharacterList: () => Promise<void>
}


const CharacterSheet = ({edit, updateCharacterList, character, allSkills, updateLogs, updateCharacter, editCharacter, allowAddingToInitiative}: CharacterSheetProps) => {
    const editCharacterInForm = (newCharacter: Character, isValid: boolean) => 
        editCharacter && isValid && editCharacter(newCharacter)
    
    const isBetween = (lowerLimit: number, value: number, upperLimit: number) =>
        lowerLimit <= value && value <= upperLimit

    const updateCharacterName = (newName: string) => {
        const {name, ...rest} = character
        const newCharacter: Character = {name: newName, ...rest}

        editCharacterInForm(newCharacter, true)
    }

    const updateCharacterRole = (newRole: string) => {
        const {role, ...rest} = character
        const newCharacter: Character = {role: newRole, ...rest}

        editCharacterInForm(newCharacter, true)
    }

    const characterAttributesValid = (c: Character): boolean => {
        const attributes = c.attributes
        const validAttributes = [
            isBetween(1, attributes.ATTR, 10),
            isBetween(1, attributes.BODY, 10),
            isBetween(1, attributes.COOL, 10),
            isBetween(1, attributes.EMP, 10),
            isBetween(1, attributes.INT, 10),
            isBetween(1, attributes.LUCK, 10),
            isBetween(1, attributes.MA, 10),
            isBetween(1, attributes.REF, 10),
            isBetween(1, attributes.TECH, 10),
        ]

        return validAttributes.every(v => v === true)
    }

    const [randomize, setRandomize] = useState(false)

    const updateCharacterAttributes = (newAttributes: Attributes) => {
        const {attributes, ...rest} = character
        const newCharacter: Character = {attributes: newAttributes, ...rest}
        const attributesAreValid = characterAttributesValid(newCharacter)

        editCharacterInForm(newCharacter, attributesAreValid)
    }

    const updateCharacterBTM = (newBtm: number) => {
        const {btm, ...rest} = character
        const newCharacter: Character = {btm: newBtm, ...rest}

        editCharacterInForm(newCharacter, isBetween(0, newBtm, 4))
    }

    const roleAndNameIsValid = (): boolean =>
        character.role != '' && character.name != ''

    const saveCharacterFormValid = (): boolean =>
        randomize ? true : edit && characterAttributesValid(character) && roleAndNameIsValid()

    const SaveNewCharacter = ({}) => {
        const createReq: CreateCharacterReq = {
            name: character.name,
            role: character.role,
            attributes: character.attributes,
            btm: character.btm,
            randomize
        }

        const createCharacterAndLog = () => 
            createCharacter(createReq).then(res => {
                updateLogs(res.logs)
                updateCharacter(res.charId).then(() => updateCharacterList())
            })
        return (
            <div className='withLeftSpace'>
                <button 
                onClick={() => {
                    createCharacterAndLog()
                }} 
                disabled={!saveCharacterFormValid()}
                className='withLeftSpace'>
                    Create character
                </button>
            </div>
        )
    }

    const updateLogsAndCharacter = (l: Log[]) => {
        updateLogs(l)
        updateCharacter(character.id)
    }

    const editWithRandomize = edit && !randomize

    return(
        <div className='sheet'>
            <Handle updateLogsAndCharacter={updateLogsAndCharacter} characterId={character.id} edit={edit} value={character.name} onUpdate={updateCharacterName}/>
            {edit && <><input type="checkbox" checked={randomize} onClick={() => setRandomize(!randomize)}/> Randomize</>}
            <RoleFiled updateChracterRole={updateCharacterRole} edit={editWithRandomize} value={character.role}/>
             <Stats characterId={character.id} edit={edit} updateCharacter={updateCharacter} updateLogs={updateLogs} updateCharacterAttributes={updateCharacterAttributes} attributes={character.attributes}/>
            {!edit && <CharacterSPField sp={character.sp} characterId={character.id} updateCharacter={updateCharacter} updateLogs={updateLogs}/>}
            <SaveAndHealthRow updateCharacterBTM={updateCharacterBTM} randomize={randomize} edit={edit} character={character} updateCharacter={updateCharacter} updateLogs={updateLogs}/>
            {edit && <SaveNewCharacter />}
            {allSkills && !edit && <SkillsByAttributes updateLogs={updateLogs} skills={allSkills} character={character} updateCharacter={updateCharacter}/>}
            {!edit &&
                <>
                    <AddWeapon characterId={character.id} updateLogsAndCharacter={updateLogsAndCharacter}/>
                    <CharacterMeleeWeapons  weapons={meleeWeapons(character.weapons)} characterId={character.id} updateLogs={updateLogs} updateCharacter={updateCharacter}/>
                    <CharacterRangedWeapons weapons={rangedWeapons(character.weapons)} characterId={character.id} updateLogs={updateLogs} updateCharacter={updateCharacter}/>
                    {allSkills && <AddArmor allSkills={allSkills} characterId={character.id} updateLogsAndCharacter={updateLogsAndCharacter}/>}
                    <CharacterArmor armors={character.armor} updateLogsAndCharacter={updateLogsAndCharacter} characterId={character.id}/>
                    <AddChrome allSkills={allSkills ?? []} characterId={character.id} updateLogsAndCharacter={updateLogsAndCharacter}/>
                    <CharacterChrome updateLogsAndCharacter={updateLogsAndCharacter} characterId={character.id} charChrome={character.chrome}/>
                </>
            }
        </div>
    )
}

export default CharacterSheet

/** if one wants to include image..? (replace Handle-Stats)
        <div className='fieldContent'>
            <div>
                <Handle allowAddingToInitiative={allowAddingToInitiative} updateLogsAndCharacter={updateLogsAndCharacter} characterId={character.id} edit={edit} value={character.name} onUpdate={updateCharacterName}/>
                <RoleFiled updateChracterRole={updateCharacterRole} edit={edit} value={character.role}/>
                <Stats edit={edit} updateCharacterAttributes={updateCharacterAttributes} attributes={character.attributes}/>
            </div>
            <div className='image'>
                <div >
                 //image uploading stuff here
                </div>
                
            </div>
            <button>Add image</button>
        </div>
 */