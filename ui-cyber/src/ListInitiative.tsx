import React, { useEffect, useState } from 'react'
import { Initiative, Log, advanceCombatSeq, clearCombatSeq, listInitiative } from './CyberClient'
import './ListInitiative.css'
import Hideable from './Hideable'

export interface ListInitiativeProps {
    initiatives: Initiative[]
    updateInitiatives: () => Promise<void>
}

const ListInitiative = ({initiatives, updateInitiatives}: ListInitiativeProps) => {
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
            <button className='updateButton' onClick={() => updateInitiatives()}>Update</button>
            {initiatives.length > 0 && <button className='updateButton' onClick={() => advanceCombatSeq().then(() => updateInitiatives())}>Advance combat</button>}
            {initiatives.length > 0 && <button className='updateButton' onClick={() => clearCombatSeq().then(() => updateInitiatives())}>Clear initiatives</button>}
            <table>
                <tr>
                    <th>Name</th>
                    <th>Initiative</th>
                    <th>Turn</th>
                </tr>
                {initiatives.map((i, idx) => 
                    <tr key={idx}>
                        <td>{i.name}</td>
                        <td>{i.initiative}</td>
                        <td>{i.current ? "This character's turn" : ''}</td>
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