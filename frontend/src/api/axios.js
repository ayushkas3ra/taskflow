import axios from 'axios'

const api = axios.create({
  baseURL: 'https://taskflow-bi9k.onrender.com/api',
})

api.interceptors.request.use(
  (config) => {
    const accessToken = localStorage.getItem('access')

    if (accessToken) {
      config.headers.Authorization = `Bearer ${accessToken}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default api
