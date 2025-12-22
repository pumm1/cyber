import { Initiative, Log, UpdateInitiativeReq, addTempCharactersToCombat, addToCombat, advanceCombatSeq, clearCombatSeq, dropFromCombat, updateInitiative, updateInitiativeBonus } from './CyberClient'
import Hideable from './Hideable'
import { Button } from './Common'
import { useEffect, useState } from 'react'
import { MultiLineEditor } from './MultiLineEditor'

import './ListInitiative.css'

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

    const [tempCharacters, setTempCharacters] = useState<string[]>([])


    const addTempCharacters = () => 
        addTempCharactersToCombat(tempCharacters).then(updateLogs)

    const [initiativeMap, setInitiativeMap] = useState<Record<string | number, number>>(
        () =>
            Object.fromEntries(
            initiatives.map(i => [
                i.charId ?? i.tempCharacter,
                i.initiative ?? 0
            ])
            )
        )

    useEffect(() => {
        setInitiativeMap(
            Object.fromEntries(
                initiatives.map(i => [
                    i.charId ?? i.tempCharacter,
                    i.initiative ?? 0
                ])
                )
        )
    }, [initiatives])

    const updateInitiativeValue = (key: string | number, value: number) => {
        setInitiativeMap(prev => ({
            ...prev,
            [key]: value
        }))
    }

    return (
        <div>
            <Hideable 
                text="initiatives" 
                props={
                    <div className="initiatives">
                        Initiatives
                        <Button label="Update" className="updateButton" onClick={() => updateInitiatives()} />
                        <Hideable text='temporary character form' props={
                            <div>
                                <Button label={`Add ${tempCharacters.length} temp. character(s) to combat session`} disabled={tempCharacters.length === 0} className="updateButton" onClick={() => addTempCharacters().then(() => updateInitiatives())} />
                                <MultiLineEditor onLinesChange={setTempCharacters}/>
                            </div>
                        } />
                        {initiatives.length > 0 && <Button disabled={!!initiatives.find(i => !i.initiative)} label="Advance combat" className="updateButton" onClick={() => advanceCombatSeq().then(updateInitiatives)} />}
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
                                    <th>Remove</th>
                                </tr>
                            </thead>
                            <tbody>
                                {initiatives.map((i) => {
                                    const key = i.charId ?? i.tempCharacter ?? 'INVALID' //fallback shouldn't really happen
                                    const initiative = initiativeMap[key]
                                    
                                    const updateInititiveReq: UpdateInitiativeReq = {
                                      charId: i.charId,
                                      tempCharacter: i.tempCharacter,
                                      initiative
                                    }


                                    return (
                                        <tr key={i.charId ?? i.tempCharacter}>
                                            <td>{i.name}</td>
                                            <td>{i.condition}</td>
                                            <td>
                                            <input
                                                type="number"
                                                value={initiative}
                                                onChange={e =>
                                                    updateInitiativeValue(key, Number(e.target.value))
                                                }
                                            />
                                                <Button disabled={initiative == 0} label='Update' onClick={() => updateInitiative(updateInititiveReq).then(updateLogs).then(() => updateInitiatives())}></Button>
                                            </td>
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
                                            <td>
                                                <Button label='X' onClick={() => dropFromCombat(i.charId, i.tempCharacter).then(updateLogs).then(() => updateInitiatives())}/>
                                            </td>
                                        </tr>
                                    )
                                })}
                            </tbody>
                        </table>
                    </div>
                } 
            />
        </div>
    )
}

export default ListInitiative