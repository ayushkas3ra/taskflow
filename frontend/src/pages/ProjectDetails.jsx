import { useEffect, useState } from 'react'
import { get_tasks } from '../services/taskService'
import { useParams } from 'react-router-dom'
import CreateTaskMoal from '../components/CreateTaskModal'
import { Link } from 'react-router-dom'

export default function ProjectDetail() {
  const [tasks, setTasks] = useState([])
  const [showModal, setShowModal] = useState(false)

  const { projectId } = useParams()

  async function fetchTasks() {
    try {
      const data = await get_tasks(projectId)
      setTasks(data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [projectId])

  if (!tasks) {
    return <h2>Loading...</h2>
  }

  return (
    <div>
      Tasks
      {tasks.map((task) => (
        <div key={task.id}>
          <Link to={`/projects/${projectId}/tasks/${task.id}`}>
            {task.name}
          </Link>
        </div>
      ))}
      <button onClick={() => setShowModal(true)}>+ New task</button>
      {showModal && (
        <CreateTaskMoal
          projectId={projectId}
          onClose={() => setShowModal(false)}
          onTaskCreated={fetchTasks}
        />
      )}
    </div>
  )
}
