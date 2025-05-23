import { useEffect, useState } from "react"
import { Log, ManualWeaponRollReq, WeaponType, manualWeaponRoll } from "./CyberClient"
import LogViewer from './LogViewer'
import Navbar from "./Navbar"
import { Button } from "./Common"
import { CrtEffect } from "./MainPage"
import { RangePB, RangeClose, RangeMedium, RangeLong, RangeExtreme, RangeResult, HitTable } from "./HitTable"

import './WeaponTool.css'

const resolveRange = (wepRange: number, targetRange: number) => {
    if (targetRange <= 1) {
        return RangePB
    } else if (wepRange / 4 >= targetRange) {
        return RangeClose
    } else if (wepRange / 2 >= targetRange) {
        return RangeMedium
    } else if (wepRange >= targetRange) {
        return RangeLong
    } else {
        return RangeExtreme
    }
}

interface RangeInfoProps {
    wepRange: number
    targetRange: number
}

const RangeInfo = ({wepRange, targetRange}: RangeInfoProps) => {
    const range: RangeResult = resolveRange(wepRange, targetRange)

    return (
        <div className="infoSection">
            {range.range} (To beat: {range.toBeat})
        </div>
    )
}

const RangeTool = ({}) => {
    const [rangeToTarget, setRangeToTarget] = useState(1)
    const [weaponRange, setWeaponRange] = useState(50)
    const min = 1
    const max = 1000
    return (
        <div className="section">
            <div>
                <RangeInfo wepRange={weaponRange} targetRange={rangeToTarget}/>
                <div className="smallSection">
                    Weapon range (m): <input type='number' value={weaponRange} onChange={e => setWeaponRange(parseInt(e.target.value))} min={min} max={max} />
                </div>
                <div className="smallSection">
                    Range to target (m): <input type='number' value={rangeToTarget} onChange={e => setRangeToTarget(parseInt(e.target.value))} min={min} max={max} />
                </div>
            </div>
            <HitTable />
        </div>
    )
}

interface DmgResult {
    passingDmg: number
    armorDamaged: boolean
    extraInfo?: string
}

const ArmorTool = ({}) => {
    const [armor, setArmor] = useState(10)
    const [incomingDmg, setIncomingDmg] = useState(1)
    const [result, setResult] = useState<DmgResult | undefined>()
    const [isAp, setIsAp] = useState(false)

    const handleArmorByDmg = (): DmgResult => {
        const armorUsed = isAp ? Math.ceil(armor / 2) : armor
        if (armorUsed - incomingDmg <= 0) {
            const extraInfo: string | undefined = 
                isAp ? `(Effective armor calculated for AP: ${armorUsed})` : undefined
            const armorDamaged = (armor > 0 ? true : false)
            if (armorDamaged) {
                setArmor(armor - 1)
            }
            return (
                {
                    passingDmg: Math.abs(armorUsed - incomingDmg),
                    armorDamaged,
                    extraInfo
                }
            )
        } else {
            return (
                {
                    passingDmg: 0,
                    armorDamaged: false
                }
            )
        }
    }

    const minDmg = 1
    const minArmor = 0
    
    return(
        <div>
            <div className="smallSection">
                Armor: <input type='number' value={armor} onChange={e => setArmor(parseInt(e.target.value))} min={minArmor}/>
            </div>
            <div className="smallSection">
                Incoming dmg: <input type='number' value={incomingDmg} onChange={e => setIncomingDmg(parseInt(e.target.value))} min={minDmg}/>
            </div>
            <div className="smallSection">
                <input type='checkbox' checked={isAp} onClick={() => setIsAp(!isAp)}/> AP
            </div>
            <button onClick={() => setResult(handleArmorByDmg())}>Dmg</button>
            {result && 
            <div>
                Result:
                <div className="smallSection">
                    <div className="smallSection">
                        {result.passingDmg > 0 ? 
                            `Passing dmg: ${result.passingDmg}`
                        : 'No damage'
                    }
                    </div>
                   {result.armorDamaged && <div className="smallSection">
                        Armor damaged! {result.extraInfo ?? ''}
                    </div>}
                </div>
            </div>
            }
        </div>
    )
}

//TODO: set parameters
const WeaponTool = ({}) => {
    const [wa, setWa] = useState(0)
    const [weaponType, setWeaponType] = useState<WeaponType>(WeaponType.SMG)
    const [logs, setLogs] = useState<Log[]>([])
    const [rollTotal, setRollTotal] = useState(1)
    const [targets, setTargets] = useState(1)
    const [shots, setShots] = useState(1)
    const [attackRange, setAttackRange] = useState(1)
    const addToLogs = (l: Log) => 
        setLogs(logs.concat(l))
    const req: ManualWeaponRollReq = {
        wa,
        attackRange,
        weaponType,
        rollTotal,
        targets,
        shots
    }

    //<option value={WeaponType.Thrown} onClick={() => setWeaponType(WeaponType.Thrown)}>Thrown</option>
    //<option value={WeaponType.Heavy} onClick={() => setWeaponType(WeaponType.Heavy)}>Heavy</option>
    //<option value={WeaponType.Melee} onClick={() => setWeaponType(WeaponType.Melee)}>Melee</option>

    const updateLogs = (newLogs: Log[]) =>
        setLogs([...logs, ...newLogs])

    const wepRoll = () => 
        manualWeaponRoll(req).then(updateLogs)

    useEffect(() => {
        document.title = "Weapon tool"
    }, []);

    return( 
        <div className="main">
            <CrtEffect />
            <Navbar />
            <h1>Weapon tool</h1>
            <table>
                <tr>
                    <th>Roll total</th>
                    <th>WA</th>
                    <th>Weapon type</th>
                    <th>Shots fired</th>
                    <th>Targets</th>
                    <th>Range</th>
                    <th>Action</th>
                </tr>
                <tr>
                    <td>
                        <input className='valueBox' onChange={e => setRollTotal(parseInt(e.target.value) || 0)} value={rollTotal}/>
                    </td>
                    <td>
                        <input className='valueBox' onChange={e => setWa(parseInt(e.target.value) || 0)} value={wa}/>
                    </td>
                    <td>
                        <select>
                            <option value={WeaponType.Handgun} onClick={() => setWeaponType(WeaponType.Handgun)}>Handgun</option>
                            <option value={WeaponType.SMG} onClick={() => setWeaponType(WeaponType.SMG)}>SMG</option>
                            <option value={WeaponType.Rifle} onClick={() => setWeaponType(WeaponType.Rifle)}>Rifle</option>
                            <option value={WeaponType.Shotgun} onClick={() => setWeaponType(WeaponType.Shotgun)}>Shotgun</option>
                        </select>
                    </td>
                    <td>
                        <input className='valueBox' onChange={e => setShots(parseInt(e.target.value) || 0)} value={shots}/>
                    </td>
                    <td>
                        <input className='valueBox' onChange={e => setTargets(parseInt(e.target.value) || 0)} value={targets}/>
                    </td>
                    <td>
                        <input className='valueBox' onChange={e => setAttackRange(parseInt(e.target.value) || 0)} value={attackRange}/>
                    </td>
                    <td>
                        <Button label='Roll' className='btn'  onClick={() => wepRoll()}/>
                    </td>
                </tr>
            </table>
            <LogViewer logs={logs} addToLogs={addToLogs} emptyLogs={() => setLogs([])}/>
            <RangeTool />
            <ArmorTool />
        </div>
    )
}

export default WeaponTool