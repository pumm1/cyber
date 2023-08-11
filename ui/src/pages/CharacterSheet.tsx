import { Character, Attributes, listSkills, Skill, CharacterSkill, Attribute, CharacterSP, rollSkill, Weapon, attack, AttackReq, AttackType, isGun, ReloadReq, reload, Log, WeaponType, repair, lvlUp, heal, RollSkillReq, doDmg, BodyPart, createCharacter, CreateCharacterReq, Chrome, UpdateIPReq, updateIP } from './CyberClient'
import React, { useState } from "react"
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

//TODO:
//tallenna IP..?
//FA toimimaan
//opt LUCK skilleihin
//thrown toimimaan?

interface UpdateCharacter {
    updateCharacter: () => Promise<void>
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

interface ValueChangerProps {
    baseValue: number
    onChange: (i: number) => void
}

const ValueChanger = ({onChange, baseValue}: ValueChangerProps) =>
    <div className='trianglesSet'>
        <a onClick={() => onChange(baseValue + 1)}>
            <div className="triangleUp"></div>
        </a>
        <a onClick={() =>  onChange(baseValue - 1)}>
            <div className="triangleDown"></div>
        </a>
    </div>

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


interface StatsProps {
    attributes: Attributes
    updateCharacterAttributes: (a: Attributes) => void
    edit: boolean
}

const Stats = ( {attributes, updateCharacterAttributes, edit}: StatsProps) => {
    
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
    updateCharacter: () => Promise<void>
}

interface SkillRowProps extends UpdateCharacter {
    charId: number
    rollSkill: (r: RollSkillReq) => Promise<number>
    skill: Skill
    charSkillLvl: number
    roll: RollSkillReq
}

const SkillRow = ({skill, charSkillLvl, roll, charId, updateCharacter}: SkillRowProps) => {
    const [rollResult, setRollResult] = useState<undefined | number>(undefined)
    return(
        <div className='skill' key={skill.id}>
            <span>
                {<button className='skillBtn' disabled={charSkillLvl >= 10 } onClick={() => lvlUp(charId, skill.id).then(updateCharacter)}>+</button>}
                <button className='skillBtn' onClick={() => rollSkill(roll).then(res => setRollResult(res))}>Roll</button>
                {skill.skill.padEnd(30, '.')}[{charSkillLvl ?? ''}]
                {rollResult && <>({rollResult})</>}
            </span>
        </div>
    )
}

const SkillRowByCharacterSkills = ({skill, characterSkills, charId, updateCharacter}: SkillProps) => {
    const charSkillLvl = characterSkills.find(s => s.id === skill.id)?.lvl ?? 0
    const roll: RollSkillReq = {
        charId: charId,
        skillId: skill.id,
        addedLuck: 0
    }

    return (
        <SkillRow charSkillLvl={charSkillLvl} updateCharacter={updateCharacter} skill={skill} charId={charId} rollSkill={rollSkill} roll={roll} />
    )
}

interface SkillsProps extends UpdateCharacterAndLogs {
    skills: Skill[]
    character: Character
}

interface SkillsByAttributeProps extends SkillsProps{
    attribute: Attribute
    characterSkills: CharacterSkill[]
}

const SkillsByAttribute = ({attribute, skills, characterSkills, character, updateCharacter}: SkillsByAttributeProps) => 
    <span key={attribute}>
        <b>{attribute}</b>
        {skills.filter(s => s.attribute === attribute).map(s => <SkillRowByCharacterSkills skill={s} characterSkills={characterSkills} charId={character.id} updateCharacter={updateCharacter}/>)}
    </span>

const SkillsByAttributes = ({skills, character, updateCharacter, updateLogs}: SkillsProps ) => {
    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter()
    }

    const spceialSkill: Skill = {
        skill: character.specialAbility,
        attribute:  Attribute.REF, //TODO
        description: '', //TODO
        id: 0
    }

    const specialRollReq: RollSkillReq = {
        charId: character.id,
        skillId: spceialSkill.id,
        addedLuck: 0
    }
    const [ipToAdd, setIpToadd] = useState(0)

    const ipReq: UpdateIPReq = {
        charId: character.id,
        ipAmount: ipToAdd
    }
    const updateIp = () => {
        updateIP(ipReq).then(updateLogsAndCharacter).then(() => setIpToadd(0))
    }

