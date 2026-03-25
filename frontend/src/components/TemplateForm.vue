<template>
  <div class="form-container">
    <h3>{{ formTitle }}</h3>
    <form @submit.prevent="submitForm">
      <div class="form-grid">
        <div class="form-group">
          <label for="nombre">Nombre del Template</label>
          <input id="nombre" v-model="form.nombre" type="text" required />
        </div>
        <div class="form-group">
          <label for="slug">Slug</label>
          <input id="slug" v-model="form.slug" type="text" required />
        </div>
        <div class="form-group">
          <label for="tipo_evento">Tipo de Evento</label>
          <select id="tipo_evento" v-model="form.tipo_evento" required>
            <option value="15">Fiesta de 15</option>
            <option value="boda">Casamiento</option>
            <option value="cumple">Cumpleaños</option>
            <option value="infantil">Infantil</option>
            <option value="otros">Otros</option>
          </select>
        </div>
        <div class="form-group full-width">
          <label for="descripcion">Descripción</label>
          <textarea id="descripcion" v-model="form.descripcion"></textarea>
        </div>
      </div>
      <div class="form-actions">
        <button type="submit" class="button-primary">Guardar</button>
        <button type="button" @click="$emit('cancel')" class="button-secondary">Cancelar</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue';

const props = defineProps({
  template: { type: Object, default: null },
});
const emit = defineEmits(['save', 'cancel']);

const initialFormState = {
  nombre: '',
  slug: '',
  descripcion: '',
  tipo_evento: 'otros',
};

const form = ref({ ...initialFormState });

watch(() => props.template, (newTemplate) => {
  if (newTemplate) {
    form.value = { ...initialFormState, ...newTemplate };
  } else {
    form.value = { ...initialFormState };
  }
}, { immediate: true });

const formTitle = computed(() => (props.template ? 'Editar Template' : 'Crear Nuevo Template'));

const submitForm = () => {
  emit('save', { ...form.value });
};
</script>

<style scoped>
.form-container { background-color: #fff; padding: 2rem; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
h3 { margin-top: 0; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1rem; }
.full-width { grid-column: 1 / -1; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 4px; }
.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 1.5rem; }
.button-primary, .button-secondary { padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; }
.button-primary { background-color: #007bff; color: white; }
.button-secondary { background-color: #6c757d; color: white; }
</style>
