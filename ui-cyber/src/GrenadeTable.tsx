import React, { useState } from 'react'
import Dice from './Dice'
import './GrenadeTable.css'
import Hideable from './Hideable'

const GrenadeTable = ({}) => {
    const [show, changeShow] = useState(false)
    type Grid = number | string
    const grids: Grid[]  = [7, '8 - 10', 9, 5, 'Target', 6, 2, '3 - 1', 4]

    const grenadeTableProp = 
        <>
            <div className='info'>If throw misses, roll 1D10 for distance from target and then 1D10 for direction away from target</div>
            <div className='missContainer'>
                <span className='miss'>
                    Direction
                    <Dice numberOfDice={1} dDie={10}></Dice>
                </span>
                <span className='miss'>
                    Distance
                    <Dice numberOfDice={1} dDie={10}></Dice>
                </span>
                <div className='grenadeTable'>
                    <div className='tableContainer'>
                            {grids.map(g => <span key={g}>{g}</span>)}
                    </div>
                </div>
            </div>
        </>

    return(
        <div className='grenadeComponent'>
            <Hideable text='grenade table' props={grenadeTableProp}/>
        </div>
    )
}

export default GrenadeTable
