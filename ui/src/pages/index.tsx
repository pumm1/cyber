import * as React from "react"
import type { HeadFC, PageProps } from "gatsby"
import Dice from "./Dice"
import SearchCharacter from "./SearchCharacter"
import './index.css'
import LogViewer from "./LogViewer"
import { useState } from "react"


const IndexPage: React.FC<PageProps> = () => {
  const [logs, setLogs] = useState<string[]>([])

  const addToLogs = (s: string) => {
    const newLogs: string[] = logs
    setLogs(newLogs.concat(s)) 
}


  return (
    <div className='main'>
      <h1>Welcome to the NET</h1>
      <div className='container'>
        <Dice/>
        <SearchCharacter/>
        <LogViewer logs={logs} addToLogs={addToLogs}/>
      </div>
    </div>
  )
}

export default IndexPage

export const Head: HeadFC = () => <title>The NET</title>
