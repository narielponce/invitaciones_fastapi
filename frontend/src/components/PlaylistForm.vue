<template>
  <section ref="playlistSectionRef" class="section playlist-section animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }">
    <div class="container">

      <div class="section-header has-text-centered">
        <h2 class="section-title" :style="{ fontFamily: `'${cliente.fuente_nombre}', cursive` }">¡Musicalizá la Fiesta!</h2>
        <p class="section-subtitle">¿Qué canción no puede faltar en la pista de baile? ¡Ayudanos a crear la playlist perfecta!</p>
      </div>

      <div class="form-container">
        <transition name="fade" mode="out-in">
          <div v-if="submissionStatus === 'success'" class="notification-panel success">
            <span class="material-symbols-outlined">playlist_add_check</span>
            <p>¡Gracias por tu sugerencia!</p>
          </div>
          <div v-else-if="submissionStatus === 'error'" class="notification-panel error">
            <span class="material-symbols-outlined">error</span>
            <p>Hubo un error al enviar tu canción. Por favor, intenta de nuevo.</p>
          </div>

          <form v-else @submit.prevent="handleSubmit" class="playlist-form">
            <div class="form-grid">
              <div class="form-group">
                <label for="interprete" class="form-label">Artista o Banda</label>
                <input id="interprete" class="form-input" v-model="form.nombre_interprete" type="text" placeholder="Ej: Dua Lipa" required>
              </div>

              <div class="form-group">
                <label for="tema" class="form-label">Nombre de la Canción</label>
                <input id="tema" class="form-input" v-model="form.nombre_tema" type="text" placeholder="Ej: Don't Start Now" required>
              </div>
            </div>

            <button class="button is-primary is-large submit-button" type="submit" :disabled="isSubmitting">
              <span class="material-symbols-outlined">add_circle</span>
              <span>{{ isSubmitting ? 'Enviando...' : 'Sugerir Canción' }}</span>
            </button>
          </form>
        </transition>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { createClienteCancion } from '../api';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});

const form = ref({
  nombre_interprete: '',
  nombre_tema: '',
});

const isSubmitting = ref(false);
const submissionStatus = ref(null);

const handleSubmit = async () => {
  isSubmitting.value = true;
  submissionStatus.value = null;
  try {
    await createClienteCancion(props.cliente.id, form.value);
    submissionStatus.value = 'success';
    // Limpiar el formulario después de un éxito
    form.value.nombre_interprete = '';
    form.value.nombre_tema = '';
    // Volver a mostrar el formulario después de un tiempo
    setTimeout(() => {
      submissionStatus.value = null;
    }, 3000);
  } catch (error) {
    submissionStatus.value = 'error';
    setTimeout(() => {
      submissionStatus.value = null;
    }, 4000);
  } finally {
    isSubmitting.value = false;
  }
};

const playlistSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(playlistSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.playlist-section {
  padding: clamp(3rem, 8vw, 6rem) 1.5rem;
  background-color: #34495e; /* Mismo color que RSVP para consistencia */
  color: #ecf0f1;
}

.section-header {
  margin-bottom: 3rem;
}

.section-title {
  font-size: clamp(2.5rem, 6vw, 4rem);
  line-height: 1.2;
  color: #ffffff;
  margin-bottom: 1rem;
}

.section-subtitle {
  font-size: clamp(1rem, 2.5vw, 1.25rem);
  color: #bdc3c7;
  max-width: 600px;
  margin: 0 auto;
}

.form-container {
  max-width: 700px;
  margin: 0 auto;
  background-color: rgba(0, 0, 0, 0.15);
  padding: clamp(1.5rem, 4vw, 3rem);
  border-radius: 12px;
}

.playlist-form .form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #bdc3c7;
  margin-bottom: 0.5rem;
  text-align: left;
}

.form-input {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid #566573;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #ecf0f1;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.form-input::placeholder {
  color: #95a5a6;
}
.form-input:focus {
  outline: none;
  border-color: var(--theme-primary-color, #3498db);
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.3);
}

.submit-button {
  width: 100%;
  font-weight: 700;
  border-radius: 8px;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  background-color: var(--theme-primary-color, #3498db);
  border-color: transparent;
}
.submit-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}
.submit-button .material-symbols-outlined {
  margin-right: 0.5rem;
}

.notification-panel {
  text-align: center;
  padding: 2rem;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}
.notification-panel .material-symbols-outlined {
  font-size: 3rem;
}
.notification-panel p {
  font-size: 1.2rem;
  font-weight: 500;
}
.notification-panel.success {
  background-color: rgba(46, 204, 113, 0.1);
  color: #2ecc71;
}
.notification-panel.error {
  background-color: rgba(231, 76, 60, 0.1);
  color: #e74c3c;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity 0.4s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .playlist-form .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>