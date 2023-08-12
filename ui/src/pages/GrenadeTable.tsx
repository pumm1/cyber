import React, { useState } from 'react'
import Dice from './Dice'
import './GrenadeTable.css'

const GrenadeTable = ({}) => {
    const [show, changeShow] = useState(false)
    type Grid = number | string
    const grids: Grid[]  = [7, '8 - 10', 9, 5, 'Target', 6, 2, '3 - 1', 4]

    return(
        <div className='grenadeComponent'>
            <button onClick={() => changeShow(!show)}>Show Grenade table</button>
            {show && <div className='info'>If throw misses, roll 1D10 for distance from target and then 1D10 for direction away from target</div>}
            {show && 
                <div className='missContainer'>
                    <span className='miss'>
                        Distance
                        <Dice numberOfDice={1} dDie={10}></Dice>
                    </span>
                    <span className='miss'>
                        Direction
                        <Dice numberOfDice={1} dDie={10}></Dice>
                    </span>
                </div>
            }
            <div className='grenadeTable'>
                {show && 
                    <div className='tableContainer'>
                        {grids.map(g => <span>{g}</span>)}
                    </div>
                }
            </div>
        </div>
    )
}

export default GrenadeTable
