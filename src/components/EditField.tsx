import React, { type ChangeEvent, type FC, type HTMLInputTypeAttribute, useState } from 'react'
import Button from './Button'

interface EditFieldProps {
  onApply: (newValue: string | number) => void
  onDiscard: () => void
  inputType: HTMLInputTypeAttribute
  defaultValue?: string | number
}

const EditField: FC<EditFieldProps> = ({ onApply, onDiscard, inputType, defaultValue }) => {
  const [input, setInput] = useState<string | number>(defaultValue ?? '')
  const handleChange = (e: ChangeEvent<HTMLInputElement>): void => {
    const { value } = e.target

    if (typeof defaultValue === 'number') {
      setInput(Number(value))
    } else {
      setInput(value)
    }

  }

  return (
    <>
      <label>
        <input type={inputType} value={input} onChange={handleChange}/>
      </label>
      <Button onClick={() => onApply(input)} type={'apply'} text={'✓'}/>
      <Button onClick={onDiscard} type={'discard'} text={'×'}/>
    </>
  )
}

export default EditField
