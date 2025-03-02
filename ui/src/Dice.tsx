import { useEffect, useState } from "react"
import { RollReq, rollDice } from "./CyberClient"
import './Dice.css'
import { Button } from "./Common"

interface DiceProps {
    numberOfDice: number
    dDie: number
    updateResult?: (n: number) => void
}

const Dice = ({numberOfDice, dDie, updateResult}: DiceProps) => {
    const [roll, setRoll] = useState<undefined | number>(undefined)

    useEffect(() => {
        updateResult && roll && updateResult(roll)
    }, [roll])

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