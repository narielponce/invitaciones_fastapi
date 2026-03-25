<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <h1>Panel de Administración</h1>
      <button @click="logout" class="logout-button">Cerrar Sesión</button>
    </header>

    <main class="dashboard-content">
      <div v-if="!showForm" class="client-list-container">
        <h2>Gestión de Clientes</h2>
        <button @click="handleCreateNew" class="button-primary">Crear Nuevo Cliente</button>
        <table class="client-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Nombre</th>
              <th>Título</th>
              <th>Email</th>
              <th>Fecha Evento</th>
              <th>Acciones</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="loading">
              <td colspan="6">Cargando clientes...</td>
            </tr>
            <tr v-else-if="error">
              <td colspan="6" class="error-text">Error al cargar clientes: {{ error }}</td>
            </tr>
            <tr v-for="cliente in clientes" :key="cliente.id">
              <td>{{ cliente.id }}</td>
              <td>{{ cliente.nombre }}</td>
              <td>{{ cliente.titulo }}</td>
              <td>{{ cliente.email }}</td>
              <td>{{ cliente.fecha_evento }}</td>
              <td class="actions">
                <button @click="handleEdit(cliente)" class="button-edit">Editar</button>
                <button @click="handleDelete(cliente.id)" class="button-delete">Borrar</button>
              </td>
            </tr>
            <tr v-if="!loading && !error && clientes.length === 0">
                <td colspan="6">No hay clientes para mostrar.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <ClientForm
        v-if="showForm"
        :cliente="selectedCliente"
        @save="onSave"
        @cancel="closeForm"
      />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { getClientes, createCliente, updateCliente, deleteCliente } from '../api';
import ClientForm from '../components/ClientForm.vue';

const router = useRouter();

const clientes = ref([]);
const loading = ref(true);
const error = ref(null);
const showForm = ref(false);
const selectedCliente = ref(null);

const fetchClientes = async () => {
  try {
    loading.value = true;
    error.value = null;
    clientes.value = await getClientes();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};

onMounted(fetchClientes);

const handleCreateNew = () => {
  selectedCliente.value = null;
  showForm.value = true;
};

const handleEdit = (cliente) => {
  selectedCliente.value = { ...cliente };
  showForm.value = true;
};

const handleDelete = async (id) => {
  if (confirm('¿Estás seguro de que quieres borrar este cliente?')) {
    try {
      await deleteCliente(id);
      await fetchClientes(); // Recargar la lista
    } catch (e) {
      alert(`Error al borrar el cliente: ${e.message}`);
    }
  }
};

const onSave = async (clienteData) => {
  try {
    if (clienteData.id) {
      // Actualizar
      await updateCliente(clienteData.id, clienteData);
    } else {
      // Crear
      await createCliente(clienteData);
    }
    await fetchClientes();
    closeForm();
  } catch (e) {
    alert(`Error al guardar el cliente: ${e.message}`);
  }
};

const closeForm = () => {
  showForm.value = false;
  selectedCliente.value = null;
};

const logout = () => {
  localStorage.removeItem('isAuthenticated');
  router.push('/admin/login');
};
</script>

<style scoped>
.dashboard-container {
  font-family: Arial, sans-serif;
  color: #333;
}
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #343a40;
  color: white;
}
.logout-button {
  padding: 0.5rem 1rem;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}
.dashboard-content {
  padding: 2rem;
}
.button-primary {
  background-color: #007bff;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 1rem;
}
.client-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}
.client-table th, .client-table td {
  border: 1px solid #ddd;
  padding: 0.75rem;
  text-align: left;
}
.client-table thead {
  background-color: #f8f9fa;
}
.actions {
  display: flex;
  gap: 0.5rem;
}
.button-edit, .button-delete {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
}
.button-edit { background-color: #ffc107; }
.button-delete { background-color: #dc3545; }
.error-text { color: #dc3545; }
</style>
