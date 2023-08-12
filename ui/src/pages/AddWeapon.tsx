import React, { useState } from 'react'
import { WeaponType } from './CyberClient'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'

interface AddWeaponProps {
    characterId: number
}

const NewWeaponForm = ({characterId}: AddWeaponProps) => {
    const [item, setItem] = useState('')
    const [diceNum, setDiceNum] = useState(1)
    const [dDie, setDie] = useState(6)
    const [dmgBonus, setDmgBonus] = useState(0)

    const updateDiceNum = (v: number) => updateNumWithLowerLimit(v, 1, setDiceNum)
    const updateDie = (v: number) => updateNumWithLowerLimit(v, 1, setDie)
    const updateDmgBonus = (v: number) => updateNumWithLowerLimit(v, 0, setDmgBonus)

    return(
        <table>
            <tr>
                <th>Item</th>
                <th>Type</th>
                <th># Dice</th>
                <th>D Die</th>
                <th>Dmg bonus</th>
            </tr>
            <tr>
                <td>
                    <input value={item} onChange={e => setItem(e.target.value)}/>
                </td>
                <td>
                    <select>
                        <option value={WeaponType.Melee}>Melee</option>
                        <option value={WeaponType.Handgun}>Handgun</option>
                    </select>
                </td>
                <td>
                    <span className='attackMod'>
                        {diceNum}<ValueChanger onChange={updateDiceNum} baseValue={diceNum}/>
                    </span>
                </td>
                <td>
                    <span className='attackMod'>
                        D{dDie}<ValueChanger onChange={updateDie} baseValue={dDie}/>
                    </span>
                </td>
                <td>
                    <span className='attackMod'>
                        +{dmgBonus}<ValueChanger onChange={updateDmgBonus} baseValue={dmgBonus}/>
                    </span>
                </td>
            </tr>
        </table>
    )
}

export const AddWeapon = ({characterId}: AddWeaponProps) => {
    const [showForm, setShowForm] = useState(false)

    return (
        <div>
             <button onClick={() => setShowForm(true)}>
                Add weapon
            </button>
            {showForm && 
                 <NewWeaponForm characterId={characterId}/>
            }
        </div>
    )
}