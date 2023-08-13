import React, { useState } from 'react'
import { AddWeaponReq, Con, Log, Reliability, WeaponType, addWeapon } from './CyberClient'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'

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
    const [weaponType, setWeaponType] = useState<WeaponType>(WeaponType.Handgun)
    const [reliability, setReliabilty] = useState<Reliability>(Reliability.Standard)
    const [humanityCost, setHumanityCost] = useState(0)
    const [wa, setWa] = useState(0)
    const [effectRadius, setEffectRadius] = useState(0)
    const [con, setCon] = useState(Con.Pocket)

    const updateDiceNum = (v: number) => updateNumWithLowerLimit(v, 1, setDiceNum)
    const updateDie = (v: number) => updateNumWithLowerLimit(v, 1, setDie)
    const updateDmgBonus = (v: number) => updateNumWithLowerLimit(v, 0, setDmgBonus)
    const updateClipSize = (v: number) => updateNumWithLowerLimit(v, 1, setClipSize)
    const updateHlCost = (v: number) => updateNumWithLowerLimit(v, 0, setHumanityCost)
    const updateWa = (v: number) => updateNumWithLowerLimit(v, 0, setWa)
    const updateEffectRadius = (v: number) => updateNumWithLowerLimit(v, 0, setEffectRadius)

    const addWeaponReq: AddWeaponReq = {
        charId: characterId,
        item,
        die: dDie,
        dice: diceNum,
        dmgBonus,
        weaponType,
        divideBy,
        wa,
        reliability,
        con,
        humanityCost,
        effectRadius,
        clipSize,
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
                <th>Add</th>
                <th>Item</th>
                <th>Type</th>
                <th># Dice</th>
                <th>D Die</th>
                <th>Dmg bonus</th>
                <th>WA</th>
                <th>Clip size</th>
                <th>CON</th>
                <th>Effect radius</th>
                <th>(Opt. HL cost)</th>
            </tr>
            <tr>
                <td>
                    <button onClick={() => addWeapon(addWeaponReq).then(updateLogsAndCharacter)}>Add</button>
                </td>
                <td>
                    <input value={item} onChange={e => setItem(e.target.value)}/>
                </td>
                <td>
                    <select>
                        <option value={WeaponType.Melee} onSelect={() => setWeaponType(WeaponType.Melee)}>Melee</option>
                        <option value={WeaponType.Handgun} onSelect={() => setWeaponType(WeaponType.Handgun)}>Handgun</option>
                        <option value={WeaponType.SMG} onSelect={() => setWeaponType(WeaponType.SMG)}>SMG</option>
                        <option value={WeaponType.Rifle} onSelect={() => setWeaponType(WeaponType.Rifle)}>Rifle</option>
                        <option value={WeaponType.Shotgun} onSelect={() => setWeaponType(WeaponType.Shotgun)}>Shotgun</option>
                        <option value={WeaponType.Thrown} onSelect={() => setWeaponType(WeaponType.Thrown)}>Thrown</option>
                        <option value={WeaponType.Heavy} onSelect={() => setWeaponType(WeaponType.Heavy)}>Heavy</option>
                    </select>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDiceNum} value={diceNum} baseValue={diceNum}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDie} value={`D${dDie}`} baseValue={dDie}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateDmgBonus} value={`+${dmgBonus}`} baseValue={dmgBonus}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateWa} value={wa} baseValue={wa}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateClipSize} value={clipSize} baseValue={clipSize}/>
                </td>
                <td>
                    <select>
                        <option value={Con.Pocket} onSelect={() => setCon(Con.Pocket)}>Pocket</option>
                        <option value={Con.Jacket} onSelect={() => setCon(Con.Jacket)}>Jacket</option>
                        <option value={Con.LongJacket} onSelect={() => setCon(Con.LongJacket)}>Lon  g Jacket</option>
                        <option value={Con.NotHideable} onSelect={() => setCon(Con.NotHideable)}>Not hideable</option>
                    </select>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateEffectRadius} value={effectRadius} baseValue={effectRadius}/>
                </td>
                <td>
                    <FormRowWithValueChanger onChange={updateHlCost} value={humanityCost} baseValue={humanityCost}/>
                </td>
            </tr>
        </table>
    )
}

export const AddWeapon = ({characterId, updateLogsAndCharacter}: AddWeaponProps) => {
    const [showForm, setShowForm] = useState(false)

    return (
        <div>
             <button onClick={() => setShowForm(!showForm)}>
                {showForm ? 'Add weapon' : 'Hide form'}
            </button>
            {showForm && 
                 <NewWeaponForm characterId={characterId} updateLogsAndCharacter={updateLogsAndCharacter}/>
            }
        </div>
    )
}   