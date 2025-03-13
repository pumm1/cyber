import DifficultyTables from "./DifficultyTables";
import GrenadeTable from "./GrenadeTable";
import WeaponTables from "./JamTable";
import LogViewer from './LogViewer';
import { Log } from "./CyberClient";
import Fumbles from "./FumbleTable";

import './InfoTables.css'

interface InfoTablesProps {
    emptyLogsFn: () => void
    addToLogs: (l: Log) => void
    logs: Log[]
}

export const InfoTables = ({logs, addToLogs, emptyLogsFn}: InfoTablesProps) => 
    <div className="infoTables">
        <LogViewer logs={logs} addToLogs={addToLogs} emptyLogs={emptyLogsFn} />
        <DifficultyTables />
        <Fumbles />
        <WeaponTables />
        <GrenadeTable />
    </div>
