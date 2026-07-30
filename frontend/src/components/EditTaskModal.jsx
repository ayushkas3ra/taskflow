import { useState } from 'react'
import { update_task } from '../services/taskService'

export default function EditTaskModal({
  task,
  projectId,
  onClose,
  onTaskUpdated,
}) {
  const [name, setName] = useState(task.name)
  const [description, setDescription] = useState(task.description)
  const [dueDate, setDueDate] = useState(task.due_date)
  const [isFinished, setIsFinished] = useState(task.is_finished)

  async function handleSubmit(e) {
    e.preventDefault()

    const taskData = {
      name,
      description,
      due_date: dueDate,
      is_finished: isFinished,
    }

    try {
      await update_task(projectId, task.id, taskData)
      onTaskUpdated()
      onClose()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div className="modal">
      <form onSubmit={handleSubmit}>
        <h2>Edit task</h2>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Task name"
        />
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Task description"
        ></textarea>
        <input
          type="date"
          value={dueDate}
          onChange={(e) => setDueDate(e.target.value)}
          placeholder="Task due date"
        />
        <label>
          <input
            type="checkbox"
            value={isFinished}
            onChange={(e) => setIsFinished(e.target.checked)}
          />
        </label>
        <button type="submit">Update</button>
        <button type="button" onClick={onClose}>
          Close
        </button>
      </form>
    </div>
  )
}
