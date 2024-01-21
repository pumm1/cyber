export interface TextFieldProps {
    placeholder?: string
    setValue: (s: string) => void
    value: string | number
}
export const TextField = ({setValue, value, placeholder}: TextFieldProps) => 
    <input placeholder={placeholder} type='text' value={value} onChange={e => {
            e.preventDefault()
            setValue(e.target.value)
        }}
    />