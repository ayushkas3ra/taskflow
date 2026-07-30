import api from '../api/axios'

export async function get_workspaces() {
  const response = await api.get('/workspaces/')
  return response.data.results
}