import React, { useState } from 'react'
import { CharacterStatusType, Log } from './CyberClient'
import { ValueChanger, updateNumWithLowerLimit } from './ValueChanger'
import Hideable from './Hideable'

interface AddStatusProps {
    characterId: number
}

const AddStatusForm = ({characterId}: AddStatusProps) => {
    const [status, setStatus] = useState('')
    const [effect, setEffect] = useState('')
    const [statusType, setStatusType] = useState<CharacterStatusType>(CharacterStatusType.Negative)

    const addStsatusReq = {
        characterId,
        status,
        effect,
        statusType
    }

    return (
        <table>
            <tr>
                <th>Status</th>
                <th>Effect</th>
                <th>Status type</th>
                <th>Action</th>
            </tr>
            <tr>
                <td>
                    <input value={status} type='text' onChange={e => {
                        e.preventDefault()
                        setStatus(e.target.value)
                    }}/>
                </td>
                <td>
                    <input value={effect} type='text' onChange={e => {
                        e.preventDefault()
                        setEffect(e.target.value)
                    }}/>
                </td>
                <td>
                    <select value={statusType}>
                        <option onClick={() => setStatusType(CharacterStatusType.Positive)} value={CharacterStatusType.Positive}>{CharacterStatusType.Positive}</option>
                        <option onClick={() => setStatusType(CharacterStatusType.Neutral)} value={CharacterStatusType.Neutral}>{CharacterStatusType.Neutral}</option>
                        <option onClick={() => setStatusType(CharacterStatusType.Negative)} value={CharacterStatusType.Negative}>{CharacterStatusType.Negative}</option>
                    </select>
                </td>
                <td>
                    <button onClick={() => console.log('TODO')}>Add</button>
                </td>
            </tr>
        </table>
    )
}

export const AddStatus = ({characterId}: AddStatusProps) =>
    <div className='form'>
        <Hideable text='status form' props={<AddStatusForm characterId={characterId} />} />
    </div>