   return (
    <>
        <label>Skills</label>
        <div className='fieldContainer'>
            <div className='skills'>
                <span>
                    <b>Special ability</b>
                    <SkillRow roll={specialRollReq} charId={character.id} updateCharacter={updateCharacter} rollSkill={rollSkill} charSkillLvl={character.specialAbilityLvl} skill={spceialSkill} />
                </span>
                {attributesInOrder.map(atr => <SkillsByAttribute updateCharacter={updateCharacter} updateLogs={updateLogs} attribute={atr} skills={skills} characterSkills={character.skills} character={character}/>)}
                <StatValue field='REP' value={2}/>
                <span className='ipToAdd'>
                    <StatValue field='Current IP' value={character.ip}/>
                    ({ipToAdd})
                    <ValueChanger onChange={setIpToadd} baseValue={ipToAdd} />
                    <button className='ipButton' disabled={ipToAdd === 0} onClick={updateIp}>Change IP</button>
                </span>
                <StatValue field='Humanity' value={character.humanity}/>
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
        weaponIsGun && <><input className='range' type='text' disabled={false} value={attackRange} onChange={e => setAttackRange(parseInt(e.target.value) || 0)}/></>

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
    const isShotgunOrAutomatic = weaponIsGun && weapon.weaponType === WeaponType.Shotgun || weapon.rof >= 3
    const defaultTargets = isShotgunOrAutomatic ? 1 : undefined
    const [targets, setTargets] = useState<number | undefined>(defaultTargets)

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
        attackRange,
        attackModifier: 0, //TODO
        targets
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
        <tr>
            <td>
                {weapon.item} {ammoInfo}
            </td>
            <td>
                {weapon.weaponType}
            </td>
            <td>
                <Dmg/>
            </td>
            <td>
                <button className='weaponButton' onClick={() => attack(attackReq).then(updateLogsAndCharacter)}>Attack</button>
            </td>
            <td>
                <AttackTypes />
                {weaponIsGun && 
                    <button className='weaponButton' onClick={() => reload(reloadReq).then(updateLogsAndCharacter)}>
                        Reload
                    </button>
                 }
            </td>
            <td>
                <Range weaponIsGun={weaponIsGun} attackRange={attackRange} setAttackRange={setAttackRange}/>
            </td>
            <td>
                {isShotgunOrAutomatic && targets !== undefined && <span className='targets'>{targets} <ValueChanger onChange={setTargets} baseValue={targets} /></span>}
            </td>
        </tr>
    )
}

interface CharacterWeaponsProps extends UpdateCharacterAndLogs{
    weapons: Weapon[]
    characterId: number
}

const CharacterWeapons = (
    {weapons, characterId, updateLogs, updateCharacter}: CharacterWeaponsProps
) => {
    return (
        <>
            <table>
                <tr>
                    <th>Weapon</th>
                    <th>Type</th>
                    <th>DMG</th>
                    <th>Action</th>
                    <th>Attack Type</th>
                    <th>Attack Range</th>
                    <th>(Optional: Targets)</th>
                </tr>
                {weapons.map(w => 
                    <WeaponRow key={`${characterId} ${w.id}`} weapon={w} characterId={characterId} updateLogs={updateLogs} updateCharacter={updateCharacter} />
                )}
            </table>
        </>
    )
}



interface ChromeRowProps {
    chrome: Chrome
}

const ChromeRow = ({chrome}: ChromeRowProps) =>
    <tr>
        <td>
            {chrome.item}
        </td>
        <td>
            {chrome.description}
        </td>
    </tr>


interface CharacterChromeProps {
    charChrome: Chrome[]
}

const CharacterChrome = ({charChrome}: CharacterChromeProps) => {
    return (
        <>
            <table>
                <tr>
                    <th>Cybernetic</th>
                    <th>Description</th>
                </tr>
                {charChrome.map(c => 
                    <ChromeRow chrome={c}/>
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

const CharacterSPField = ({sp, characterId, updateCharacter, updateLogs}: SPFieldProps) => {
    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter()
    }
    const Label = ({label}: {label: string}) => <label className='armorLabel'><i>{label}</i></label>
    const BoldenVal = ({value}: GridBoxProps) => 
        <div><b><i>{value}</i></b></div>

    interface DmgSetterProps {
        bodyPart: BodyPart
    }

    const DmgSetter = ({bodyPart}: DmgSetterProps) => {
        const [dmg, setDmg] = useState(0)

        const updateDmg = (newVal: number) => {
            if (newVal >= 0) {
                setDmg(newVal)
            }
        }

        const dmgReq = {
            charId: characterId,
            bodyPart,
            dmg
        }

        return( //FIX DMG
            <div className='dmgSetter'>
                <ValueChanger onChange={updateDmg} baseValue={dmg}/>
                <button className='dmgSetterButton' disabled={dmg === 0} onClick={() => doDmg(dmgReq).then(logs => {
                    setDmg(0)
                    updateLogsAndCharacter(logs)
                })}>{dmg} DMG</button>
            </div>
        )
    }


    const GridBox = ({value, otherValue, bolden, otherElement}: GridBoxProps) => 
        <div className='sp'>
            <div>{!!bolden ? <BoldenVal value={value}/> : value}</div>
            {otherValue && !!bolden && <div><BoldenVal value={otherValue}/> </div>}
            {otherElement && <div>{otherElement}</div>}
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
                    <GridBox value={sp.head} otherElement={<DmgSetter bodyPart={BodyPart.Head}/>}/>
                    <GridBox value={sp.body} otherElement={<DmgSetter bodyPart={BodyPart.Body}/>}/>
                    <GridBox value={sp.r_arm} otherElement={<DmgSetter bodyPart={BodyPart.R_arm}/>}/>
                    <GridBox value={sp.l_arm} otherElement={<DmgSetter bodyPart={BodyPart.L_arm}/>}/>
                    <GridBox value={sp.r_leg} otherElement={<DmgSetter bodyPart={BodyPart.R_leg}/>}/>
                    <GridBox value={sp.l_leg} otherElement={<DmgSetter bodyPart={BodyPart.L_leg}/>}/>
                </div>
                <button className='repair' onClick={() => repair(characterId).then(updateLogsAndCharacter)}>Repair</button>
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
                    return <div className='dmgBoxSet'>{arr}</div>;
                })()}
        </>
       <div className='dmgStun'>{lower}</div>
    </div>
    )
}

