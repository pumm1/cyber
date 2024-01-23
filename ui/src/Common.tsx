import './Common.css'

export interface InputProps {
    setValue: (s: string) => void
    placeholder?: string
    value?: string | number
}

export interface TextAreaProps extends InputProps {
    readOnly?: boolean
    variant?: 'resizeable'
}

export const TextField = ({setValue, value, placeholder}: InputProps) => 
    <input placeholder={placeholder} type='text' value={value} onChange={e => {
            e.preventDefault()
            setValue && setValue(e.target.value)
        }}
    />

export const TextArea = ({setValue, readOnly, value, placeholder, variant}: TextAreaProps) =>
    <textarea readOnly={readOnly} className={variant ? 'resizeable' : undefined} placeholder={placeholder} value={value} onChange={e => {
            e.preventDefault()
            setValue(e.target.value)
        }}
    />



//TODO: fix these names with the class names
type ButtonVariant = 'SomeSpaceLeft' | 'SomeSpaceRight' | 'SpaceLeft' | 'SomeLeftSpace'

export interface ButtonProps {
    variant?: ButtonVariant
    onClick: () => void | Promise<void>
    label: string
    disabled?: boolean
}

//TODO: rename the classNames better!
const resolveButtonClassName = (variant?: ButtonVariant) => {
    switch(variant) {
        case 'SpaceLeft':
            return 'withLeftSpace'
        case 'SomeSpaceRight':
            return 'withLessRightSpace'
        case 'SomeLeftSpace':
            return 'withLessLeftSpace'
        case 'SomeSpaceLeft':
            return 'withSpaceLeft'
        default:
            return undefined
    }
    }

export const Button = ({label, onClick, variant, disabled}: ButtonProps) => 
    <button className={resolveButtonClassName(variant)} disabled={disabled} onClick={onClick}>
        {label}
    </button>

    