import { Initiative, advanceCombatSeq, clearCombatSeq } from './CyberClient'
import './ListInitiative.css'
import Hideable from './Hideable'
import { Button } from './Common'

export interface ListInitiativeProps {
    initiatives: Initiative[]
    updateInitiatives: () => Promise<void>
    setCharacterById: (i: number) => void
}

const ListInitiative = ({initiatives, updateInitiatives, setCharacterById}: ListInitiativeProps) => {
    /**
     when using python as backend, one might end up in a weird race condition.
     now this app fetches all the skills initially and we could already fetch also the initaitives.
     though if we fetch both at around the same time, there's some kind of sql transaction and python not being 
     threaded, fetching initatives returns actually the skills...
     took some time to debug

     there might be some simple fix for this
     */

     const initiativesProps = 
        <div className='initiatives'>
            Initiatives
            <Button label='Update' className='updateButton' onClick={() => updateInitiatives()}/>
            {initiatives.length > 0 && <Button label='Advance combat' className='updateButton' onClick={() => advanceCombatSeq().then(() => updateInitiatives())}/>}
            {initiatives.length > 0 && <Button label='Clear initiatives' className='updateButton' onClick={() => clearCombatSeq().then(() => updateInitiatives())}/>}
            <table>
                <tr>
                    <th>Name</th>
                    <th>Initiative</th>
                    <th>Turn</th>
                    <th>Select character</th>
                </tr>
                {initiatives.map((i, idx) => 
                    <tr key={idx}>
                        <td>{i.name}</td>
                        <td>{i.initiative}</td>
                        <td>{i.current ? "This character's turn" : ''}</td>
                        <td>
                            <Button label='Show' onClick={() => setCharacterById(i.charId)}/>
                        </td>
                    </tr>
                )}
            </table>
        </div>

    return(
        <div>
            <Hideable text='initiatives' props={initiativesProps}/>
        </div>
    )
}

export default ListInitiative