<template>
  <section ref="dressCodeSectionRef" v-if="cliente.codigo_vestimenta"
    class="section dress-code-section animate-on-scroll" :class="{ 'animate-in': isIntersecting }">
    <div class="container has-text-centered">

      <div class="section-header">
        <h2 class="section-title" :style="{ fontFamily: `'${cliente.fuente_nombre}', cursive` }">Código de Vestimenta</h2>
        <p class="section-subtitle">Nos encantaría que nos acompañaras con tu mejor look en este día tan especial.</p>
      </div>

      <div class="dress-code-main">
        <div class="dress-code-icon">
          <span class="material-symbols-outlined">{{ details.icon }}</span>
        </div>
        <h3 class="dress-code-title">{{ cliente.codigo_vestimenta }}</h3>
        <p class="dress-code-description">{{ details.description }}</p>
      </div>

      <div class="color-palette-container">
        <h4 class="palette-title">Paleta de Colores Sugerida</h4>
        <div class="palette-circles">
          <div v-for="color in palette" :key="color" class="palette-circle" :style="{ backgroundColor: color }"></div>
        </div>
        <p class="palette-note">No es obligatorio, ¡es solo una fuente de inspiración!</p>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});

const dressCodeDetails = {
  'Formal': {
    icon: 'styler',
    description: 'Hombres: Traje formal oscuro y corbata. Mujeres: Vestido de noche largo.'
  },
  'Elegante': {
    icon: 'styler',
    description: 'Hombres: Traje formal, corbata opcional. Mujeres: Vestido de noche o de cóctel sofisticado.'
  },
  'Elegante Sport': {
    icon: 'tie',
    description: 'Hombres: Camisa y pantalón de vestir, con o sin saco. Mujeres: Vestido de cóctel o un conjunto chic.'
  },
  'Cóctel': {
    icon: 'nightlife',
    description: 'Hombres: Traje sin corbata o pantalón de vestir y un buen saco. Mujeres: Vestido corto o midi.'
  },
  'Casual': {
    icon: 'accessibility_new',
    description: 'Un look relajado pero arreglado. ¡Lo más importante es que te sientas a gusto!'
  },
   'Default': {
    icon: 'checkroom',
    description: 'Vení con tu mejor atuendo para celebrar.'
  }
};

const details = computed(() => {
  return dressCodeDetails[props.cliente.codigo_vestimenta] || dressCodeDetails['Default'];
});

// Paleta de colores predefinida. Se podría hacer dinámica en el futuro.
const palette = ref(['#8d99ae', '#A3B18A', '#588157', '#3A5A40', '#344E41']);

const dressCodeSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(dressCodeSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.dress-code-section {
  padding: clamp(3rem, 8vw, 6rem) 1.5rem;
  background-color: #2c3e50;
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

.dress-code-main {
  background: rgba(255, 255, 255, 0.05);
  max-width: 600px;
  margin: 0 auto 3rem;
  padding: 2.5rem;
  border-radius: 12px;
}

.dress-code-icon {
  margin-bottom: 1rem;
}
.dress-code-icon .material-symbols-outlined {
  font-size: 3.5rem;
  color: var(--theme-primary-color, #3498db);
  /* Estilo para iconos outlined */
  font-variation-settings:
  'FILL' 0,
  'wght' 300,
  'GRAD' 0,
  'opsz' 48;
}

.dress-code-title {
  font-size: 1.5rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #ffffff;
  margin-bottom: 0.75rem;
}

.dress-code-description {
  font-size: 1.1rem;
  color: #bdc3c7;
  line-height: 1.6;
}

.color-palette-container {
  max-width: 600px;
  margin: 0 auto;
}

.palette-title {
  font-size: 1rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: #bdc3c7;
  margin-bottom: 1.5rem;
}

.palette-circles {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1.5rem;
}

.palette-circle {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  border: 2px solid white;
  transition: transform 0.3s ease;
}
.palette-circle:hover {
  transform: scale(1.1);
}

.palette-note {
  font-size: 0.9rem;
  color: #95a5a6;
}

@media (max-width: 768px) {
  .dress-code-main {
    padding: 2rem 1.5rem;
  }
}
</style>