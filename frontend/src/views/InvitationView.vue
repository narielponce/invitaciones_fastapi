<template>
  <div v-if="loading" class="loading-container">
    <p>Cargando invitación...</p>
  </div>
  <div v-else-if="error" class="error-container">
    <h2>Error</h2>
    <p>{{ error }}</p>
  </div>
  <div v-else-if="cliente">
    <!-- 
      Este es el cargador dinámico.
      Renderizará el componente que corresponda según el 'slug' del template.
    -->
    <component 
      :is="activeTemplateComponent" 
      :cliente="cliente" 
    />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { getInvitationByEventTypeAndSlug } from '../api';

// Importa aquí TODAS las plantillas de invitación disponibles
// Ahora usaremos DefaultTemplate como nuestro "TemplateBase" universal
import DefaultTemplate from '../invitation-templates/BaseTemplate.vue';
// Puedes renombrar el archivo a TemplateBase.vue si prefieres, pero aquí lo importamos así.

const route = useRoute();
const cliente = ref(null);
const loading = ref(true);
const error = ref(null);

// Esta propiedad computada decide qué componente de plantilla mostrar
const activeTemplateComponent = computed(() => {
  // En este enfoque unificado, siempre retornamos el Template Base.
  // La "magia" de diferenciación ocurrirá dentro de ese componente mediante CSS y Props.
  return DefaultTemplate;
});


onMounted(async () => {
  const { tipo_evento, slug } = route.params;
  if (!slug || !tipo_evento) {
    error.value = 'No se ha especificado una invitación válida.';
    loading.value = false;
    return;
  }

  try {
    cliente.value = await getInvitationByEventTypeAndSlug(tipo_evento, slug);
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
});
</script>

<style scoped>
.loading-container, .error-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  font-size: 1.5rem;
}
.error-container {
  color: #dc3545;
}
</style>
