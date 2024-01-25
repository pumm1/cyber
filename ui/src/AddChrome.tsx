import React, { useState } from 'react'
import { AddChromeReq, Attribute, AttributeExtra, AttributeBonus, Log, Skill, SkillBonus, addChrome, attributes, sortedSkills } from './CyberClient'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'
import './AddWeapon.css'
import Hideable from './Hideable'
import { Button } from './Common'

interface AddChromeProps {
    characterId: number
    allSkills: Skill[]
    updateLogsAndCharacter: (logs: Log[]) => void
}

export interface AtrBonusesProps {
    attributeBonuses: AttributeBonus[]
    onDelete: (a: AttributeBonus) => void
}

export const AtrBonuses = ({attributeBonuses, onDelete}: AtrBonusesProps) =>
    <div>{attributeBonuses.map((b, idx) => <div key={`${b.attribute}-${idx}`}>{b.attribute} {b.bonus} <Button label='x' onClick={() => onDelete(b)}/></div>) }</div>

export interface SkillBonusesProps {
    allSkills: Skill[]
    skillBonuses: SkillBonus[]
    onDelete: (i: number) => void
}
export const SkillBonuses = ({skillBonuses, allSkills, onDelete}: SkillBonusesProps) =>
    <div>
        {skillBonuses.map(sb => <div>{allSkills.find(s => s.id === sb.skillId)?.skill || 'Not found'} {sb.bonus} <Button label='x' onClick={() => onDelete(sb.skillId)}/></div>)}
    </div>

const NewChromeForm = ({characterId, updateLogsAndCharacter, allSkills}: AddChromeProps) => {
    const [item, setItem] = useState('')
    const [description, setDescription] = useState('')
    const [attributeBonuses, setAttributeBonuses] = useState<AttributeBonus[]>([])
    const [skillBonuses, setSkillBonuses] = useState<SkillBonus[]>([])
    const [attribute, setAtr] = useState<Attribute | AttributeExtra>(Attribute.INT)
    const [atrBonus, setAtrBonus] = useState(0)
    const [skillId, setSkillId] = useState(1)
    const [skillBonus, setSkillBonus] = useState(0)
    const [humanityCost, setHumanityCost] = useState(0)

    const emptyForm = () => {
        setItem('')
        setDescription('')
        setAttributeBonuses([])
        setSkillBonuses([])
        setAtr(Attribute.INT)
        setAtrBonus(0)
        setSkillId(1)
        setSkillBonus(0)
        setHumanityCost(0)
    }

    const setInitialBonuses = () => {
        setAttributeBonuses([])
        setSkillBonuses([])
        setAtrBonus(0)
        setSkillBonus(0)
    }

    const updateHumanityCost = (v: number) => updateNumWithLowerLimit(v, 0, setHumanityCost)

    const newAtrBonus: AttributeBonus = {
        attribute,
        bonus: atrBonus
    }
    const newSkillBonus: SkillBonus = {
        skillId,
        bonus: skillBonus
    }

    const addChromeReq: AddChromeReq = {
        charId: characterId,
        item,
        description,
        attributeBonuses,
        skillBonuses,
        humanityCost
    }

    const onAtrBonusDelete = (a: AttributeBonus) => 
        setAttributeBonuses(attributeBonuses.filter(b => b.attribute !== a.attribute))

    const onSkillBonusDelete = (s: number) =>
        setSkillBonuses(skillBonuses.filter(sb => sb.skillId !== s))

    return(
        <table>
            <tr>
                <th>Add chrome</th>
                <th>Item</th>
                <th>Descr.</th>
                <th>HL</th>
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
                    <Button label='Add' onClick={() => addChrome(addChromeReq).then(updateLogsAndCharacter).then(setInitialBonuses).then(emptyForm)}/>
                </td>
                <td>
                    <input className='inputField' value={item} onChange={e => setItem(e.target.value)}/>
                </td>
                <td>
                    <input value={description} onChange={e => setDescription(e.target.value)}/>
                </td>
                <td>
                    <span className='attackMod'>{humanityCost}<ValueChanger onChange={updateHumanityCost} baseValue={humanityCost}/></span>
                </td> 
                <td>
                    <AtrBonuses attributeBonuses={attributeBonuses} onDelete={onAtrBonusDelete}/>
                </td>
                <td>
                    <Button label='Add bonus' onClick={() => setAttributeBonuses([newAtrBonus, ...attributeBonuses])}/>
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
                    <SkillBonuses onDelete={onSkillBonusDelete} skillBonuses={skillBonuses} allSkills={allSkills}/>
                </td>
                <td>
                    <Button label='Add bonus' onClick={() => setSkillBonuses([newSkillBonus, ...skillBonuses])}/>
                </td>
                <td>
                    <select>
                        {sortedSkills(allSkills).map(s => 
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

const AddChrome = ({characterId, updateLogsAndCharacter, allSkills}: AddChromeProps) => 
    <div className='form'>
        <Hideable text='chrome form' props={<NewChromeForm allSkills={allSkills} characterId={characterId} updateLogsAndCharacter={updateLogsAndCharacter}/>} />
    </div>

export default AddChrome