import React, { useState } from 'react'
import { Attribute, AttributeBonus, Log, Skill, SkillBonus } from './CyberClient'
import { ValueChanger } from './ValueChanger'

interface AddChromeProps {
    characterId: number
    allSkills: Skill[]
    updateLogsAndCharacter: (logs: Log[]) => void
}

const NewChromeForm = ({characterId, updateLogsAndCharacter, allSkills}: AddChromeProps) => {
    const [item, setItem] = useState('')
    const [description, setDescription] = useState('')
    const [attributeBonuses, setAttributeBonuses] = useState<AttributeBonus[]>([])
    const [skillBonuses, setSkillBonuses] = useState<SkillBonus[]>([])
    const [attribute, setAtr] = useState(Attribute.INT)
    const [atrBonus, setAtrBonus] = useState(1)
    const [skillId, setSkillId] = useState(0)
    const [skillBonus, setSkillBonus] = useState(0)
    const newAtrBonus: AttributeBonus = {
        attribute,
        bonus: atrBonus
    }
    const newSkillBonus: SkillBonus = {
        skillId,
        bonus: skillBonus
    }
    
    const attributes = [
        Attribute.ATTR, Attribute.BODY, Attribute.COOL, Attribute.EMP, Attribute.INT, 
        Attribute.LUCK, Attribute.MA, Attribute.REF, Attribute.TECH
    ]

    const AtrBonuses = ({}) =>
        <>{attributeBonuses.map(b => <div>{b.attribute} {b.bonus}</div>) }</>

    const SkillBonuses = ({}) =>
        <>{skillBonuses.map(sb => <div>{allSkills.find(s => s.id === sb.skillId)?.skill || 'Not found'} {sb.bonus}</div>)}</>

    return(
        <table>
            <tr>
                <th>Add chrome</th>
                <th>Item</th>
                <th>Descr.</th>
                <th>Curr. atr. Bonuses</th>
                <th>Add atr. bonus</th>
                <th>Bonus attribute</th>
                <th>Atr. bonus</th>
                <th>Curr. Skill bonuses</th>
                <th>Add skill bonus</th>
                <th>Bonus skill</th>
                <th>Skill bonus</th>
            </tr>
            <tr>
                <td>
                    <button>Add</button>
                </td>
                <td>
                    <input value={item} onChange={e => setItem(e.target.value)}/>
                </td>
                <td>
                    <input value={description} onChange={e => setDescription(e.target.value)}/>
                </td>
                <td> 
                    <AtrBonuses />
                </td>
                <td>
                    <button onClick={() => setAttributeBonuses([newAtrBonus, ...attributeBonuses])}>Add bonus</button>
                </td>
                <td>
                    <select>
                        {attributes.map(atr => 
                                 <option value={atr} onClick={() => setAtr(atr)}>{atr}</option>
                            )}
                    </select>
                </td>
                <td>
                    <span className='attackMod'>{atrBonus}<ValueChanger onChange={setAtrBonus} baseValue={atrBonus}/></span>
                </td>
                <td>
                    <SkillBonuses />
                </td>
                <td>
                    <button onClick={() => setSkillBonuses([newSkillBonus, ...skillBonuses])}>Add skill</button>
                </td>
                <td>
                    <select>
                        {allSkills.map(s => 
                            <option value={s.description} onClick={() => setSkillId(s.id)}>{s.skill}</option>
                        )}
                    </select>
                </td>
                <td>
                    <span className='attackMod'>{skillBonus}<ValueChanger onChange={setSkillBonus} baseValue={skillBonus}/></span>
                </td>
            </tr>
        </table>
    )
}

const AddChrome = ({characterId, updateLogsAndCharacter, allSkills}: AddChromeProps) => {
    const [showForm, setShowForm] = useState(false)

    
    
    return(
        <div className='form'>
             <button onClick={() => setShowForm(!showForm)}>
                {!showForm ? 'Add chrome' : 'Hide chrome form'}
            </button>
            {showForm && 
                 <NewChromeForm allSkills={allSkills} characterId={characterId} updateLogsAndCharacter={updateLogsAndCharacter}/>
            }
        </div>
    )
}

export default AddChrome