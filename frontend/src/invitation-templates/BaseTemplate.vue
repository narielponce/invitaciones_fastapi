<template>
  <div :class="['invitation-wrapper', themeClass]">
    <HeroSection :cliente="cliente" />
    <Countdown :cliente="cliente" />
    <EventInfo :cliente="cliente" />

    <!-- NUEVO: Mostrar Ceremonia si está activado -->
    <CeremonyInfo v-if="cliente.mostrar_ceremonia && cliente.fecha_ceremonia" :cliente="cliente" />
    
    <!-- Mostrar Galería si está activado -->
    <PhotoGallery v-if="cliente.mostrar_galeria" :cliente="cliente" />
    
    <RsvpForm :cliente="cliente" />
    
    <!-- Mostrar Dress Code si está activado -->
    <DressCode v-if="cliente.mostrar_dresscode" :cliente="cliente" />
    
    <!-- Mostrar Instagram si está activado -->
    <Social v-if="cliente.mostrar_instagram" :cliente="cliente" />
    
    <!-- Mostrar Playlist si está activado -->
    <PlaylistForm v-if="cliente.mostrar_playlist" :cliente="cliente" />
    
    <!-- Mostrar Regalos si está activado -->
    <Gifts v-if="cliente.mostrar_regalos" :cliente="cliente" />
    
    <Farewell :cliente="cliente" />
    <PageFooter />
  </div>
</template>

<script setup>
import { computed } from 'vue';
// Importar todos los componentes de sección que componen esta plantilla
import HeroSection from '../components/HeroSection.vue';
import Countdown from '../components/Countdown.vue';
import EventInfo from '../components/EventInfo.vue';
import CeremonyInfo from '../components/CeremonyInfo.vue';
import PhotoGallery from '../components/PhotoGallery.vue';
import RsvpForm from '../components/RsvpForm.vue';
import PlaylistForm from '../components/PlaylistForm.vue';
import DressCode from '../components/DressCode.vue';
import Social from '../components/Social.vue';
import Gifts from '../components/Gifts.vue';
import Farewell from '../components/Farewell.vue';
import PageFooter from '../components/PageFooter.vue';

const props = defineProps({
  cliente: {
    type: Object,
    required: true
  }
});

// --- CONFIGURACIÓN DE TEMA con Clases CSS ---
// Esta propiedad computada genera la clase del tema dinámicamente.
// Lee el 'slug' desde el objeto anidado 'cliente.template' que viene de la API.
const themeClass = computed(() => {
  const templateName = props.cliente?.template?.slug;
  return templateName ? `theme-${templateName}` : '';
});
</script>

<style scoped>
/* 
 * Los estilos base ahora aplican las variables definidas en 'src/assets/themes.css'.
 * El color, la tipografía y otros aspectos cambiarán según la clase de tema 
 * que se aplique a este div 'invitation-wrapper'.
 */
.invitation-wrapper {
  font-family: var(--theme-font-main);
  background-color: var(--theme-background-primary);
  color: var(--theme-text-primary);
  min-height: 100vh;
  /* Añadimos una transición suave para el cambio de fondo y color */
  transition: background-color 0.5s ease, color 0.5s ease;
}
</style>
