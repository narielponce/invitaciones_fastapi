<template>
  <section 
    ref="heroSectionRef"
    class="hero is-fullheight hero-section animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }"
    :style="heroStyle"
  >
  <div class="hero-overlay"></div>
    <div class="hero-body hero-body-bottom">
      <div class="hero-bottom-text">
        <h1 class="hero-title font-shadows hero-title-color">
          {{ cliente.nombre }}
        </h1>
        <h2 class="hero-subtitle hero-title-color">
          {{ cliente.mensaje_bienvenida }}
        </h2>
      </div>
    </div>
    <div class="scroll-indicator-wrapper">
      <div class="scroll-indicator"></div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: {
    type: Object,
    required: true
  }
});

const API_BASE_URL = '/api';

const heroStyle = computed(() => {
  if (props.cliente && props.cliente.imagen_fondo) {
    const imageUrl = `${API_BASE_URL}/uploads/${props.cliente.imagen_fondo}`;
    return {
      backgroundImage: `url('${imageUrl}')`,
      backgroundSize: 'cover',
      backgroundPosition: 'center 30%',
    };
  }
  return {};
});

const heroSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(heroSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.hero-section {
  position: relative;
  overflow: hidden;
  color: var(--theme-text-primary);
}
.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    transparent,
    var(--theme-overlay-background)
  );
  z-index: 1;
}
.hero-body {
  position: relative;
  z-index: 2;
}
.hero-body-bottom {
  align-items: flex-end;
  justify-content: center;
  text-align: center;
  padding: 0 1.5rem 5rem 1.5rem; /* Añadido padding horizontal */
}
.hero-title {
  font-family: var(--theme-font-headings);
  font-size: clamp(3rem, 8vw, 6rem);
  letter-spacing: 2px;
  line-height: 1.1;

  opacity: 0;
  filter: blur(8px);
  transform: translateY(30px);
  transition: 
    opacity 1.2s ease,
    transform 1.2s ease,
    filter 1.2s ease;
}
.hero-title::after {
  content: "";
  display: block;
  width: 60px;
  height: 3px;
  background: var(--theme-primary-color);
  margin: 1rem auto 0;
  opacity: 0.8;
}
.hero-subtitle {
  font-family: var(--theme-font-main);
  font-size: clamp(1.2rem, 3vw, 2rem);
  font-weight: 400;
  opacity: 0;
  transform: translateY(20px);
  transition: all 1.2s ease 0.4s; /* delay */
}
.animate-on-scroll {
  opacity: 0;
  transform: scale(1.05);
  transition: all 1.5s ease;
}
.scroll-indicator-wrapper {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 2;
}

.animate-in {
  opacity: 1;
  transform: scale(1);
}
.animate-in .hero-title {
  opacity: 1;
  filter: blur(0);
  transform: translateY(0);
}
.animate-in .hero-subtitle {
  opacity: 0.9;
  transform: translateY(0);
}
.scroll-indicator {
  width: 24px;
  height: 40px;
  border: 2px solid var(--theme-text-primary);
  border-radius: 20px;
  margin: 2rem auto 0;
  position: relative;
}

.scroll-indicator::before {
  content: "";
  position: absolute;
  top: 8px;
  left: 50%;
  width: 4px;
  height: 8px;
  background: var(--theme-text-primary);
  transform: translateX(-50%);
  border-radius: 2px;
  animation: scrollAnim 1.5s infinite;
}

@keyframes scrollAnim {
  0% { opacity: 0; transform: translate(-50%, 0); }
  50% { opacity: 1; transform: translate(-50%, 8px); }
  100% { opacity: 0; transform: translate(-50%, 16px); }
}

/* Media Query para dispositivos pequeños */
@media (max-width: 768px) {
  .hero-section {
    background-position: center 10% !important;
  }
  .hero-title {
    font-size: 3.5rem; /* Reducir tamaño de fuente en móvil */
  }
  .hero-subtitle {
    font-size: 1.2rem; /* Reducir tamaño de fuente en móvil */
  }
  .hero-body-bottom {
    padding-bottom: 4rem; /* Menos padding inferior en móvil */
  }
}
</style>
