import { useState } from "react"
import { RollReq, rollDice } from "./CyberClient"
import React from "react"
import './Dice.css'


const Dice = ({numberOfDice, dDie}: RollReq) => {
    const [roll, setRoll] = useState<undefined | number>(undefined)

    const rollReq: RollReq = {numberOfDice, dDie}
    return (
        <div className='diceContainer'>
            <span className='dice'>
                <button onClick={() => rollDice(rollReq).then(res => setRoll(res))}>
                    ROLL [{numberOfDice}D{dDie}]
                </button>
                {roll !== undefined && <div className='result'>{roll}</div>}
            </span>
        </div>
    )
}

export default Dice