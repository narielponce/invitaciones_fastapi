<template>
  <section ref="rsvpSectionRef" class="section rsvp-section animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }">
    <div class="container">

      <div class="section-header has-text-centered">
        <h2 class="section-title" :style="{ fontFamily: `'${cliente.fuente_nombre}', cursive` }">Confirma tu Asistencia</h2>
        <p class="section-subtitle">Tu presencia hará este día aún más especial. Por favor, completa el formulario.</p>
      </div>

      <div class="form-container">
        <transition name="fade" mode="out-in">
          <div v-if="submissionStatus === 'success'" class="notification-panel success">
            <span class="material-symbols-outlined">check_circle</span>
            <p>¡Gracias por confirmar! Te esperamos.</p>
          </div>
          <div v-else-if="submissionStatus === 'error'" class="notification-panel error">
            <span class="material-symbols-outlined">error</span>
            <p>Hubo un error al enviar tu confirmación. Por favor, intenta de nuevo o contacta por WhatsApp.</p>
          </div>

          <form v-else @submit.prevent="handleSubmit" class="rsvp-form">
            <div class="form-grid">
              <div class="form-group full-width">
                <label for="nombre_invitado" class="form-label">Nombre Completo</label>
                <input id="nombre_invitado" class="form-input" v-model="form.nombre_invitado" type="text" placeholder="Tu nombre y apellido" required>
              </div>

              <div class="form-group">
                <label for="asistencia" class="form-label">¿Asistirás?</label>
                <div class="select-wrapper">
                  <select id="asistencia" class="form-input" v-model="form.asistencia" required>
                    <option :value="true">Sí, allí estaré</option>
                    <option :value="false">No podré asistir</option>
                  </select>
                </div>
              </div>

              <div class="form-group">
                <label for="cantidad_acompanantes" class="form-label">Acompañantes</label>
                <div class="select-wrapper">
                  <select id="cantidad_acompanantes" class="form-input" v-model="form.cantidad_acompanantes" :disabled="!form.asistencia">
                    <option value="1">Solo yo</option>
                    <option value="2">2 personas</option>
                    <option value="3">3 personas</option>
                    <option value="4">4 personas</option>
                  </select>
                </div>
              </div>
              
              <div class="form-group full-width">
                <label for="restricciones" class="form-label">Alergias o Restricciones Alimentarias</label>
                <textarea id="restricciones" class="form-textarea" v-model="form.restricciones_alimentarias" placeholder="Ej: celíaco, vegano, alergia a frutos secos..."></textarea>
              </div>
            </div>

            <button class="button is-primary is-large submit-button" type="submit" :disabled="isSubmitting">
              <span class="material-symbols-outlined">send</span>
              <span>{{ isSubmitting ? 'Enviando...' : 'Confirmar Asistencia' }}</span>
            </button>

            <div class="form-divider">o</div>

            <a :href="whatsappUrl" class="button is-large whatsapp-button" target="_blank">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="whatsapp-icon"><path d="M19.004 4.998a9.85 9.85 0 00-13.926 0 9.85 9.85 0 000 13.928l-1.077 3.945 4.038-1.058a9.84 9.84 0 007.965 0 9.85 9.85 0 000-13.928zM8.01 17.118a8.16 8.16 0 01-4.32-1.205l-.31-.184-3.212.84 .856-3.13a8.16 8.16 0 01-1.26-4.432 8.16 8.16 0 0112.5-6.022 8.16 8.16 0 01-1.928 11.134zM11.91 8.526c-.19 0-.37.01-.55.03l-.21.02c-.22.02-.45.08-.66.33-.25.29-.85.83-.85 2.02s.87 2.34 1 2.5c.12.16 1.71 2.73 4.15 3.65.58.22 1.04.35 1.41.45.62.16 1.18.14 1.62.08.48-.06 1.41-.58 1.61-1.14.2-.56.2-1.04.14-1.14s-.21-.16-.45-.28l-2.82-1.38c-.23-.11-.4-.16-.56.16-.16.32-.61.77-.75.93-.14.16-.28.18-.51.06-.23-.12-1-.37-1.9-1.17-.71-.61-1.18-1.36-1.32-1.58-.14-.22-.02-.34.1-.45.11-.1.25-.29.38-.43.12-.14.16-.23.25-.38.09-.15.05-.28-.02-.4L12.48 9c-.08-.18-.16-.16-.24-.16s-.22-.02-.33-.02z"/></svg>
              <span>Confirmar por WhatsApp</span>
            </a>
          </form>
        </transition>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { createClienteConfirmacion } from '../api';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});

