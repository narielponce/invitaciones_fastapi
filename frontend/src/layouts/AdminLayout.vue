<template>
  <div class="admin-layout">
    <aside class="sidebar">
      <h1 class="admin-title">Admin Panel</h1>
      <nav class="admin-nav">
        <RouterLink to="/admin/clientes">Gestión de Clientes</RouterLink>
        <RouterLink to="/admin/templates">Gestión de Templates</RouterLink>
      </nav>
      <div class="logout-section">
        <button @click="logout" class="logout-button">Cerrar Sesión</button>
      </div>
    </aside>
    <main class="main-content">
      <RouterView />
    </main>
  </div>
</template>

<script setup>
import { RouterView, RouterLink, useRouter } from 'vue-router';

const router = useRouter();

const logout = () => {
  localStorage.removeItem('isAuthenticated');
  router.push('/admin/login');
};
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}
.sidebar {
  width: 250px;
  background-color: #343a40;
  color: #fff;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}
.admin-title {
  font-size: 1.5rem;
  font-weight: bold;
  text-align: center;
  margin-bottom: 2rem;
}
.admin-nav {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
.admin-nav a {
  color: #adb5bd;
  text-decoration: none;
  padding: 0.75rem 1rem;
  border-radius: 5px;
  transition: background-color 0.2s, color 0.2s;
}
.admin-nav a:hover {
  background-color: #495057;
  color: #fff;
}
.admin-nav a.router-link-exact-active {
  background-color: #007bff;
  color: #fff;
}
.logout-section {
  margin-top: auto; /* Pushes logout to the bottom */
}
.logout-button {
  width: 100%;
  padding: 0.75rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.main-content {
  flex-grow: 1;
  padding: 2rem;
  background-color: #f8f9fa;
}
</style>
