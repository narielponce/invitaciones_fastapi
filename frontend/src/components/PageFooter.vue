<template>
  <footer 
    ref="footerRef"
    class="footer enhanced-footer animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }"
  >
    <div class="content has-text-centered">
      <div class="footer-content">
        <div class="footer-ornament"></div>
        <p class="footer-text">© {{ currentYear }} - Tu Fiesta Online. Todos los derechos reservados.</p>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const currentYear = new Date().getFullYear();

const footerRef = ref(null);
const { isIntersecting } = useIntersectionObserver(footerRef, { threshold: 0.1 });
</script>

<style scoped>
.enhanced-footer {
  padding: 3rem 1.5rem;
  background-color: #343a40;
  color: #f8f9fa;
}
.footer-ornament {
  height: 1px;
  background: #495057;
  width: 50%;
  margin: 0 auto 1rem;
}
</style>
