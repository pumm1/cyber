import React, { useEffect, useRef } from "react"
import "./MultiLineEditor.css"

type Props = {
  value?: string
  onLinesChange?: (lines: string[]) => void
}

export const MultiLineEditor: React.FC<Props> = ({
  value = "",
  onLinesChange
}) => {
  const ref = useRef<HTMLDivElement>(null)

  // Sync external value → editor
  useEffect(() => {
    if (ref.current && ref.current.innerText !== value) {
      ref.current.innerText = value
    }
  }, [value])

  // User typing → emit lines
  const handleInput = () => {
    if (!ref.current) return

    const text = ref.current.innerText.replace(/\r\n/g, "\n")
    const lines = text.split("\n").map(t => t.trim()).filter(t => t.length > 0)

    onLinesChange?.(lines)
  }

  return (
    <div
      ref={ref}
      contentEditable
      suppressContentEditableWarning
      className="editor"
      onInput={handleInput}
    />
  )
}
