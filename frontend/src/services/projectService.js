import api from '../api/axios'

export async function get_projects(workspaceId) {
  const response = await api.get(`/workspaces/${workspaceId}/projects`)
  return response.data.results
}

export async function create_project(workspaceId, projectData) {
  const response = await api.post(
    `/workspaces/${workspaceId}/projects/`,
    projectData
  )
  return response.data
}
