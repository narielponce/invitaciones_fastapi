<template>
  <div class="dashboard-container">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>Panel de Invitados</h1>
        <p v-if="cliente" class="subtitle">Evento de {{ cliente.nombre }}</p>
      </div>
    </header>

    <main class="dashboard-content" v-if="!loading && !error && cliente">
      <!-- Resumen Estadístico -->
      <section class="stats-section">
        <div class="stat-card">
          <span class="material-symbols-outlined icon">group</span>
          <div class="stat-info">
            <h3>{{ totalAcompanantes }}</h3>
            <p>Total Asistentes Confirmados</p>
          </div>
        </div>
        <div class="stat-card">
          <span class="material-symbols-outlined icon">cancel</span>
          <div class="stat-info">
            <h3>{{ totalNoAsisten }}</h3>
            <p>No asisten</p>
          </div>
        </div>
        <div class="stat-card">
          <span class="material-symbols-outlined icon">music_note</span>
          <div class="stat-info">
            <h3>{{ cliente.canciones.length }}</h3>
            <p>Canciones pedidas</p>
          </div>
        </div>
      </section>

      <!-- Tabla de Confirmaciones -->
      <section class="data-section">
        <div class="section-header">
          <h2><span class="material-symbols-outlined">how_to_reg</span> Confirmaciones de Asistencia</h2>
        </div>
        
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Nombre del Invitado</th>
                <th>Asistencia</th>
                <th>Acompañantes</th>
                <th>Restricciones Alimentarias</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="cliente.confirmaciones.length === 0">
                <td colspan="4" class="empty-state">Aún no hay confirmaciones.</td>
              </tr>
              <tr v-for="rsvp in cliente.confirmaciones" :key="rsvp.id" :class="{'no-asiste': !rsvp.asistencia}">
                <td><strong>{{ rsvp.nombre_invitado }}</strong></td>
                <td>
                  <span class="badge" :class="rsvp.asistencia ? 'badge-success' : 'badge-danger'">
                    {{ rsvp.asistencia ? 'Sí Asiste' : 'No Asiste' }}
                  </span>
                </td>
                <td>{{ rsvp.asistencia ? rsvp.cantidad_acompanantes : '-' }}</td>
                <td class="restricciones">{{ rsvp.restricciones_alimentarias || 'Ninguna' }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Tabla de Canciones -->
      <section class="data-section">
        <div class="section-header">
          <h2><span class="material-symbols-outlined">queue_music</span> Playlist Solicitada</h2>
        </div>
        
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Intérprete / Banda</th>
                <th>Nombre de la Canción</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="cliente.canciones.length === 0">
                <td colspan="2" class="empty-state">Aún no hay canciones solicitadas.</td>
              </tr>
              <tr v-for="cancion in cliente.canciones" :key="cancion.id">
                <td><strong>{{ cancion.nombre_interprete }}</strong></td>
                <td>{{ cancion.nombre_tema }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </main>

    <main class="dashboard-content centered" v-else-if="loading">
      <div class="loader"></div>
      <p>Cargando tu panel de control...</p>
    </main>

    <main class="dashboard-content centered error-state" v-else-if="error">
      <span class="material-symbols-outlined error-icon">lock_open_right</span>
      <h2>Acceso Denegado</h2>
      <p>{{ error }}</p>
      <p class="help-text">Asegúrate de haber ingresado con el enlace completo que te enviaron por WhatsApp.</p>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { getClienteDashboard } from '../api';

const route = useRoute();
const cliente = ref(null);
const loading = ref(true);
const error = ref(null);

onMounted(async () => {
  const { tipo_evento, slug } = route.params;
  const token = route.query.token;

  if (!token) {
    error.value = "Falta el token de acceso seguro.";
    loading.value = false;
    return;
  }

  try {
    cliente.value = await getClienteDashboard(tipo_evento, slug, token);
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

const totalAcompanantes = computed(() => {
  if (!cliente.value || !cliente.value.confirmaciones) return 0;
  return cliente.value.confirmaciones
    .filter(c => c.asistencia)
    .reduce((total, c) => total + c.cantidad_acompanantes, 0);
});

const totalNoAsisten = computed(() => {
  if (!cliente.value || !cliente.value.confirmaciones) return 0;
  return cliente.value.confirmaciones.filter(c => !c.asistencia).length;
});
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #f4f6f9;
  font-family: 'Inter', system-ui, sans-serif;
  color: #2c3e50;
}

.dashboard-header {
  background: linear-gradient(135deg, #2c3e50, #3498db);
  color: white;
  padding: 2rem 1rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.header-content {
  max-width: 1000px;
  margin: 0 auto;
}

.dashboard-header h1 {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
}

.subtitle {
  margin: 0.5rem 0 0 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.dashboard-content {
  max-width: 1000px;
  margin: 2rem auto;
  padding: 0 1rem;
}

.centered {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
}

/* Stats Section */
.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2.5rem;
}

.stat-card {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  border-left: 5px solid #3498db;
}

.stat-card .icon {
  font-size: 3rem;
  color: #3498db;
  opacity: 0.2;
}

.stat-info h3 {
  margin: 0;
  font-size: 2rem;
  color: #2c3e50;
}

.stat-info p {
  margin: 0;
  color: #7f8c8d;
  font-weight: 500;
}

/* Data Section */
.data-section {
  background: white;
  border-radius: 10px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

.section-header h2 {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 0;
  color: #2c3e50;
  font-size: 1.5rem;
  border-bottom: 2px solid #ecf0f1;
  padding-bottom: 1rem;
}

.table-responsive {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1rem;
}

.data-table th, .data-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid #ecf0f1;
}

.data-table th {
  background-color: #f8f9fa;
  font-weight: 600;
  color: #34495e;
}

.data-table tr:hover {
  background-color: #f8f9fa;
}

.data-table tr.no-asiste {
  opacity: 0.6;
}

.badge {
  padding: 0.3rem 0.6rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}
.badge-success { background-color: #e8f8f5; color: #1abc9c; }
.badge-danger { background-color: #fdedec; color: #e74c3c; }

.restricciones {
  color: #e67e22;
  font-weight: 500;
}

.empty-state {
  text-align: center;
  color: #95a5a6;
  padding: 3rem !important;
  font-style: italic;
}

/* Loader */
.loader {
  border: 5px solid #f3f3f3;
  border-top: 5px solid #3498db;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 1s linear infinite;
  margin-bottom: 1rem;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Error State */
.error-state .error-icon {
  font-size: 4rem;
  color: #e74c3c;
  margin-bottom: 1rem;
}
.error-state h2 { color: #e74c3c; }
.help-text { color: #7f8c8d; font-size: 0.9rem; margin-top: 1rem; }
</style>
