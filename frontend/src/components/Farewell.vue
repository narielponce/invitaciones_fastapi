<template>
  <section 
    ref="farewellSectionRef"
    class="section farewell-section animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }"
  >
    <div class="container has-text-centered">
      <div class="farewell-content">
        <p class="farewell-message">¡Te esperamos para celebrar!</p>
        <h2 class="farewell-signature">
          {{ cliente.nombre }}
        </h2>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});

const farewellSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(farewellSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.farewell-section {
  position: relative;
  padding: clamp(6rem, 15vw, 12rem) 1.5rem;
  background-color: var(--theme-background-secondary);
  color: var(--theme-text-primary);
}

.container {
  position: relative;
  z-index: 2;
}

.farewell-message {
  font-size: clamp(1.2rem, 3vw, 1.75rem);
  color: var(--theme-text-secondary);
  margin-bottom: 1.5rem;
  letter-spacing: 1px;
  font-family: var(--theme-font-main);
}

.farewell-signature {
  font-family: var(--theme-font-headings);
  font-size: clamp(3.5rem, 8vw, 7rem);
  line-height: 1.1;
  color: var(--theme-text-primary);
  text-shadow: 0 4px 15px rgba(0, 0, 0, 0.05); /* Sombra muy sutil para color sólido */
}

/* Animation */
.farewell-section.animate-on-scroll {
  opacity: 0;
  transform: scale(1.05);
  transition: opacity 1.2s ease, transform 1.2s ease;
}

.farewell-section.animate-in {
  opacity: 1;
  transform: scale(1);
}
</style>