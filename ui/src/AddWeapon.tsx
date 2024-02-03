import { useEffect, useMemo, useState } from 'react'
import './AddWeapon.css'
import { AddWeaponReq, Con, Log, Reliability, WeaponType, addWeapon } from './CyberClient'
import Hideable from './Hideable'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'
import { Button } from './Common'


const basicSMGTemplate = (charId: number): AddWeaponReq => {
    return (
        {
            charId,
            item: 'SMG',
            die: 6,
            dice: 2,
            dmgBonus: 0,
            weaponType: WeaponType.SMG,
            divideBy: 1,
            rof: 30,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.Jacket,
            weight: 2,
            humanityCost: 0,
            effectRadius: 0,
            clipSize: 30,
            customRange: undefined
        }
    ) 
}

const basicRifleTemplate = (charId: number): AddWeaponReq => {
    return (
        {
            charId,
            item: 'Rifle',
            die: 6,
            dice: 4,
            dmgBonus: 0,
            weaponType: WeaponType.Rifle,
            divideBy: 1,
            rof: 30,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.LongJacket,
            weight: 4,
            humanityCost: 0,
            effectRadius: 0,
            clipSize: 30,
            customRange: undefined
        }
    )
}

const basicMeleeTemplate = (charId: number): AddWeaponReq => {
    return (
        {
            charId,
            item: 'Melee',
            die: 6,
            dice: 2,
            dmgBonus: 0,
            weaponType: WeaponType.Melee,
            divideBy: 1,
            rof: 1,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.Jacket,
            weight: 2,
            humanityCost: 0,
            effectRadius: 0,
            clipSize: 1,
            customRange: undefined
        }
    )
}

const basicHandgunTemplate = (charId: number): AddWeaponReq => {
    return (
        {
            charId,
            item: 'Handgun',
            die: 6,
            dice: 2,
            dmgBonus: 0,
            weaponType: WeaponType.Handgun,
            divideBy: 1,
            rof: 2,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.Pocket,
            weight: 2,
            humanityCost: 0,
            effectRadius: 0,
            clipSize: 1,
            customRange: undefined
        }
    )
}

const basicHeavyTemplate = (charId: number): AddWeaponReq => {
    return (
        {
            charId,
            item: 'Heavy',
            die: 6,
            dice: 6,
            dmgBonus: 0,
            weaponType: WeaponType.Heavy,
            divideBy: 1,
            rof: 2,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.NotHideable,
            weight: 5,
            humanityCost: 0,
            effectRadius: 0,
            clipSize: 1,
            customRange: undefined
        }
    )
}

const basicThrownTemplate = (charId: number): AddWeaponReq => {
    return (
        {
            charId,
            item: 'Thrown',
            die: 6,
            dice: 4,
            dmgBonus: 0,
            weaponType: WeaponType.Thrown,
            divideBy: 1,
            rof: 2,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.Jacket,
            weight: 2,
            humanityCost: 0,
            effectRadius: 3,
            clipSize: 1,
            customRange: undefined
        }
    )
}

const basicShotgunTemplate = (charId: number): AddWeaponReq => {
    return (
        {
            charId,
            item: 'Shotgun',
            die: 6,
            dice: 4,
            dmgBonus: 0,
            weaponType: WeaponType.Shotgun,
            divideBy: 1,
            rof: 1,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.LongJacket,
            weight: 2,
            humanityCost: 0,
            effectRadius: 3,
            clipSize: 1,
            customRange: undefined
        }
    )
}


interface AddWeaponProps {
    characterId: number
    updateLogsAndCharacter: (logs: Log[]) => void
}