const form = ref({
  nombre_invitado: '',
  asistencia: true,
  cantidad_acompanantes: 1,
  restricciones_alimentarias: ''
});

const isSubmitting = ref(false);
const submissionStatus = ref(null);

const handleSubmit = async () => {
  isSubmitting.value = true;
  submissionStatus.value = null;
  try {
    await createClienteConfirmacion(props.cliente.id, form.value);
    submissionStatus.value = 'success';
  } catch (error) {
    console.error("Error submitting confirmation:", error);
    submissionStatus.value = 'error';
  } finally {
    isSubmitting.value = false;
  }
};

const whatsappUrl = computed(() => {
  const text = encodeURIComponent(`¡Hola! Quiero confirmar mi asistencia para la boda de ${props.cliente.nombre}.`);
  // Reemplaza con el número de teléfono de tu cliente si está en la base de datos
  const phone = props.cliente.telefono_envio_confirmacion || 'TUNUMERO'; 
  return `https://wa.me/${phone}?text=${text}`;
});

const rsvpSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(rsvpSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.rsvp-section {
  padding: clamp(3rem, 8vw, 6rem) 1.5rem;
  background-color: #34495e;
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

.rsvp-form .form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group.full-width {
  grid-column: 1 / -1;
}

.form-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: #bdc3c7;
  margin-bottom: 0.5rem;
  text-align: left;
}

.form-input, .form-textarea {
  background-color: rgba(0, 0, 0, 0.2);
  border: 1px solid #566573;
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: #ecf0f1;
  font-size: 1rem;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
}
.form-input::placeholder, .form-textarea::placeholder {
  color: #95a5a6;
}
.form-input:focus, .form-textarea:focus {
  outline: none;
  border-color: var(--theme-primary-color, #3498db);
  box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.3);
}

.form-textarea {
  min-height: 100px;
  resize: vertical;
}

.select-wrapper {
  position: relative;
}
.select-wrapper::after {
  content: 'expand_more';
  font-family: 'Material Symbols Outlined';
  position: absolute;
  top: 50%;
  right: 1rem;
  transform: translateY(-50%);
  pointer-events: none;
  color: #bdc3c7;
}
.form-input.select {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 100%;
  cursor: pointer;
}

.submit-button, .whatsapp-button {
  width: 100%;
  font-weight: 700;
  border-radius: 8px;
  margin-top: 1.5rem;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.submit-button:hover, .whatsapp-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(0, 0, 0, 0.2);
}
.submit-button {
  background-color: var(--theme-primary-color, #3498db);
  border-color: transparent;
}
.submit-button .material-symbols-outlined {
  margin-right: 0.5rem;
}

.whatsapp-button {
  background: transparent;
  border: 2px solid #2ecc71;
  color: #2ecc71;
}
.whatsapp-button:hover {
  background: #2ecc71;
  color: white;
}
.whatsapp-icon {
  width: 20px;
  height: 20px;
  fill: currentColor;
  margin-right: 0.75rem;
}

.form-divider {
  text-align: center;
  margin: 1.5rem 0;
  color: #95a5a6;
  font-size: 0.9rem;
  text-transform: uppercase;
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
  .rsvp-form .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>