const API = 'http://localhost:8000';

async function logout() {
  const token = sessionStorage.getItem('token');
  sessionStorage.removeItem('token');
  sessionStorage.removeItem('username');
  window.location.href = 'login.html';
}