import { useState } from 'react'
import Dice from './Dice'
import './GrenadeTable.css'
import Hideable from './Hideable'


type Grid = number | string

const topVal: Grid = '8,10'
const topLeftVal: Grid = 7
const topRightVal: Grid = 9
const targetVal: Grid = 'Target'
const leftVal: Grid = 5
const rightVal: Grid = 6
const bottomVal = '3,1'
const bottomLeftVal = 2
const bottomRightVal = 4

const matchDirectionToGrid = (dirNum: number): Grid => {
    switch(dirNum) {
        case 1:
        case 3:
            return bottomVal
        case 2:
            return bottomLeftVal
        case 4:
            return bottomRightVal
        case 5:
            return leftVal
        case 6:
            return rightVal
        case 7:
            return topLeftVal
        case 8:
        case 10:
            return topVal
        case 9:
            return topRightVal
        default:
            return targetVal
    }
}

const gridMatches = (grid: Grid, directionToUse?: number): boolean => {
    const directionToUseGrid = directionToUse ? matchDirectionToGrid(directionToUse) === grid : false

    return directionToUseGrid
}

const GrenadeTable = ({}) => {
    const grids: Grid[]  = [topLeftVal, topVal, topRightVal, leftVal, targetVal, rightVal, bottomLeftVal, bottomVal, bottomRightVal]
    const [directionVal, setDirectionVal] = useState<number | undefined>()

    const grenadeTableProp = 
        <>
            <div className='info'>If throw misses, roll 1D10 for distance from target and then 1D10 for direction away from target</div>
            <div className='missContainer'>
                <span className='miss'>
                    Direction
                    <Dice numberOfDice={1} dDie={10} updateResult={setDirectionVal}></Dice>
                </span>
                <span className='miss'>
                    Distance
                    <Dice numberOfDice={1} dDie={10}></Dice>
                </span>
                <div className='grenadeTable'>
                    <div className='tableContainer'>
                            {grids.map(g => <span className={gridMatches(g, directionVal) ? 'gridDirection' : undefined} key={g}>{g}</span>)}
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
