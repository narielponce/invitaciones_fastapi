<template>
  <section ref="gallerySectionRef" class="section gallery-section animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }">
    <div class="container">

      <div class="section-header has-text-centered">
        <h2 class="section-title" :style="{ fontFamily: `'${cliente.fuente_nombre}', cursive` }">Momentos Especiales</h2>
        <p class="section-subtitle">
          Capturamos algunos de nuestros momentos favoritos.
        </p>
      </div>

      <div v-if="clientImages.length > 0" class="photo-gallery-grid">
        <div v-for="(image, index) in clientImages" :key="index" class="gallery-item" @click="openLightbox(index)">
          <img :src="getFullImageUrl(image)" :alt="`Foto ${index + 1}`" class="gallery-image">
          <div class="gallery-overlay">
            <span class="material-symbols-outlined">zoom_in</span>
          </div>
        </div>
      </div>
      <div v-else class="has-text-centered">
        <p class="no-images-text">Próximamente, aquí habrá una galería de fotos.</p>
      </div>
    </div>

    <!-- Lightbox -->
    <div class="lightbox" :class="{ 'is-active': isLightboxOpen }" @click.self="closeLightbox">
      <div class="lightbox-content">
        <button class="lightbox-button close" @click="closeLightbox">
          <span class="material-symbols-outlined">close</span>
        </button>
        <button v-if="clientImages.length > 1" class="lightbox-button prev" @click.stop="prevImage">
          <span class="material-symbols-outlined">chevron_left</span>
        </button>
        <button v-if="clientImages.length > 1" class="lightbox-button next" @click.stop="nextImage">
          <span class="material-symbols-outlined">chevron_right</span>
        </button>

        <figure class="lightbox-figure">
          <transition name="fade" mode="out-in">
            <img :key="currentLightboxImage" :src="currentLightboxImage" alt="Imagen ampliada" class="lightbox-image">
          </transition>
        </figure>
        
        <div class="lightbox-counter" v-if="clientImages.length > 0">
          {{ currentImageIndex + 1 }} / {{ clientImages.length }}
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});

const API_BASE_URL = 'http://localhost:8000';

const clientImages = computed(() => {
  const images = [];
  for (let i = 1; i <= 9; i++) {
    if (props.cliente && props.cliente[`imagen${i}`]) {
      images.push(props.cliente[`imagen${i}`]);
    }
  }
  return images;
});

const getFullImageUrl = (relativePath) => {
  if (!relativePath) return '';
  return `${API_BASE_URL}/uploads/${relativePath}`;
};

const isLightboxOpen = ref(false);
const currentImageIndex = ref(0);

const currentLightboxImage = computed(() => {
  if (clientImages.value.length === 0 || currentImageIndex.value >= clientImages.value.length) return '';
  return getFullImageUrl(clientImages.value[currentImageIndex.value]);
});

const openLightbox = (index) => {
  currentImageIndex.value = index;
  isLightboxOpen.value = true;
  document.body.classList.add('is-clipped');
};

const closeLightbox = () => {
  isLightboxOpen.value = false;
  document.body.classList.remove('is-clipped');
};

const prevImage = () => { currentImageIndex.value = (currentImageIndex.value - 1 + clientImages.value.length) % clientImages.value.length; };
const nextImage = () => { currentImageIndex.value = (currentImageIndex.value + 1) % clientImages.value.length; };

const handleKeydown = (event) => {
  if (isLightboxOpen.value) {
    if (event.key === 'Escape') closeLightbox();
    if (event.key === 'ArrowLeft' && clientImages.value.length > 1) prevImage();
    if (event.key === 'ArrowRight' && clientImages.value.length > 1) nextImage();
  }
};

onMounted(() => {
  window.addEventListener('keydown', handleKeydown);
});
onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown);
  document.body.classList.remove('is-clipped');
});

const gallerySectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(gallerySectionRef, { threshold: 0.1 });
</script>

<style scoped>
.gallery-section {
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

.photo-gallery-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1rem;
}

.gallery-item {
  position: relative;
  overflow: hidden;
  cursor: pointer;
  aspect-ratio: 1 / 1;
  border-radius: 8px;
}

.gallery-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.gallery-item:hover .gallery-image {
  transform: scale(1.1);
}

.gallery-overlay {
  position: absolute;
  inset: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.4s ease;
  color: white;
}

.gallery-overlay .material-symbols-outlined {
  font-size: 3rem;
  transform: scale(0.8);
  transition: transform 0.4s ease;
}

.gallery-item:hover .gallery-overlay {
  opacity: 1;
}

.gallery-item:hover .gallery-overlay .material-symbols-outlined {
  transform: scale(1);
}

.no-images-text {
  color: #bdc3c7;
  font-size: 1.1rem;
  padding: 2rem;
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  max-width: 500px;
  margin: 2rem auto;
}

/* Lightbox */
.lightbox {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(10, 10, 10, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  visibility: hidden;
  transition: opacity 0.3s ease, visibility 0.3s ease;
}

.lightbox.is-active {
  opacity: 1;
  visibility: visible;
}

.lightbox-content {
  position: relative;
  width: 90%;
  height: 90%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-figure {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.lightbox-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
  border-radius: 4px;
}

.lightbox-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.4);
  color: white;
  border: none;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s ease;
}
.lightbox-button:hover {
  background: rgba(0, 0, 0, 0.7);
}
.lightbox-button .material-symbols-outlined {
  font-size: 32px;
}

.lightbox-button.close {
  top: 20px;
  right: 20px;
  transform: none;
  width: 40px;
  height: 40px;
}

.lightbox-button.prev {
  left: 20px;
}

.lightbox-button.next {
  right: 20px;
}

.lightbox-counter {
  position: absolute;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.9rem;
}

/* Transition for image change */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>