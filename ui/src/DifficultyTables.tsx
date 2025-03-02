import { useState } from 'react'
import Hideable from './Hideable'

import './DifficultyTables.css'

interface Difficulty {
    label: string
    added: boolean
    difficulty: number
    difficultyLabel?: string
}

const easy: Difficulty = {
    label: 'Easy',
    added: false,
    difficulty: 10
}

const average: Difficulty = {
    label: 'Average',
    added: false,
    difficulty: 15
}

const difficult: Difficulty = {
    label: 'Difficult',
    added: false,
    difficulty: 20
}

const veryDifficult: Difficulty = {
    label: 'Very difficult',
    added: false,
    difficulty: 25
}

const nearlyImpossible: Difficulty = {
    label: 'Nearly impossible',
    added: false,
    difficulty: 30
}

const difficulties: Difficulty[] = [easy, average, difficult, veryDifficult, nearlyImpossible]

const noOneNeverDoneBefore: Difficulty = {
    label: 'Never done before',
    added: true,
    difficulty: 6
}

const noRightparts: Difficulty = {
    label: "Don't have right parts",
    added: true,
    difficulty: 2
}

const noRightTools: Difficulty = {
    label: "Don't have right tools",
    added: true,
    difficulty: 3
}

const unfamiliar: Difficulty = {
    label: 'Unfamiliar tools/weapon/vehicle etc.',
    added: true,
    difficulty: 4
}

const underStress: Difficulty = {
    label: 'Under stress',
    added: true,
    difficulty: 3
}

const underAttack: Difficulty = {
    label: 'Under attack',
    added: true,
    difficulty: 3,
    difficultyLabel: '3 to 4'
}

const wounded: Difficulty = {
    label: 'Wounded',
    added: true,
    difficulty: 2,
    difficultyLabel: '2 to 6'
}

const intoxicatedOrTired: Difficulty = {
    label: 'Intoxicated or tired',
    added: true,
    difficulty: 4
}

const hostileEnv: Difficulty = {
    label: 'Hostile environment',
    added: true,
    difficulty: 4
}

const veryHostileEnv: Difficulty = {
    label: 'Very hostile environment',
    added: true,
    difficulty: 6
}

const lackOfInstructions: Difficulty = {
    label: 'Lack of instructions for task',
    added: true,
    difficulty: 2
}

const othersAroundMakingItDifficult: Difficulty = {
    label: 'Others around are making it difficult to focus',
    added: true,
    difficulty: 3
}

const selfNeverDoneBefore: Difficulty = {
    label: 'Character has never done before',
    added: true,
    difficulty: 1
}

const difficultAcrobatics: Difficulty = {
    label: 'Difficult acrobatics',
    added: true,
    difficulty: 3
}

const veryDifficultAcrobatics: Difficulty = {
    label: 'Very difficult acrobatics',
    added: true,
    difficulty: 4
}

const impossibleAcrobatics: Difficulty = {
    label: 'Impossible acrobatics',
    added: true,
    difficulty: 5
}

const obscureOrHiddenInformation: Difficulty = {
    label: 'Obscured or hidden information',
    added: true,
    difficulty: 3
}

const wellHidden: Difficulty = {
    label: 'Well hidden clue/secret door or panel etc.',
    added: true,
    difficulty: 3
}

const complex: Difficulty = {
    label: 'Complex',
    added: true,
    difficulty: 2
}

const veryComplex: Difficulty = {
    label: 'Very complex',
    added: true,
    difficulty: 5
}

const alerted: Difficulty = {
    label: 'Character is alterted',
    added: true,
    difficulty: 3
}

const brightlyLit: Difficulty = {
    label: 'Brightly lit area',
    added: true,
    difficulty: 3
}

const insuffienctLight: Difficulty = {
    label: 'Insufficient light',
    added: true,
    difficulty: 3
}

const pitchDark: Difficulty = {
    label: 'Pitch dark',
    added: true,
    difficulty: 4
}

const secretiveUnderObservation: Difficulty = {
    label: 'Trying to be secretive under observation',
    added: true,
    difficulty: 4
}

const difficultyModifiers: Difficulty[] = [
    noOneNeverDoneBefore, noRightparts, noRightTools, unfamiliar, underStress, underAttack, wounded,
    intoxicatedOrTired, hostileEnv, veryHostileEnv, lackOfInstructions, othersAroundMakingItDifficult,
    selfNeverDoneBefore, difficultAcrobatics, veryDifficultAcrobatics, impossibleAcrobatics,
    obscureOrHiddenInformation, wellHidden, complex, veryComplex, alerted, brightlyLit,
    insuffienctLight, pitchDark, secretiveUnderObservation
]

interface TableProps {
    items: Difficulty[]
    selected?: Difficulty[]
    select?: (d: Difficulty) => void
    empty?: () => void
}

const Table = ({items, selected, select, empty}: TableProps) =>
    <table>
        <tr>
            <th>Difficulty</th>
            <th>To beat</th>
            {select !== undefined && <th>Select</th>}
        </tr>
        {items.map((d, idx) => 
                <tr>
                    <td><span className={selected !== undefined && selected.includes(d) ? 'selectedDifficultyMod' : undefined}>{d.label}</span></td>
                    <td>{d.added && '+'}{d.difficultyLabel ?? d.difficulty}{!d.added && '+'}</td>
                    {empty !== undefined && select !== undefined && idx === 0 && <td><button onClick={() => empty()}>Empty</button></td>}
                    {select !== undefined && idx > 0 && <td><button disabled={selected?.includes(d)} onClick={() => {select(d)}}>Select</button></td>}
                </tr>
            )}
    </table>

const ModifiersTable = ({}) => {
    const [selectedModifiers, setSelectedModifiers] = useState<Difficulty[]>([])
    const selectedDifficulty: Difficulty = {
        label: 'Selected Modifiers',
        added: true,
        difficulty: selectedModifiers.length > 0 ? (selectedModifiers.map(m => m.difficulty)).reduce((a, b) => a + b) : 0
    }

    const addToModifiers = (d: Difficulty) => 
        !selectedModifiers.includes(d) && setSelectedModifiers([d, ...selectedModifiers])

    return (
        <Table items={[selectedDifficulty, ...difficultyModifiers]} selected={selectedModifiers} select={addToModifiers} empty={() => setSelectedModifiers([])}/>
    )
}

const DifficultyTables = ({}) =>
    <div>
        <Hideable text='difficulties' props={<Table items={difficulties}/>}/>
        <div className='difficulties'>
            <Hideable text='modifiers' props={<ModifiersTable />}/>
        </div>
    </div>

export default DifficultyTables
