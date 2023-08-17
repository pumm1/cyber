import React, { useEffect, useState } from 'react'
import { Initiative, Log, advanceCombatSeq, clearCombatSeq, listInitiative } from './CyberClient'
import './ListInitiative.css'

export interface ListInitiativeProps {
    updateLogs: (l: Log[]) => void
    initiatives: Initiative[]
    setInitiatives: (i: Initiative[]) => void
}

const ListInitiative = ({updateLogs, setInitiatives, initiatives}: ListInitiativeProps) => {
    const [showInitiative, setShowInitiative] = useState(false)

    const updateInitiatives = () => listInitiative().then(setInitiatives)
    /**
     when using python as backend, one might end up in a weird race condition.
     now this app fetches all the skills initially and we could already fetch also the initaitives.
     though if we fetch both at around the same time, there's some kind of sql transaction and python not being 
     threaded, fetching initatives returns actually the skills
     fetches actually the skills.. 
     took some time to debug
     */

    return(
        <div className='listInitiative'>
            <button className='showButton' onClick={() => {
                setShowInitiative(!showInitiative)
                updateInitiatives()
            }}>{showInitiative ? 'Hide' : 'Show'} initiaitives</button>
            {showInitiative && 
                <div>
                    Initiatives
                    <button className='updateButton' onClick={() => updateInitiatives()}>Update</button>
                    {initiatives.length > 0 && <button className='updateButton' onClick={() => advanceCombatSeq().then(updateLogs).then(() => updateInitiatives())}>Advance combat</button>}
                    {initiatives.length > 0 && <button className='updateButton' onClick={() => clearCombatSeq().then(updateLogs).then(() => updateInitiatives())}>Clear initiatives</button>}
                    <table>
                        <tr>
                            <th>Name</th>
                            <th>Initiative</th>
                            <th>Turn</th>
                        </tr>
                        {initiatives.map((i, idx) => 
                            <tr>
                                <td>{i.name}</td>
                                <td>{i.initiative}</td>
                                <td>{i.current ? "This character's turn" : ''}</td>
                            </tr>
                        )}
                    </table>
                </div>
            }
        </div>
    )
}

export default ListInitiative