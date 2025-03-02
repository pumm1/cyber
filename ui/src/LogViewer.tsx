import { useState, useEffect, useRef } from 'react';
import './LogViewer.css';
import { Log, LogType } from './CyberClient';
import { Button } from './Common';

const LogRow = ({ log, idx }: { log: Log; idx: number }) => (
    <div key={idx} className={log.logType === LogType.pos ? 'logPos' : log.logType === LogType.neg ? 'logNeg' : 'log'}>
        {'>'} {log.log}
    </div>
)

interface LogViewerProps {
  logs: Log[]
  addToLogs: (s: Log) => void
  emptyLogs: () => void
}

const LogViewer = ({ logs, addToLogs, emptyLogs }: LogViewerProps) => {
  const [input, setInput] = useState<string>('')
  const logsContainerRef = useRef<HTMLDivElement>(null)

  // Scroll to the bottom when logs change
  useEffect(() => {
    if (logsContainerRef.current) {
      logsContainerRef.current.scrollTop = logsContainerRef.current.scrollHeight;
    }
  }, [logs])

  return (
    <div className="logViewer">
      <div><b>Logs</b></div>
      <div className="logs" ref={logsContainerRef}>
        {logs.map((log, idx) => (
          <LogRow log={log} idx={idx} key={idx} />
        ))}
      </div>
      <div className="input">
        <input type="text" value={input} onChange={(e) => setInput(e.target.value)} />
      </div>
      <div>
        <Button
          label="Add to logs"
          className="btn"
          disabled={input.length <= 0}
          onClick={() => {
            addToLogs({ log: input, logType: LogType.neutral });
            setInput('');
          }}
        />
        <Button label="Empty logs" className="btn" onClick={emptyLogs} />
      </div>
    </div>
  )
}

export default LogViewer
