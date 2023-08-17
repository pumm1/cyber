import * as React from "react"
import type { HeadFC, PageProps } from "gatsby"
import SearchOrCreateCharacter from "./SearchOrCreateCharacter"
import './index.css'
import LogViewer from "./LogViewer"
import { useState } from "react"
import { Initiative, Log } from "./CyberClient"
import GrenadeTable from "./GrenadeTable"
import ListInitiative from "./ListInitiative"
import DifficultyTable from "./DifficultyTable"


const IndexPage: React.FC<PageProps> = () => {
  const [logs, setLogs] = useState<Log[]>([])
  const [initiatives, setInitiatives] = useState<Initiative[]>([])

  const addToLogs = (l: Log) => {
    const newLogs: Log[] = logs
    setLogs(newLogs.concat(l)) 
  }

  const updateLogs = (newLogs: Log[]) => 
    setLogs([...logs, ...newLogs])


  return (
    <div className='main'>
      <h1>Welcome to the NET</h1>
      <div className='container'>
        <SearchOrCreateCharacter initiatives={initiatives} updateLogs={updateLogs}/>
        <LogViewer logs={logs} addToLogs={addToLogs}/>
        <ListInitiative initiatives={initiatives} setInitiatives={setInitiatives} updateLogs={updateLogs}/>
        <DifficultyTable />
        <GrenadeTable />
      </div>
    </div>
  )
}

export default IndexPage

export const Head: HeadFC = () => <title>The NET</title>
