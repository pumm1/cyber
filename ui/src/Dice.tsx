import { useState } from "react"
import { RollReq, rollDice } from "./CyberClient"
import './Dice.css'
import { Button } from "./Common"


const Dice = ({numberOfDice, dDie}: RollReq) => {
    const [roll, setRoll] = useState<undefined | number>(undefined)

    const rollReq: RollReq = {numberOfDice, dDie}
    return (
        <div className='diceContainer'>
            <span className='dice'>
                <Button label={`ROLL [${numberOfDice}D${dDie}]`} onClick={() => rollDice(rollReq).then(res => setRoll(res))}/>
                {roll !== undefined && <div className='result'>{roll}</div>}
            </span>
        </div>
    )
}

export default Dice