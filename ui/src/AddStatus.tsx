import { useState } from 'react'
import { AddCharacterStatusReq, CharacterStatusType, Log, addCharacterStatus } from './CyberClient'
import Hideable from './Hideable'
import { Button, TextField } from './Common'

interface AddStatusProps {
    characterId: number
    updateLogsAndCharacter: (l: Log[]) => void
}

const AddStatusForm = ({characterId, updateLogsAndCharacter}: AddStatusProps) => {
    const [status, setStatus] = useState('')
    const [effect, setEffect] = useState('')
    const [statusType, setStatusType] = useState<CharacterStatusType>(CharacterStatusType.Negative)

    const addStsatusReq: AddCharacterStatusReq = {
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
                    <TextField value={status} setValue={setStatus}/>
                </td>
                <td>
                    <TextField value={effect} setValue={setEffect}/>
                </td>
                <td>
                    <select value={statusType}>
                        <option onClick={() => setStatusType(CharacterStatusType.Positive)} value={CharacterStatusType.Positive}>{CharacterStatusType.Positive}</option>
                        <option onClick={() => setStatusType(CharacterStatusType.Neutral)} value={CharacterStatusType.Neutral}>{CharacterStatusType.Neutral}</option>
                        <option onClick={() => setStatusType(CharacterStatusType.Negative)} value={CharacterStatusType.Negative}>{CharacterStatusType.Negative}</option>
                    </select>
                </td>
                <td>
                    <Button label='Add' onClick={() => addCharacterStatus(characterId, addStsatusReq).then(updateLogsAndCharacter)}/>
                </td>
            </tr>
        </table>
    )
}

export const AddStatus = ({characterId, updateLogsAndCharacter}: AddStatusProps) =>
    <div className='form'>
        <Hideable text='status form' props={<AddStatusForm updateLogsAndCharacter={updateLogsAndCharacter} characterId={characterId} />} />
    </div>
