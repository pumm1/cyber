import { useState } from "react"
import { rollDice } from "./CyberClient"
import React from "react"
import './Dice.css'

const Dice = () => {
    const [roll, setRoll] = useState<undefined | number>(undefined)

    return (
        <div className='diceContainer'>
            <span className='dice'>
                <button onClick={() => rollDice().then(res => setRoll(res))}>
                    ROLL
                </button>
                {roll !== undefined && <div className='result'>Roll: {roll}</div>}
            </span>
        </div>
    )
}

export default Dice