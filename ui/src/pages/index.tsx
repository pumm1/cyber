import * as React from "react"
import type { HeadFC, PageProps } from "gatsby"
import SearchOrCreateCharacter from "./SearchOrCreateCharacter"
import './index.css'
import LogViewer from "./LogViewer"
import { useState } from "react"
import { Log, LogType } from "./CyberClient"
import GrenadeTable from "./GrenadeTable"


const IndexPage: React.FC<PageProps> = () => {
  const [logs, setLogs] = useState<Log[]>([])

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
        <SearchOrCreateCharacter updateLogs={updateLogs}/>
        <LogViewer logs={logs} addToLogs={addToLogs}/>
        <GrenadeTable />
      </div>
    </div>
  )
}

export default IndexPage

export const Head: HeadFC = () => <title>The NET</title>
