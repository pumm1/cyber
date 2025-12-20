import { Initiative, Log, addToCombat, advanceCombatSeq, clearCombatSeq, updateInitiativeBonus } from './CyberClient'
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

    const [tempCharacter, setTempCharacter] = useState('')


    const addTempCharacter = () => 
        addToCombat({
            tempCharacter,
        }).then(updateLogs)

     
    return (
        <div>
            <Hideable 
                text="initiatives" 
                props={
                    <div className="initiatives">
                        Initiatives
                        <Button label="Update" className="updateButton" onClick={() => updateInitiatives()} />
                        <div>
                            <input type='text' value={tempCharacter} onChange={e => setTempCharacter(e.target.value)}/>
                            <Button label="Add temp character" disabled={!tempCharacter} className="updateButton" onClick={() => addTempCharacter()} />
                        </div>
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
                                    <tr key={i.charId ?? i.tempCharacter}>
                                        <td>{i.name}</td>
                                        <td>{i.condition}</td>
                                        <td>{i.initiative}</td>
                                        <td>
                                            <input
                                                style={{maxWidth: 60}}
                                                type="number"
                                                min={0}
                                                value={i.charId ? i.bonusInitiative ?? bonusInitiatives[i.charId] : ''}
                                                onChange={(e) => handleBonusChange(i.charId ?? -9999, e.target.value ? Number(e.target.value) : undefined)}
                                            />
                                        <input
                                                style={{maxWidth: 60}}
                                                type="number"
                                                min={0}
                                                value={i.charId ? i.bonusTurns ?? bonusTurns[i.charId] : ''}
                                                onChange={(e) => handleTurnsChange(i.charId ?? -9999, e.target.value ? Number(e.target.value) : undefined)}
                                            />
                                            <button 
                                                onClick={() => 
                                                    updateInitiativeBonus({charId: i.charId, tempCharacter: i.tempCharacter, bonus: bonusInitiatives[i.charId ?? i.tempCharacter ?? ''] ?? 0, turns: bonusTurns[i.charId ?? i.tempCharacter ?? ''] ?? 0}).then(updateLogs)
                                                }
                                                disabled={i.bonusTurns === bonusTurns[i.charId ?? i.tempCharacter ?? ''] || i.bonusInitiative === bonusInitiatives[i.charId ?? i.tempCharacter ?? '']}>
                                                Update
                                            </button>
                                        </td>
                                        <td>{i.current ? "Current" : ''}</td>
                                        <td>
                                            <Button disabled={!i.charId} label="Show" onClick={() => setCharacterById(i.charId ?? -999999)} />
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