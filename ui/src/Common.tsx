import './Common.css'

export interface InputProps {
    setValue: (s: string) => void
    placeholder?: string
    value?: string | number
}

export interface TextAreaProps extends InputProps {
    readOnly?: boolean
    variant?: 'resizeable' | 'small'
}

export const TextField = ({setValue, value, placeholder}: InputProps) => 
    <input placeholder={placeholder} type='text' value={value} onChange={e => {
            e.preventDefault()
            setValue && setValue(e.target.value)
        }}
    />

export const TextArea = ({setValue, readOnly, value, placeholder, variant}: TextAreaProps) =>
    <textarea readOnly={readOnly} className={variant === 'resizeable' ? 'resizeable' : variant === 'small' ?  'small' : undefined} placeholder={placeholder} value={value} onChange={e => {
            e.preventDefault()
            setValue(e.target.value)
        }}
    />



//TODO: fix these names with the class names
type ButtonVariant = 'SpaceLeft' | 'LessSpaceLeft' | 'MoreSpaceLeft'

export interface ButtonProps {
    variant?: ButtonVariant
    onClick?: () => void | Promise<void>
    label: string
    disabled?: boolean
    className?: string
}

//TODO: rename the classNames better!
const resolveButtonClassName = (variant?: ButtonVariant) => {
    switch(variant) {
        case 'MoreSpaceLeft':
            return 'withMoreLeftSpace'
        case 'SpaceLeft':
            return 'withLeftSpace'
        case 'LessSpaceLeft':
            return 'withLessLeftSpace'
        default:
            return undefined
    }
}

export const Button = ({label, onClick, variant, disabled, className}: ButtonProps) => 
    <button className={className ?? resolveButtonClassName(variant)} disabled={disabled} onClick={onClick}>
        {label}
    </button>

    