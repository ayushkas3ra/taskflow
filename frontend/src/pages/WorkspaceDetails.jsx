import React, { useEffect } from 'react'
import { useState } from 'react'
import { get_projects } from '../services/projectService'
import { useParams } from 'react-router-dom'
import { Link } from 'react-router-dom'
import CreateProjectModal from '../components/CreateProjectModal'

export default function WorkspaceDetails() {
  const [projects, setProjects] = useState([])
  const [showModal, setShowModal] = useState(false)

  const { workspaceId } = useParams()

  async function fetchProjects() {
    try {
      const data = await get_projects(workspaceId)
      setProjects(data)
    } catch (error) {
      console.error(error)
    }
  }

  useEffect(() => {
    fetchProjects()
  }, [workspaceId])

  if (!projects) {
    return <h1>Loading projects..</h1>
  }

  return (
    <div>
      <h1>Projects</h1>
      {projects.map((project) => (
        <div key={project.id}>
          <Link to={`/projects/${project.id}/tasks/`}>{project.name}</Link>
        </div>
      ))}
      <button onClick={() => setShowModal(true)}>+ New Project</button>
      {showModal && (
        <CreateProjectModal
          workspaceId={workspaceId}
          onClose={() => setShowModal(false)}
          onProjectCreated={fetchProjects}
        />
      )}
    </div>
  )
}
