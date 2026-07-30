import { useState } from 'react'
import { create_project } from '../services/projectService'
import { useParams } from 'react-router-dom'

export default function CreateProjectModal({ onClose, onProjectCreated }) {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [dueDate, setDueDate] = useState('')

  const { workspaceId } = useParams()

  const projectData = {
    name: name,
    description: description,
    due_date: dueDate,
  }

  async function handleSubmit(e) {
    e.preventDefault()
    try {
      await create_project(workspaceId, projectData)

      onProjectCreated()
      onClose()
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <h1>New Project Form</h1>
      <input
        onChange={(e) => setName(e.target.value)}
        value={name}
        name="name"
        type="text"
        placeholder="name"
      />
      <input
        onChange={(e) => setDescription(e.target.value)}
        value={description}
        name="description"
        type="text"
        placeholder="description"
      />
      <input
        onChange={(e) => setDueDate(e.target.value)}
        value={dueDate}
        name="due_date"
        type="date"
        placeholder="due date"
      />
      <button type="submit">Save</button>
    </form>
  )
}
