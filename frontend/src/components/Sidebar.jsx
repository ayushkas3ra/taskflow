import { logout } from '../services/authService'
import { useNavigate } from 'react-router-dom'

const navigate = useNavigate()

function handleLogout() {
  logout()
  navigate('/login')
}

export default function Sidebar() {
  return <button onClick={handleLogout}>Logout</button>
}
