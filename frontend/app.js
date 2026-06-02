const { createApp, ref, onMounted } = Vue;

const API = 'http://localhost:8000';

createApp({
  setup() {
    const form = ref({ name: '', description: '' });
    const creating = ref(false);
    const createError = ref('');
    const sessionItems = ref([]);

    const lookupId = ref('');
    const fetching = ref(false);
    const fetchError = ref('');
    const fetchedItem = ref(null);

    const currentPage = ref(1);
    const pageSize = 10;

    const loggingOut = ref(false);

    onMounted(loadItems);

    async function createItem() {
      createError.value = '';
      if (!form.value.name.trim()) {
        createError.value = 'Name is required.';
        return;
      }
      creating.value = true;
      try {
        const res = await fetch(`${API}/items`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: form.value.name.trim(),
            description: form.value.description.trim() || null,
          }),
        });
        if (!res.ok) throw new Error(`Error ${res.status}`);
        const item = await res.json();
        sessionItems.value.unshift(item);
        form.value = { name: '', description: '' };
      } catch (e) {
        createError.value = e.message;
      } finally {
        await loadItems();
        creating.value = false;
      }
    }

    async function fetchItem() {
      fetchError.value = '';
      fetchedItem.value = null;
      if (!lookupId.value) {
        fetchError.value = 'Please enter an ID.';
        return;
      }
      fetching.value = true;
      try {
        const res = await fetch(`${API}/items/${lookupId.value}`);
        if (res.status === 404) throw new Error('Item not found.');
        if (!res.ok) throw new Error(`Error ${res.status}`);
        fetchedItem.value = await res.json();
      } catch (e) {
        fetchError.value = e.message;
      } finally {
        fetching.value = false;
      }
    }

    async function loadItems() {
    
      const offset = (currentPage.value - 1) * pageSize;
      const response = await fetch(
        `${API}/items?limit=${pageSize}&offset=${offset}`
      );
      sessionItems.value = await response.json();
    }

    async function nextPage() {
      currentPage.value++;
      await loadItems();
    }
  
    async function previousPage() {
        if (currentPage.value > 1) {
            currentPage.value--;
            await loadItems();
        }
    }

    async function logout() {
        loggingOut.value = true;
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
  

    return {
        form, creating, createError, sessionItems,
        lookupId, fetching, fetchError, fetchedItem,
        loggingOut, logout,
        createItem, fetchItem,
        nextPage, previousPage,
        currentPage, pageSize
      };  
  }
}).mount('#app');