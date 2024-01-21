import React, { useState } from 'react'
import './Hideable.css'

export interface HideableProps {
    text: string
    props: JSX.Element
}

const Hideable = ({text, props}: HideableProps) => {
    const [show, setShow] = useState(false)

    return(
        <div>
            <button className='hideable' onClick={() => {
                    setShow(!show)
                }}>{show ? 'Hide' : 'Show'} {text}
            </button>
            {show && props}
        </div>
    )
}

export default Hideable