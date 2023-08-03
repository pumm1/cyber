import React from 'react'
import { useState, useEffect } from 'react'
import './LogViewer.css'

const LogViewer = ({logs, addToLogs}: {logs: string[], addToLogs: (s: string) => void}) => {
    const [input, setInput] = useState<string>('') //for testing
    var fieldRef = React.useRef<HTMLInputElement>(null)

    const LogRow = ({log}: {log: string}) =>
        <div className='log'>
            {log}
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
            <input type='text' value={input} onChange={e => setInput(e.target.value)} />
            <button onClick={() =>{
                 addToLogs(input)
                 setInput('')
            }}>Add log</button>
        </div>
    )
} 

export default LogViewer