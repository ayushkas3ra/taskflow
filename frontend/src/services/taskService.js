import api from '../api/axios'

export async function get_tasks(projectId) {
  const response = await api.get(`projects/${projectId}/tasks/`)
  return response.data.results
}

export async function get_task_detail(projectId, taskId) {
  const response = await api.get(`projects/${projectId}/tasks/${taskId}/`)
  return response.data
}

export async function create_task(projectId, taskData) {
  const response = await api.post(`projects/${projectId}/tasks/`, taskData)
  return response.data
}

export async function update_task(projectId, taskId, taskData) {
  const response = await api.patch(
    `projects/${projectId}/tasks/${taskId}/`,
    taskData
  )
  return response.data
}

export async function delete_task(projectId, taskId) {
  const response = await api.delete(`projects/${projectId}/tasks/${taskId}/`)
  return response.data
}
