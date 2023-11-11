import React from 'react'
import { useState, useEffect } from 'react'
import './LogViewer.css'
import { Log, LogType } from './CyberClient'

interface LogViewerProps {
    logs: Log[]
    addToLogs: (s: Log) => void
    emptyLogs: () => void
}

const LogViewer = ({logs, addToLogs, emptyLogs}: LogViewerProps) => {
    const [input, setInput] = useState<string>('')
    var fieldRef = React.useRef<HTMLInputElement>(null)

    const LogRow = ({log}: {log: Log}) =>
        <div className={log.logType == LogType.pos ? 'logPos' : log.logType === LogType.neg ? 'logNeg' : 'log'}>
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
        <div className='logViewer'>
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
            <div>
                <button className='btn' disabled={input.length <=0} onClick={() =>{
                 addToLogs({log: input, logType: LogType.neutral})
                 setInput('')
                 }}>
                    Add to logs
                </button>
                <button className='btn' onClick={() => emptyLogs()}>
                    Empty logs
                </button>
            </div>
        </div>
    )
} 

export default LogViewer