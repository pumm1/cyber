import { useEffect, useState } from "react"
import { Log, ManualWeaponRollReq, WeaponType, manualWeaponRoll } from "./CyberClient"
import LogViewer from './LogViewer'
import Navbar from "./Navbar"
import { Button } from "./Common"
import { CrtEffect } from "./MainPage"
import { RangePB, RangeClose, RangeMedium, RangeLong, RangeExtreme, RangeResult, HitTable } from "./HitTable"

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
        <div>
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
        <>
            <div>
                <RangeInfo wepRange={weaponRange} targetRange={rangeToTarget}/>
                <div>
                    Weapon range (m): <input type='number' value={weaponRange} onChange={e => setWeaponRange(parseInt(e.target.value))} min={min} max={max} />
                </div>
                <div>
                    
                    Range to target (m): <input type='number' value={rangeToTarget} onChange={e => setRangeToTarget(parseInt(e.target.value))} min={min} max={max} />
                </div>
            </div>
            <HitTable />
        </>
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
        </div>
    )
}

export default WeaponTool