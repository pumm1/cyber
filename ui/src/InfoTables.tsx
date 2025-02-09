import DifficultyTable from "./DifficultyTable";
import GrenadeTable from "./GrenadeTable";
import JamTable from "./JamTable";

import './InfoTables.css'

export const InfoTables = ({}) => 
    <div className="infoTables">
        <DifficultyTable />
        <JamTable />
        <GrenadeTable />
    </div>
