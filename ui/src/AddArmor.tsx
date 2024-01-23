import { useState } from 'react'
import { AddArmorReq, Attribute, AttributeExtra, AttributeBonus, BodyPart, Log, Skill, SkillBonus, addArmor, attributes, sortedSkills } from './CyberClient'
import './AddWeapon.css'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'
import { AtrBonuses, SkillBonuses } from './AddChrome'
import Hideable from './Hideable'
import { Button } from './Common'

export interface AddArmorProps {
    allSkills: Skill[]
    characterId: number
    updateLogsAndCharacter: (logs: Log[]) => void
}

const NewArmorForm = ({characterId, updateLogsAndCharacter, allSkills}: AddArmorProps) => {
    
    const [item, setItem] = useState('')
    const [sp, setSP] = useState(1)
    const [bodyParts, setBodyParts] = useState<BodyPart[]>([])
    const [ev, setEv] = useState(0)
    const [attributeBonuses, setAttributeBonuses] = useState<AttributeBonus[]>([])
    const [skillBonuses, setSkillBonuses] = useState<SkillBonus[]>([])
    const [attribute, setAtr] = useState<Attribute | AttributeExtra>(Attribute.INT)
    const [atrBonus, setAtrBonus] = useState(0)
    const [skillId, setSkillId] = useState(1)
    const [skillBonus, setSkillBonus] = useState(0)
    const [humanityCost, setHumanityCost] = useState(0)

    const emptyForm = () => {
        setItem('')
        setSP(0)
        setBodyParts([])
        setEv(0)
        setAttributeBonuses([])
        setSkillBonuses([])
        setAtr(Attribute.INT)
        setAtrBonus(0)
        setSkillId(1)
        setSkillBonus(0)
        setHumanityCost(0)
    }

    const updateSP = (v: number) => updateNumWithLowerLimit(v, 1, setSP)
    const updateHumanityCost = (v: number) => updateNumWithLowerLimit(v, 0, setHumanityCost)

    const bodyPartsOptions: BodyPart[] = [
        BodyPart.Head,
        BodyPart.Body,
        BodyPart.R_arm,
        BodyPart.L_arm,
        BodyPart.R_leg,
        BodyPart.L_leg
    ]

    const newAtrBonus: AttributeBonus = {
        attribute,
        bonus: atrBonus
    }

    const newSkillBonus: SkillBonus = {
        skillId,
        bonus: skillBonus
    }

    const addArmorReq: AddArmorReq = {
        charId: characterId,
        item,
        ev,
        sp,
        bodyParts,
        attributeBonuses,
        skillBonuses,
        humanityCost
    }
    return (
        <table>
            <tr>
                <th>Add armor</th>
                <th>Item</th>
                <th>SP</th>
                <th>EV</th>
                <th>Covers</th>
                <th>Body parts</th>
                <th>Curr. atr. Bonuses</th>
                <th>Add atr. bonus</th>
                <th>Atr.</th>
                <th>Atr. bonus</th>
                <th>Curr. Skill bonuses</th>
                <th>Add skill bonus</th>
                <th>Bonus skill</th>
                <th>Skill bonus</th>
                <th>(Opt. HL)</th>
            </tr>
            <tr>
                <td>
                    <Button label='Add' disabled={bodyParts.length <= 0} onClick={() => addArmor(addArmorReq).then(updateLogsAndCharacter).then(emptyForm)}/>
                </td>
                <td>
                    <input className='inputField' value={item} onChange={e => setItem(e.target.value)}/>
                </td>
                <td>
                    <span className='attackMod'>{sp}<ValueChanger onChange={updateSP} baseValue={sp}/></span>
                </td>
                <td>
                    <span className='attackMod'>{ev}<ValueChanger onChange={setEv} baseValue={ev}/></span>
                </td>
                <td>
                    [{bodyParts.join(', ')}]
                </td>
                <td>
                    <select>
                        {bodyPartsOptions.map(bp => 
                            !bodyParts.includes(bp) && <option value={bp} onClick={() => setBodyParts([bp, ...bodyParts])}>{bp}</option>
                        )}
                    </select>
                </td>
                <td>
                    <AtrBonuses attributeBonuses={attributeBonuses}/>
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
                    <SkillBonuses allSkills={allSkills} skillBonuses={skillBonuses}/>
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
                <td>
                    <span className='attackMod'>{humanityCost}<ValueChanger onChange={updateHumanityCost} baseValue={humanityCost}/></span>
                </td>
            </tr>
        </table>
    )
}

const AddArmor = ({characterId, updateLogsAndCharacter, allSkills}: AddArmorProps) => 
    <div className='form'>
        <Hideable text='armor form' props={<NewArmorForm allSkills={allSkills} characterId={characterId} updateLogsAndCharacter={updateLogsAndCharacter}/>}/>
    </div>

export default AddArmor