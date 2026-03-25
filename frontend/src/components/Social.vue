<template>
  <section ref="socialSectionRef" v-if="cliente.instagram_url"
    class="section social-section enhanced-social animate-on-scroll" :class="{ 'animate-in': isIntersecting }"
    :style="backgroundStyle">
    <div class="container">
      <div class="social-content-enhanced">
        <div class="social-icon-large">
          <div class="detail-icon">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
              class="instagram-icon">
              <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
              <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
              <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
            </svg>
          </div>
        </div>
        <h3 class="social-title">¡Compartí tus momentos!</h3>
        <p class="social-description">Etiquétame en tus fotos y videos del evento</p>
        <a :href="cliente.instagram_url" class="button is-link enhanced-social-btn" target="_blank">
          <span class="icon">
            <div class="detail-icon">
              <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="instagram-icon">
                <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
                <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
                <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
              </svg>
            </div>
          </span>
          <span>Ver Instagram</span>
        </a>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});
const API_BASE_URL = 'http://localhost:8000';

const backgroundStyle = computed(() => {
  if (props.cliente.imagen_fondo_ig) {
    const imageUrl = `${API_BASE_URL}/uploads/${props.cliente.imagen_fondo_ig}`;
    return {
      backgroundImage: `linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), url('${imageUrl}')`,
      backgroundSize: 'cover',
      backgroundPosition: 'center 20%',
    };
  }
  return { backgroundColor: '#222' };
});

const socialSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(socialSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.social-section {
  padding: 5rem 1.5rem;
  text-align: center;
  color: white;
}

.social-icon-large {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.social-title {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 0.5rem;
}

.social-description {
  margin-bottom: 1.5rem;
  font-size: 1.2rem;
}

.enhanced-social-btn {
  background-color: transparent;
  border-color: white;
  font-weight: bold;
}

.enhanced-social-btn:hover {
  background-color: rgba(255, 255, 255, 0.1);
}

.instagram-icon {
  /* Usamos el mismo tamaño que tus iconos de Google */
  width: 24px; 
  height: 24px;
  /* 'currentColor' hace que tome el color del texto de tu invitación automáticamente */
  color: inherit; 
  vertical-align: middle;
}

@media (max-width: 768px) {
  .social-section {
    padding: 4rem 1rem;
  }

  .social-title {
    font-size: 1.8rem;
  }

  .social-description {
    font-size: 1rem;
  }
}
</style>
