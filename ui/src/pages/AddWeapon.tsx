import React, { useState } from 'react'
import { AddWeaponReq, Con, Log, Reliability, WeaponType, addWeapon } from './CyberClient'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'
import './AddWeapon.css'
import Hideable from './Hideable'

interface AddWeaponProps {
    characterId: number
    updateLogsAndCharacter: (logs: Log[]) => void
}

const NewWeaponForm = ({characterId, updateLogsAndCharacter}: AddWeaponProps) => {
    const [item, setItem] = useState('')
    const [diceNum, setDiceNum] = useState(1)
    const [dDie, setDie] = useState(6)
    const [dmgBonus, setDmgBonus] = useState(0)
    const [divideBy, setDivideBy] = useState(1)
    const [clipSize, setClipSize] = useState(1)
    const [weaponType, setWeaponType] = useState<WeaponType>(WeaponType.Melee)
    const [reliability, setReliabilty] = useState<Reliability>(Reliability.Standard)
    const [humanityCost, setHumanityCost] = useState(0)
    const [wa, setWa] = useState(0)
    const [effectRadius, setEffectRadius] = useState(0)
    const [con, setCon] = useState(Con.Pocket)
    const [rof, setRof] = useState(1)
    const [weight, setWeight] = useState(1)
    const [customRange, setCustomRange] = useState<number | undefined>(undefined)

    const emptyForm = () => {
        setItem('')
        setDiceNum(1)
        setDie(6)
        setDmgBonus(0)
        setDivideBy(1)
        setClipSize(1)
        setReliabilty(Reliability.Standard)
        setHumanityCost(0)
        setWa(0)
        setEffectRadius(0)
        setCon(Con.Pocket)
        setRof(1)
        setWeight(1)
        setCustomRange(undefined)
    }

    const updateDiceNum = (v: number) => updateNumWithLowerLimit(v, 1, setDiceNum)
    const updateDie = (v: number) => updateNumWithLowerLimit(v, 1, setDie)
    const updateDmgBonus = (v: number) => updateNumWithLowerLimit(v, 0, setDmgBonus)
    const updateClipSize = (v: number) => updateNumWithLowerLimit(v, 1, setClipSize)
    const updateHlCost = (v: number) => updateNumWithLowerLimit(v, 0, setHumanityCost)
    const updateWa = (v: number) => updateNumWithLowerLimit(v, -5, setWa)
    const updateEffectRadius = (v: number) => updateNumWithLowerLimit(v, 0, setEffectRadius)
    const updateDivideBy = (v: number) => updateNumWithLowerLimit(v, 1, setDivideBy)
    const updateRof = (v: number) => updateNumWithLowerLimit(v, 1, setRof)
    const updateWeight = (v: number) => updateNumWithLowerLimit(v, 1, setWeight)

    const addWeaponReq: AddWeaponReq = {
        charId: characterId,
        item,
        die: dDie,
        dice: diceNum,
        dmgBonus,
        weaponType,
        divideBy,
        rof,
        wa,
        reliability,
        con,
        weight,
        humanityCost,
        effectRadius,
        clipSize,
        customRange
    }


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
                    <button onClick={() => addWeapon(addWeaponReq).then(updateLogsAndCharacter).then(emptyForm)}>Add</button>
                </td>
                <td>
                    <input className='inputField' value={item} onChange={e => setItem(e.target.value)}/>
                </td>
                <td>
                    <select>
                        <option value={WeaponType.Melee} onClick={() => setWeaponType(WeaponType.Melee)}>Melee</option>
                        <option value={WeaponType.Handgun} onClick={() => setWeaponType(WeaponType.Handgun)}>Handgun</option>
                        <option value={WeaponType.SMG} onClick={() => setWeaponType(WeaponType.SMG)}>SMG</option>
                        <option value={WeaponType.Rifle} onClick={() => setWeaponType(WeaponType.Rifle)}>Rifle</option>
                        <option value={WeaponType.Shotgun} onClick={() => setWeaponType(WeaponType.Shotgun)}>Shotgun</option>
                        <option value={WeaponType.Thrown} onClick={() => setWeaponType(WeaponType.Thrown)}>Thrown</option>
                        <option value={WeaponType.Heavy} onClick={() => setWeaponType(WeaponType.Heavy)}>Heavy</option>
                    </select>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDiceNum} value={diceNum} baseValue={diceNum}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDie} value={`D${dDie}`} baseValue={dDie}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDivideBy} value={`/${divideBy}`} baseValue={divideBy}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDmgBonus} value={`+${dmgBonus}`} baseValue={dmgBonus}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateRof} value={rof} baseValue={rof}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateWa} value={wa} baseValue={wa}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateClipSize} value={clipSize} baseValue={clipSize}/>
                </td>
                <td>
                    <select>
                        <option value={Reliability.Standard} onClick={() => setReliabilty(Reliability.Standard)}>ST</option>
                        <option value={Reliability.VeryReliable} onClick={() => setReliabilty(Reliability.VeryReliable)}>VR</option>
                        <option value={Reliability.Unreliable} onClick={() => setReliabilty(Reliability.Unreliable)}>UR</option>
                    </select> 
                </td>
                <td>
                    <select>
                        <option value={Con.Pocket} onClick={() => setCon(Con.Pocket)}>P</option>
                        <option value={Con.Jacket} onClick={() => setCon(Con.Jacket)}>J</option>
                        <option value={Con.LongJacket} onClick={() => setCon(Con.LongJacket)}>L</option>
                        <option value={Con.NotHideable} onClick={() => setCon(Con.NotHideable)}>N</option>
                    </select>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateWeight} value={`${weight}kg`} baseValue={weight}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateEffectRadius} value={effectRadius} baseValue={effectRadius}/>
                </td>
                <td>
                     <input placeholder={'0'} className='shortInput' value={customRange} onChange={e => setCustomRange(parseInt(e.target.value) || 0)}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateHlCost} value={humanityCost} baseValue={humanityCost}/>
                </td>
            </tr>
        </table>
    )
}

export const AddWeapon = ({characterId, updateLogsAndCharacter}: AddWeaponProps) => 
    <div className='form'>
        <Hideable text='weapon form' props={<NewWeaponForm characterId={characterId} updateLogsAndCharacter={updateLogsAndCharacter}/>}/>
    </div>