interface SaveAndHealthProps extends UpdateCharacterAndLogs{
    character: Character
    edit: boolean
    updateCharacterBTM: (n: number) => void
}

const SaveAndHealthRow = ({character, updateCharacter, updateLogs, edit, updateCharacterBTM}: SaveAndHealthProps) => {
    const { dmgTaken } = character
    const save = character.attributes.BODY
    const btm = character.btm
    
    const leftOver = dmgTaken % 4

    const updateLogsAndCharacter = (resLogs: Log[]) => {
        updateLogs(resLogs)
        updateCharacter()
    }

    const resolveTicks = (lowerLimit:number, upperLimit: number): number => 
        dmgTaken > lowerLimit ? (dmgTaken >= upperLimit ? 4 : leftOver) : 0
    
    const [healAmount, setHealAmount] = useState(1)

    const healReq = {
        charId: character.id,
        amount: healAmount
    }

    return(
        <div className='boxContainer'>
             <div className='outerBox'>
                    <div className='boxLabel'>Save</div>
                    <div className='boxValue'>{save}</div>
                </div>
                <div className='outerBox'>
                    <div className='boxLabel'>BTM</div>
                    <div className='boxValue'>
                        {btm}
                        {edit &&
                            <ValueChanger onChange={updateCharacterBTM} baseValue={btm}/>
                        }
                    </div>
                </div>
                {!edit && <div className='dmgTakenContainer'>
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
                    </div>
                </div>}
        </div>
    )
}

interface TextFieldProps {
    fieldName: string
    value: string
    edit: boolean
    onUpdate: (n: string) => void 
}

const TextField = ({fieldName, value, edit, onUpdate}: TextFieldProps) => {
    return(
        <div className='fieldContainer'>
            <span className='fieldContent'>
                <label>{fieldName}</label>
                <input disabled={!edit} className='fieldValue' value={value} onChange={e => onUpdate(e.target.value)} />
            </span>
        </div>
    )
}

export interface CharacterSheetProps extends UpdateCharacterAndLogs{
    edit: boolean
    character: Character
    allSkills?: Skill[]
    editCharacter?: (c: Character) => void
}


const CharacterSheet = ({edit, character, allSkills, updateLogs, updateCharacter, editCharacter}: CharacterSheetProps) => {
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
        edit && characterAttributesValid(character) && roleAndNameIsValid()

    const SaveNewCharacter = ({}) => {
        const createReq: CreateCharacterReq = {
            name: character.name,
            role: character.role,
            attributes: character.attributes,
            btm: character.btm,
            randomize: false
        }

        const createCharacterAndLog = () => 
            createCharacter(createReq).then(updateLogs)
        return (
            <div className='saveCharacter'>
                <button onClick={() => createCharacterAndLog()} disabled={!saveCharacterFormValid()}className='saveCharacterBtn'>Create character</button>
            </div>
        )
    }
        

    return(
        <div className='sheet'>
            <TextField edit={edit} fieldName='HANDLE' value={character.name} onUpdate={updateCharacterName}/>
            <RoleFiled updateChracterRole={updateCharacterRole} edit={edit} value={character.role}/>
            <Stats edit={edit} updateCharacterAttributes={updateCharacterAttributes} attributes={character.attributes}/>
            {!edit && <CharacterSPField sp={character.sp} characterId={character.id} updateCharacter={updateCharacter} updateLogs={updateLogs}/>}
            <SaveAndHealthRow updateCharacterBTM={updateCharacterBTM} edit={edit} character={character} updateCharacter={updateCharacter} updateLogs={updateLogs}/>
            {edit && <SaveNewCharacter />}
            {allSkills && !edit && <SkillsByAttributes updateLogs={updateLogs} skills={allSkills} character={character} updateCharacter={updateCharacter}/>}
            <CharacterWeapons weapons={character.weapons} characterId={character.id} updateLogs={updateLogs} updateCharacter={updateCharacter}/>
            <CharacterChrome charChrome={character.chrome}/>
        </div>
    )
}

export default CharacterSheet