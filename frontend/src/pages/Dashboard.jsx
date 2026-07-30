import { useState, useEffect } from 'react'
import { get_workspaces } from '../services/workspaceService'
import { Link } from 'react-router-dom'

export default function Dashboard() {
  const [workspaces, setWorkspaces] = useState([])

  useEffect(() => {
    async function fetchWorkspaces() {
      try {
        const data = await get_workspaces()
        setWorkspaces(data)
      } catch (error) {
        console.error(error)
      }
    }
    fetchWorkspaces()
  }, [])

  if (!workspaces) {
    return <h1>Loading workspaces..</h1>
  }

  return (
    <div>
      <h1>Dashboard</h1>
      {workspaces.map((workspace) => (
        <div key={workspace.id}>
          <Link to={`/workspaces/${workspace.id}`}>{workspace.name}</Link>
        </div>
      ))}
    </div>
  )
}