const NewWeaponForm = ({characterId, updateLogsAndCharacter}: AddWeaponProps) => {
    const addWeaponReqBasic: AddWeaponReq = useMemo(() => {
        return {
            charId: characterId,
            item: '',
            die: 6,
            dice: 1,
            dmgBonus: 1,
            weaponType: WeaponType.Melee,
            divideBy: 1,
            rof: 1,
            wa: 0,
            reliability: Reliability.Standard,
            con: Con.Pocket,
            weight: 1,
            humanityCost: 0,
            effectRadius: 0,
            clipSize: 1,
            customRange: 0
        }
    }, [characterId])

    const [weapon, setWeapon] = useState(addWeaponReqBasic)

    const emptyForm = () => {
        setWeapon(addWeaponReqBasic)
    }

    const updateDiceNum = (v: number) => updateNumWithLowerLimit(v, 1, (i: number) => setWeapon({...weapon, dice: i}))
    const updateDie = (v: number) => updateNumWithLowerLimit(v, 1, (i: number) => setWeapon({...weapon, die: i}))
    const updateDmgBonus = (v: number) => updateNumWithLowerLimit(v, 0, (i: number) => setWeapon({...weapon, dmgBonus: i}))
    const updateClipSize = (v: number) => updateNumWithLowerLimit(v, 1, (i: number) => setWeapon({...weapon, clipSize: i}))
    const updateHlCost = (v: number) => updateNumWithLowerLimit(v, 0, (i: number) => setWeapon({...weapon, humanityCost: i}))
    const updateWa = (v: number) => updateNumWithLowerLimit(v, -5, (i: number) => setWeapon({...weapon, wa: i}))
    const updateEffectRadius = (v: number) => updateNumWithLowerLimit(v, 0, (i: number) => setWeapon({...weapon, effectRadius: i}))
    const updateDivideBy = (v: number) => updateNumWithLowerLimit(v, 1, (i: number) => setWeapon({...weapon, divideBy: i}))
    const updateRof = (v: number) => updateNumWithLowerLimit(v, 1, (i: number) => setWeapon({...weapon, rof: i}))
    const updateWeight = (v: number) => updateNumWithLowerLimit(v, 1, (i: number) => setWeapon({...weapon, weight: i}))


    useEffect(() => {
        setWeapon(addWeaponReqBasic)
    }, [addWeaponReqBasic])


    interface FormRowWithValueChangerProps {
        value: number | string
        baseValue: number
        onChange: (i: number) => void
    }

    const FormRowWithValueChanger = ({value, baseValue, onChange}: FormRowWithValueChangerProps) => 
        <span className='attackMod'>{value}<ValueChanger onChange={onChange} baseValue={baseValue}/></span>

    return(
        <table>
            <tr>
                <th>Add weapon</th>
                <th>Item</th>
                <th>Type</th>
                <th># Dice</th>
                <th>D Die</th>
                <th>(Opt. Div)</th>
                <th>Dmg bonus</th>
                <th>ROF</th>
                <th>WA</th>
                <th>Clip size</th>
                <th>Rel.</th>
                <th>CON</th>
                <th>Weight</th>
                <th>Effect radius</th>
                <th>(Opt. range)</th>
                <th>(Opt. HL cost)</th>
            </tr>
            <tr>
                <td>
                    <Button label='Add' onClick={() => addWeapon(weapon).then(updateLogsAndCharacter).then(emptyForm)}/>
                </td>
                <td>
                    <input className='inputField' value={weapon.item} onChange={e => setWeapon({...weapon, item: e.target.value})}/>
                </td>
                <td>
                    <select>
                        <option value={WeaponType.Melee} onClick={() => setWeapon(basicMeleeTemplate(characterId))}>Melee</option>
                        <option value={WeaponType.Handgun} onClick={() => setWeapon(basicHandgunTemplate(characterId))}>Handgun</option>
                        <option value={WeaponType.SMG} onClick={() => setWeapon(basicSMGTemplate(characterId))}>SMG</option>
                        <option value={WeaponType.Rifle} onClick={() => setWeapon(basicRifleTemplate(characterId))}>Rifle</option>
                        <option value={WeaponType.Shotgun} onClick={() => setWeapon(basicShotgunTemplate(characterId))}>Shotgun</option>
                        <option value={WeaponType.Thrown} onClick={() => setWeapon(basicThrownTemplate(characterId))}>Thrown</option>
                        <option value={WeaponType.Heavy} onClick={() => setWeapon(basicHeavyTemplate(characterId))}>Heavy</option>
                    </select>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDiceNum} value={weapon.dice} baseValue={weapon.dice}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDie} value={`D${weapon.die}`} baseValue={weapon.die}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDivideBy} value={`/${weapon.divideBy}`} baseValue={weapon.divideBy}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDmgBonus} value={`+${weapon.dmgBonus}`} baseValue={weapon.dmgBonus}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateRof} value={weapon.rof} baseValue={weapon.rof}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateWa} value={weapon.wa} baseValue={weapon.wa}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateClipSize} value={weapon.clipSize} baseValue={weapon.clipSize}/>
                </td>
                <td>
                    <select>
                        <option value={Reliability.Standard} onClick={() => setWeapon({...weapon, reliability: Reliability.Standard})}>ST</option>
                        <option value={Reliability.VeryReliable} onClick={() => setWeapon({...weapon, reliability: Reliability.VeryReliable})}>VR</option>
                        <option value={Reliability.Unreliable} onClick={() => setWeapon({...weapon, reliability: Reliability.Unreliable})}>UR</option>
                    </select> 
                </td>
                <td>
                    <select>
                        <option value={Con.Pocket} onClick={() => setWeapon({...weapon, con: Con.Pocket})}>P</option>
                        <option value={Con.Jacket} onClick={() => setWeapon({...weapon, con: Con.Jacket})}>J</option>
                        <option value={Con.LongJacket} onClick={() => setWeapon({...weapon, con: Con.LongJacket})}>L</option>
                        <option value={Con.NotHideable} onClick={() => setWeapon({...weapon, con: Con.NotHideable})}>N</option>
                    </select>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateWeight} value={`${weapon.weight}kg`} baseValue={weapon.weight}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateEffectRadius} value={weapon.effectRadius} baseValue={weapon.effectRadius}/>
                </td>
                <td>
                     <input placeholder={'0'} className='shortInput' value={weapon.customRange} onChange={e => 
                        setWeapon({...weapon, customRange: parseInt(e.target.value) || 0})
                    }/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateHlCost} value={weapon.humanityCost} baseValue={weapon.humanityCost}/>
                </td>
            </tr>
        </table>
    )
}

export const AddWeapon = ({characterId, updateLogsAndCharacter}: AddWeaponProps) => 
    <div className='form'>
        <Hideable text='weapon form' props={<NewWeaponForm characterId={characterId} updateLogsAndCharacter={updateLogsAndCharacter}/>}/>
    </div>