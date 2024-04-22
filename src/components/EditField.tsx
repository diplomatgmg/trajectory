import React, { type ChangeEvent, type FC, type HTMLInputTypeAttribute, useEffect, useRef, useState } from 'react'
import Button from './Button'

interface EditFieldProps {
  onApply: (newValue: string | number) => void
  onDiscard: () => void
  inputType: HTMLInputTypeAttribute
  defaultValue?: string | number
}

const EditField: FC<EditFieldProps> = ({ onApply, onDiscard, inputType, defaultValue }) => {
  const [input, setInput] = useState<string | number>(defaultValue ?? '')
  const inputRef = useRef<HTMLInputElement | null>(null)

  useEffect(() => {
    inputRef.current?.select()
  }, [])

  const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    console.log(inputRef)

    const { value } = e.target

    if (typeof defaultValue === 'number') {
      setInput(Number(value))
    } else {
      setInput(value)
    }

  }

  return (
    <>
      <label >
        <input type={inputType} value={input} onChange={handleChange} ref={inputRef}/>
      </label>
      <Button onClick={() => onApply(input)} type={'apply'} text={'✓'}/>
      <Button onClick={onDiscard} type={'discard'} text={'×'}/>
    </>
  )
}

export default EditField
