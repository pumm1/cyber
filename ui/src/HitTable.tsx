
export type Range = 'Point Blank' | 'Close' | 'Medium' | 'Long' | 'Extreme'
 
export interface RangeResult {
    range: Range
    toBeat: number
}

export const RangePB: RangeResult = {
    range: 'Point Blank',
    toBeat: 10
}

export const RangeClose: RangeResult = {
    range: 'Close',
    toBeat: 15
}

export const RangeMedium: RangeResult = {
    range: 'Medium',
    toBeat: 20
}

export const RangeLong: RangeResult = {
    range: 'Long',
    toBeat: 25
}

export const RangeExtreme: RangeResult = {
    range: 'Extreme',
    toBeat: 30
}

const AllRanges = [RangePB, RangeClose, RangeMedium, RangeLong, RangeExtreme]

export const HitTable = ({}) =>
    <table>
        <tr>
            <th>
                Range
            </th>
            <th>
                To beat
            </th>
        </tr>
            {AllRanges.map(r => 
                <tr>
                    <td>
                        {r.range}
                    </td>
                    <td>
                        {r.toBeat}
                    </td>
                </tr>
            )}
    </table>
