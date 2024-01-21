export interface TextFieldProps {
    setValue: (s: string) => void
    value: string | number
}
const TextField = ({setValue, value}: TextFieldProps) => 
    <input type='text' value={value} onChange={e => {
            e.preventDefault()
            setValue(e.target.value)
        }}
    />