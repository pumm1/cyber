import { useState } from 'react'
import './Hideable.css'
import { Button } from './Common'

export interface HideableProps {
    text: string
    props: JSX.Element
}

const Hideable = ({text, props}: HideableProps) => {
    const [show, setShow] = useState(false)
    const prefix = show ? 'Hide' : 'Show'
    const label = `${prefix} ${text}`

    return(
        <div>
            <Button label={label} className='hideable' onClick={() => {
                    setShow(!show)
                }}/>
            {show && props}
        </div>
    )
}

export default Hideable