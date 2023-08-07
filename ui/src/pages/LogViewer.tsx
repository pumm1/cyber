import React from 'react'
import { useState, useEffect } from 'react'
import './LogViewer.css'
import { Log, LogType } from './CyberClient'

const LogViewer = ({logs, addToLogs}: {logs: Log[], addToLogs: (s: Log) => void}) => {
    const [input, setInput] = useState<string>('') //for testing
    var fieldRef = React.useRef<HTMLInputElement>(null)

    const LogRow = ({log}: {log: Log}) =>
        <div className='log'>
            {'>'} {log.log}
        </div>

    const scrollToBottom = () => {
        fieldRef.current?.scrollIntoView()
    }

    useEffect(() => {
        scrollToBottom()
      }, [logs]);
    
    const logsIdxLimit = logs.length - 1 
    return (
        <div>
            <div><b>Logs</b></div>
            <div className='logs' ref={fieldRef}>
                {logs.map((log, idx) => {
                    return(
                        <>
                            <LogRow log={log} />
                            {logsIdxLimit === idx && <div ref={fieldRef}/>}
                        </>
                    )
                })}
            </div>
            <div className='input'><input type='text' value={input} onChange={e => setInput(e.target.value)} /></div>
            <div><button onClick={() =>{
                 addToLogs({log: input, logType: LogType.neutral})
                 setInput('')
            }}>Add log</button></div>
        </div>
    )
} 

export default LogViewer