import { useState } from "react"
import Hideable from "./Hideable"
import Dice from "./Dice"

type FumbleArea = 'Combat (REF)' | 'Athletics (REF)' | 'TECH' | 'EMP' | 'INT'

const FumbleAreas: FumbleArea[] = [
    'Combat (REF)', 'Athletics (REF)', 'TECH', 'EMP', 'INT'
]

const NoFumble = 'No Fumble'

const CombatNoFumble = `${NoFumble}. You just screw up.`
const CombatDropWeapon = 'You drop your weapon.'
const CombatDischarge = 'Weapon discharges (Make reliability roll for non-automatic weapon) or strikes something harmless.'
const CombatWeaponJam = 'Weapon jams (Make reliability roll non-automatic weapon) or imbeds itself in the ground for one turn.'
const CombatWoundYourself = 'You manage to wound yourself. Roll for location.'
const CombatWoundParty = 'You manage to wound a member of your own party.'

const CombatFumbles = ({}) => {
    return (
        <>
            <div>1-4: {CombatNoFumble}</div>
            <div>5: {CombatDropWeapon}</div>
            <div>6: {CombatDischarge}</div>
            <div>7: {CombatWeaponJam}</div>
            <div>8: {CombatWoundYourself}</div>
            <div>9-10: {CombatWoundParty}</div>
        </>
    )
}

const CombatFumblesByResult = (res: number): string => {
    if (res < 5) {
        return CombatNoFumble
    } else if (res === 5) {
        return CombatDropWeapon
    } else  if (res ===  6) {
        return CombatDischarge
    } else  if (res === 7) {
        return CombatWeaponJam
    } else  if (res === 8) {
        return CombatWoundYourself
    } else {
        return CombatWoundParty
    }
}

const AthleticsNoFumble = `${NoFumble}. You just make an idiot of yourself.`
const AthleticsMinorFumble = 'You fail miserably. Take 1 point in minor damage (Sprain, fall, stumble), plus make a Save vs. Stun.'
const AthleticsMajorFumble = 'You fail abysmally. If a physical action, take 1D6 in damage from falling or strained muscles. Also make roll vs Stun at -1.'

const AthleticsFumbles = ({}) => {
    return (
        <>
            <div>1-4: {AthleticsNoFumble}</div>
            <div>5-7: {AthleticsMinorFumble}</div>
            <div>8-10: {AthleticsMajorFumble}</div>
        </>
    )
}

const AthleticsFumblesByResult = (res: number): string => {
    if (res < 5) {
        return AthleticsNoFumble
    } else  if (res < 8) {
        return AthleticsMinorFumble
    } else {
        return AthleticsMajorFumble
    }
}

const TechNoFumble = `${NoFumble}. You just can't get it together.`
const TechMinorFumble = "You not only fail, you make it worse! You drop the tools you're working with, or you lose your grip and damage the thing you're working with even more. Raise the difficulty by 5 points and try again."
const TechMajorFumble = 'Wow. Did you ever blow it! You damaged the device or creation beyond repair. Buy a new one.'

const TechFumbles = ({}) => {
    return (
        <>
            <div>1-4: {TechNoFumble}</div>
            <div>5-7: {TechMinorFumble}</div>
            <div>8-10: {TechMajorFumble}</div>
        </>
    )
}

const TechFumblesByResult = (res: number): string => {
    if (res < 5) {
        return TechNoFumble
    } else  if (res < 8) {
        return TechMinorFumble
    } else {
        return TechMajorFumble
    }
}

const EmpNoFumble = `${NoFumble}. They just won't buy it`
const EmpMinorFumble = "So much for your people skills. You not only don't convince them; you leave them totally cold (-4 to your next EMP die roll) to any other suggestion you might have."
const EmpMajorFumble = "Yow! You blew it royally. You not only didn't convice them, but now they're actually violently opposed to anything you want to do. Roll 1D10. On 1-4, they actually attempt to do you physical harm."

