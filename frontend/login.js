const { createApp, ref } = Vue;

const API = 'http://localhost:8000';

createApp({
  setup() {
    const form = ref({ username: '', password: '' });
    const loading = ref(false);
    const error = ref('');

    async function login() {
      error.value = '';
      if (!form.value.username.trim() || !form.value.password.trim()) {
        error.value = 'Username and password are required.';
        return;
      }
      loading.value = true;
      try {
        const res = await fetch(`${API}/auth/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: form.value.username.trim(),
            password: form.value.password.trim(),
          }),
        });
        if (res.status === 401) throw new Error('Invalid credentials.');
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const data = await res.json();


        sessionStorage.setItem('token', data.token);
        sessionStorage.setItem('username', data.username);
        window.location.href = 'index.html';
      } catch (e) {
        error.value = e.message;
      } finally {
        loading.value = false;
      }
    }

    return { form, loading, error, login };
  }
}).mount('#app');