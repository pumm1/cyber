import React from 'react'
import './CharacterSheet.css'

interface ValueChangerProps {
    baseValue: number
    onChange: (i: number) => void
}

export const updateNumWithLowerLimit = (newValue: number, limit: number, setter: (i: number) => void) => {
    if (newValue >= limit) {
        setter(newValue)
    }
}

export const ValueChanger = ({onChange, baseValue}: ValueChangerProps) =>
    <div className='trianglesSet'>
        <a onClick={() => onChange(baseValue + 1)}>
            <div className="triangleUp"></div>
        </a>
        <a onClick={() =>  onChange(baseValue - 1)}>
            <div className="triangleDown"></div>
        </a>
    </div>

