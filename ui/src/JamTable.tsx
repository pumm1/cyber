import { Reliability } from './CyberClient'
import Hideable from './Hideable'
import { HitTable } from './HitTable'

interface ReliabilityValue {
    label: string
    reliability: Reliability
    toBeat: number
}

const unreliable = {
    label: 'Unreliable',
    reliability: Reliability.Unreliable,
    toBeat: 8
}

const standard = {
    label: 'Standard',
    reliability: Reliability.Standard,
    toBeat: 5
}

const veryReliable = {
    label: 'Very reliable',
    reliability: Reliability.VeryReliable,
    toBeat: 3
}

const reliabilities: ReliabilityValue[] = [unreliable, standard, veryReliable]

const JamTable = ({}) => {
    return(
        <table>
            <tr>
                <th>Reliability</th>
                <th>Jams</th>
            </tr>
            {reliabilities.map(r => 
                    <tr>
                        <td>{r.label} ({r.reliability})</td>
                        <td>{`${r.toBeat} or lower`}</td>
                    </tr>
                )}
        </table>
    )
}

const Tables = ({}) => {
    return (
        <div>
            <HitTable />
            <JamTable />
        </div>
    )
}

const WeaponTables = ({}) => 
    <Hideable text='weapon table' props={<Tables />}/>

export default WeaponTables