const EmpFumbles = ({}) => {
    return (
        <>
            <div>1-4: {EmpNoFumble}</div>
            <div>5-6: {EmpMinorFumble}</div>
            <div>7-10: {EmpMajorFumble}</div>
        </>
    )
}

const EmpFumblesByResult = (res: number): string => {
    if (res < 5) {
        return EmpNoFumble
    } else  if (res < 7) {
        return EmpMinorFumble
    } else {
        return EmpMajorFumble
    }
}

const IntNoFumble = `${NoFumble}. You just don't know how to do it. You don't know what's going on. You carry on oblivious to higher concerns.`
const IntMinorFumble = "You don't only know anything about what's going on, and you haven't a clue about how to do anything about it. Make a convince check at -2 to see if anyone else notices how dumb you are."
const IntMajorFumble = "Wow, are you oblivious. You not only don't know what's going on or anything about the subject, but everyone knows how ignorant you are."

const IntFumles = ({}) => {
    return (
        <>
            <div>1-4: {IntNoFumble}</div>
            <div>5-7: {IntMinorFumble}</div>
            <div>8-10: {IntMajorFumble}</div>
        </>
    )   
}

const IntFumblesByResult = (res: number): string => {
    if (res < 5) {
        return IntNoFumble
    } else  if (res < 8) {
        return IntMinorFumble
    } else {
        return IntMajorFumble
    }
}

const fumbleResultsForArea = (area: FumbleArea, res: number) => {
    switch (area) {
        case 'Athletics (REF)':
            return AthleticsFumblesByResult(res)
        case 'Combat (REF)': 
            return CombatFumblesByResult(res)
        case 'EMP':
            return EmpFumblesByResult(res)
        case 'INT':
            return IntFumblesByResult(res)
        case 'TECH':
            return TechFumblesByResult(res) 
    }
}


const RollFumble = ({}) => {
    const [fumbleResult, setFumbleResult] = useState<string | undefined>()

    return (
        <div>
            <table>
                <tr>
                    <th>Area</th>
                    <th>Roll</th>
                </tr>
                    {FumbleAreas.map(f => 
                        <tr>
                            <td>{f}</td>
                            <td>
                                <Dice hideResult={true} numberOfDice={1} dDie={10} updateResult={(i: number) => setFumbleResult(fumbleResultsForArea(f, i))}></Dice>
                            </td>
                        </tr>
                    )}
            </table>
            {fumbleResult && <span>{fumbleResult}</span>}
        </div>
    )
}

interface FumbleAreaResultsProps {
    area: FumbleArea
}

const FumbleTableResults = ({area}: FumbleAreaResultsProps) => {
    switch (area) {
        case 'Athletics (REF)':
            return (
                <>
                    <td>{area}</td>
                    <td><AthleticsFumbles /></td>
                </>
            )
        case 'Combat (REF)':
            return (
                <>
                    <td>{area}</td>
                    <td><CombatFumbles /></td>
                </>
            )
        case 'EMP':
            return (
                <>
                    <td>{area}</td>
                    <td><EmpFumbles /></td>
                </>
            )
        case 'INT':
            return (
                <>
                    <td>{area}</td>
                    <td><IntFumles /></td>
                </>
            )
        case 'TECH':
            return (
                <>
                    <td>{area}</td>
                    <td><TechFumbles /></td>
                </>
            )
    }
}

const FumbleTable = ({}) => {
    return (
        <div>
            <table>
                <tr>
                    <th>Area</th>
                    <th>Result</th>
                </tr>
                {FumbleAreas.map(f => 
                    <tr>
                        <FumbleTableResults area={f}/>
                    </tr>
                )}
            </table>
        </div>
    )
}

const Fumbles = ({}) => {
    return (
        <div>
            <Hideable text="Fumble rolls" props={<RollFumble/>} />
            <Hideable text='Fumble table' props={<FumbleTable/>} />
        </div>
    )
}

export default Fumbles