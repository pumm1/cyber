import { Initiative, Log, advanceCombatSeq, clearCombatSeq, updateInitiativeBonus } from './CyberClient'
import './ListInitiative.css'
import Hideable from './Hideable'
import { Button } from './Common'
import { useEffect, useState } from 'react'

export interface ListInitiativeProps {
    initiatives: Initiative[]
    updateInitiatives: () => Promise<void>
    setCharacterById: (i: number) => void
    updateLogs: (l: Log[]) => void
}

const ListInitiative = ({initiatives, updateInitiatives, setCharacterById, updateLogs}: ListInitiativeProps) => {
    /**
     when using python as backend, one might end up in a weird race condition.
     now this app fetches all the skills initially and we could already fetch also the initaitives.
     though if we fetch both at around the same time, there's some kind of sql transaction and python not being 
     threaded, fetching initatives returns actually the skills...
     took some time to debug

     there might be some simple fix for this
     */

     const [bonusInitiatives, setBonusInitiatives] = useState<{ [key: string]: number | undefined }>(() =>
        Object.fromEntries(initiatives.map(i => [i.charId, i.bonusInitiative]))
    )
    const [bonusTurns, setBonusTurns] = useState<{ [key: string]: number | undefined }>(() =>
        Object.fromEntries(initiatives.map(i => [i.charId, i.bonusTurns]))
    )

    const handleBonusChange = (charId: number, value: number | undefined) => {
        setBonusInitiatives(prev => ({ ...prev, [charId]: value }))
    }

    const handleTurnsChange = (charId: number, value: number | undefined) => {
        setBonusTurns(prev => ({ ...prev, [charId]: value }))
    }

      // Reset bonusInitiatives and bonusTurns when initiatives change
      useEffect(() => {
        setBonusInitiatives(Object.fromEntries(initiatives.map(i => [i.charId, i.bonusInitiative])));
        setBonusTurns(Object.fromEntries(initiatives.map(i => [i.charId, i.bonusTurns])));
    }, [initiatives])

     
    return (
        <div>
            <Hideable 
                text="initiatives" 
                props={
                    <div className="initiatives">
                        Initiatives
                        <Button label="Update" className="updateButton" onClick={() => updateInitiatives()} />
                        {initiatives.length > 0 && <Button label="Advance combat" className="updateButton" onClick={() => advanceCombatSeq().then(updateInitiatives)} />}
                        {initiatives.length > 0 && <Button label="Clear initiatives" className="updateButton" onClick={() => clearCombatSeq().then(updateInitiatives)} />}
                        <table>
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Cond.</th>
                                    <th>Init. (Base)</th>
                                    <th>Init. Bonus + Turns</th>
                                    <th>Turn</th>
                                    <th>Select character</th>
                                </tr>
                            </thead>
                            <tbody>
                                {initiatives.map((i) => (
                                    <tr key={i.charId}>
                                        <td>{i.name}</td>
                                        <td>{i.condition}</td>
                                        <td>{i.initiative}</td>
                                        <td>
                                            <input
                                                style={{maxWidth: 60}}
                                                type="number"
                                                min={0}
                                                value={i.bonusInitiative ?? bonusInitiatives[i.charId] ?? ''}
                                                onChange={(e) => handleBonusChange(i.charId, e.target.value ? Number(e.target.value) : undefined)}
                                            />
                                        <input
                                                style={{maxWidth: 60}}
                                                type="number"
                                                min={0}
                                                value={i.bonusTurns ?? bonusTurns[i.charId] ?? ''}
                                                onChange={(e) => handleTurnsChange(i.charId, e.target.value ? Number(e.target.value) : undefined)}
                                            />
                                            <button 
                                                onClick={() => 
                                                    updateInitiativeBonus({charId: i.charId, bonus: bonusInitiatives[i.charId] ?? 0, turns: bonusTurns[i.charId] ?? 0}).then(updateLogs)
                                                }
                                                disabled={i.bonusTurns === bonusTurns[i.charId] || i.bonusInitiative === bonusInitiatives[i.charId]}>
                                                Update
                                            </button>
                                        </td>
                                        <td>{i.current ? "Current" : ''}</td>
                                        <td>
                                            <Button label="Show" onClick={() => setCharacterById(i.charId)} />
                                        </td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                } 
            />
        </div>
    )
}

export default ListInitiative