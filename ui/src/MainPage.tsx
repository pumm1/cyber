import React, { useState } from 'react';
import { Initiative, Log, Skill, listInitiative, listSkills } from './CyberClient';
import SearchOrCreateCharacter from './SearchOrCreateCharacter';
import LogViewer from './LogViewer';
import Navbar from './Navbar';
import { InfoTables } from './InfoTables';

import './MainPage.css';

const App = ({}) => {
  const [logs, setLogs] = useState<Log[]>([])
  const [allSkills, setSkills] = useState<Skill[]>([])
  const [initiatives, setInitiatives] = useState<Initiative[]>([])

  const addToLogs = (l: Log) => {
    const newLogs: Log[] = logs
    setLogs(newLogs.concat(l)) 
  }

  const updateLogs = (newLogs: Log[]) => 
    setLogs([...logs, ...newLogs])

  const emptyLogs = () => 
    setLogs([])

  const updateInitiatives = () => 
    listInitiative().then(setInitiatives)


  React.useEffect(() => {
    listSkills().then(setSkills).then(_ => updateInitiatives())
  }, [])

  React.useEffect(() => {
    document.title = "Home"
}, []);


  return (
    <>
      <div className="main">
        <div className="crt-effect" /> {/* Place it inside main */}
        <Navbar />
        <h1>Welcome to the NET</h1>
        <div className="infoContainer">
          <div className="sheetContainer">
            <SearchOrCreateCharacter
              skills={allSkills}
              updateInitiatives={updateInitiatives}
              initiatives={initiatives}
              updateLogs={updateLogs}
            />
          </div>
          <div>
            <InfoTables logs={logs} addToLogs={addToLogs} emptyLogsFn={emptyLogs}/>
          </div>
        </div>
      </div>
    </>
  )
}



export default App;
