<template>
  <section ref="ceremonyInfoSectionRef" class="section ceremony-info-section animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }">
    <div class="container has-text-centered">

      <div class="section-header">
        <h2 class="section-title" :style="{ fontFamily: `'${cliente.fuente_nombre}', cursive` }">La Ceremonia</h2>
        <p class="section-subtitle">
          Nos daremos el "sí, quiero" en:
        </p>
      </div>

      <div class="event-details-grid">
        <div class="detail-item">
          <div class="detail-icon"><span class="material-symbols-outlined">calendar_today</span></div>
          <h3 class="detail-title">Fecha</h3>
          <p class="detail-text">{{ formattedFechaCeremonia }}</p>
        </div>

        <div class="detail-item">
          <div class="detail-icon"><span class="material-symbols-outlined">schedule</span></div>
          <h3 class="detail-title">Hora</h3>
          <p class="detail-text">{{ formattedHoraCeremonia }}</p>
        </div>

        <div class="detail-item">
          <div class="detail-icon"><span class="material-symbols-outlined">church</span></div>
          <h3 class="detail-title">Lugar</h3>
          <p class="detail-text">{{ cliente.lugar_ceremonia }}</p>
          <p class="detail-text-address">{{ cliente.direccion_ceremonia }}</p>
        </div>
      </div>

      <a :href="googleMapsUrl" target="_blank" class="button is-primary is-large map-button">
        <span class="material-symbols-outlined">location_on</span>
        <span>Ver Ubicación</span>
      </a>

    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});

const formattedFechaCeremonia = computed(() => {
  if (!props.cliente.fecha_ceremonia) return '--';
  const date = new Date(props.cliente.fecha_ceremonia + 'T00:00:00');
  return date.toLocaleDateString('es-ES', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' });
});

const formattedHoraCeremonia = computed(() => {
  if (!props.cliente.hora_ceremonia) return '--';
  const [hours, minutes] = props.cliente.hora_ceremonia.split(':');
  return `${hours}:${minutes} hs`;
});

const googleMapsUrl = computed(() => {
  if (props.cliente.direccion_ceremonia) {
    const encodedAddress = encodeURIComponent(`${props.cliente.lugar_ceremonia}, ${props.cliente.direccion_ceremonia}`);
    return `https://www.google.com/maps/search/?api=1&query=${encodedAddress}`;
  }
  return '#';
});

const ceremonyInfoSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(ceremonyInfoSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.ceremony-info-section {
  padding: clamp(3rem, 8vw, 6rem) 1.5rem;
  /* Utiliza un color de fondo ligeramente diferente para crear distinción visual si se desea, o el mismo para unificar */
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

.event-details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  max-width: 1000px;
  margin: 0 auto 3.5rem;
}

.detail-item {
  background: rgba(255, 255, 255, 0.05);
  padding: 2rem;
  border-radius: 12px;
  transition: transform 0.3s ease, background-color 0.3s ease;
}

.detail-item:hover {
  transform: translateY(-8px);
  background: rgba(255, 255, 255, 0.1);
}

.detail-icon {
  font-size: 2.5rem;
  color: var(--theme-primary-color, #3498db);
  margin-bottom: 1rem;
}

.detail-title {
  font-size: 0.9rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #bdc3c7;
  margin-bottom: 0.5rem;
}

.detail-text {
  font-size: clamp(1rem, 2.5vw, 1.1rem);
  color: #ffffff;
  font-weight: 500;
  line-height: 1.5;
}

.detail-text-address {
  font-size: 0.9rem;
  color: #bdc3c7;
  margin-top: 0.25rem;
}

.map-button {
  background-color: var(--theme-primary-color, #3498db);
  border-color: transparent;
  font-weight: 700;
  border-radius: 8px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  padding: 0.75rem 2rem;
}

.map-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
}

.map-button .material-symbols-outlined {
  margin-right: 0.5rem;
  vertical-align: middle;
}

/* Animation */
.ceremony-info-section.animate-on-scroll {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.8s ease, transform 0.8s ease;
}

.ceremony-info-section.animate-in {
  opacity: 1;
  transform: translateY(0);
}
</style>