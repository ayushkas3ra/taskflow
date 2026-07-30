import api from '../api/axios'

export async function login(username, password) {
  const response = await api.post('/token/', {
    username,
    password,
  })
  return response.data
}

export function logout() {
  localStorage.removeItem('access')
  localStorage.removeItem('refresh')
}
