import { useState } from 'react'
import { useParams } from 'react-router-dom'
import { create_task } from '../services/taskService'

export default function CreateTaskModal({ onClose, onTaskCreated }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [isFinished, setIsFinished] = useState(false)
  const [dueDate, setDueDate] = useState('')

  const { projectId } = useParams()

  const taskData = {
    name,
    description,
    is_finished: isFinished,
    due_date: dueDate,
  }

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      await create_task(projectId, taskData)
      onTaskCreated()
      onClose()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <h1>New Task form</h1>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="task name"
        />
        <input
          type="text"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="task description"
        />
        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          placeholder="due date"
        />
        <button type="submit">Save</button>
      </form>
    </div>
  )
}
