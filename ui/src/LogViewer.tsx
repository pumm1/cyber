import React from 'react'
import { useState, useEffect } from 'react'
import './LogViewer.css'
import { Log, LogType } from './CyberClient'
import { Button } from './Common'

interface LogViewerProps {
    logs: Log[]
    addToLogs: (s: Log) => void
    emptyLogs: () => void
}

const LogViewer = ({logs, addToLogs, emptyLogs}: LogViewerProps) => {
    const [input, setInput] = useState<string>('')
    var fieldRef = React.useRef<HTMLInputElement>(null)

    const LogRow = ({log, idx}: {log: Log, idx: number}) =>
        <div key={idx} className={log.logType === LogType.pos ? 'logPos' : log.logType === LogType.neg ? 'logNeg' : 'log'}>
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
                            <LogRow log={log} idx={idx}/>
                            {logsIdxLimit === idx && <div ref={fieldRef}/>}
                        </>
                    )
                })}
            </div>
            <div className='input'><input type='text' value={input} onChange={e => setInput(e.target.value)} /></div>
            <div>
                <Button label='Add to logs' className='btn' disabled={input.length <=0} onClick={() =>{
                 addToLogs({log: input, logType: LogType.neutral})
                 setInput('')
                 }}/>
                 <Button label='Empty lgos' className='btn' onClick={() => emptyLogs()}/>
            </div>
        </div>
    )
} 

export default LogViewer