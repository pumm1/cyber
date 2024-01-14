import React, { useState } from 'react';
import './App.css';
import { Initiative, Log, Skill, listInitiative, listSkills } from './CyberClient';
import ListInitiative from './ListInitiative';
import SearchOrCreateCharacter from './SearchOrCreateCharacter';
import LogViewer from './LogViewer';
import GrenadeTable from './GrenadeTable';
import DifficultyTable from './DifficultyTable';
import Navbar from './Navbar';

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


  return (
    <div className='main'>
      <Navbar />
      <h1>Welcome to the NET</h1>
      <div className='container'>
        <ListInitiative initiatives={initiatives} updateInitiatives={updateInitiatives}/>
        <SearchOrCreateCharacter skills={allSkills} updateInitiatives={updateInitiatives} initiatives={initiatives} updateLogs={updateLogs}/>
        <LogViewer logs={logs} addToLogs={addToLogs} emptyLogs={emptyLogs}/>
        <DifficultyTable />
        <GrenadeTable />
      </div>
    </div>
  )
}



export default App;
