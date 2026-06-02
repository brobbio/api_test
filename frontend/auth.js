const API = 'http://localhost:8000';

async function logout() {
  const token = localStorage.getItem('token');
  try {
    await fetch(`${API}/auth/logout`, {
      method: 'DELETE',
      headers: { 'Authorization': `Bearer ${token}` },
    });
  } finally {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    window.location.href = 'login.html';
  }
}