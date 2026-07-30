import { useEffect, useState } from 'react'
import { get_task_detail, delete_task } from '../services/taskService'
import { useParams } from 'react-router-dom'
import EditTaskModal from '../components/EditTaskModal'
import { useNavigate } from 'react-router-dom'

export default function TaskDetails() {
  const [task, setTask] = useState(null)
  const [editTask, setEditTask] = useState(false)

  const navigate = useNavigate()

  const { projectId, taskId } = useParams()

  async function getTaskDetails() {
    try {
      const data = await get_task_detail(projectId, taskId)
      setTask(data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    getTaskDetails()
  }, [projectId, taskId])

  if (!task) {
    return <h1>Loading task...</h1>
  }

  // delete logic
  async function handleDelete() {
    const confirmed = window.confirm('Are you sure to delete this task?')
    if (!confirmed) return

    try {
      await delete_task(projectId, taskId)
      navigate(`/projects/${projectId}/tasks/`)
    } catch (error) {
      console.error(error)
    }
  }

  return (
    <div>
      <div>{task.name}</div>
      <div>{task.description}</div>
      <div className="buttons">
        <button onClick={() => setEditTask(true)}>Edit</button>
        <button onClick={handleDelete}>Delete</button>
      </div>
      {editTask && (
        <EditTaskModal
          task={task}
          projectId={projectId}
          onClose={() => setEditTask(false)}
          onTaskUpdated={getTaskDetails}
        />
      )}
    </div>
  )
}
