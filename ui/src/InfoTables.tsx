import DifficultyTable from "./DifficultyTable";
import GrenadeTable from "./GrenadeTable";
import JamTable from "./JamTable";
import LogViewer from './LogViewer';

import './InfoTables.css'
import { Log } from "./CyberClient";

interface InfoTablesProps {
    emptyLogsFn: () => void
    addToLogs: (l: Log) => void
    logs: Log[]
}

export const InfoTables = ({logs, addToLogs, emptyLogsFn}: InfoTablesProps) => 
    <div className="infoTables">
        <LogViewer logs={logs} addToLogs={addToLogs} emptyLogs={emptyLogsFn} />
        <DifficultyTable />
        <JamTable />
        <GrenadeTable />
    </div>
