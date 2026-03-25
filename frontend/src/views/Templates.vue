<template>
  <div class="content-container">
    <div v-if="!showForm">
      <h2>Gestión de Templates</h2>
      <button @click="handleCreateNew" class="button-primary">Crear Nuevo Template</button>
      <table class="item-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nombre</th>
            <th>Slug</th>
            <th>Tipo de Evento</th>
            <th>Acciones</th>
          </tr>
        </thead>
        <tbody>
          <tr v-if="loading"><td colspan="5">Cargando...</td></tr>
          <tr v-else-if="error"><td colspan="5" class="error-text">Error: {{ error }}</td></tr>
          <tr v-for="template in templates" :key="template.id">
            <td>{{ template.id }}</td>
            <td>{{ template.nombre }}</td>
            <td>{{ template.slug }}</td>
            <td>{{ template.tipo_evento }}</td>
            <td class="actions">
              <button @click="handleEdit(template)" class="button-edit">Editar</button>
              <button @click="handleDelete(template.id)" class="button-delete">Borrar</button>
            </td>
          </tr>
          <tr v-if="!loading && !error && templates.length === 0">
            <td colspan="5">No hay templates para mostrar.</td>
          </tr>
        </tbody>
      </table>
    </div>

    <TemplateForm
      v-if="showForm"
      :template="selectedTemplate"
      @save="onSave"
      @cancel="closeForm"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { getTemplates, createTemplate, updateTemplate, deleteTemplate } from '../api';
import TemplateForm from '../components/TemplateForm.vue';

const templates = ref([]);
const loading = ref(true);
const error = ref(null);
const showForm = ref(false);
const selectedTemplate = ref(null);

const fetchTemplates = async () => {
  try {
    loading.value = true;
    error.value = null;
    templates.value = await getTemplates();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
};

onMounted(fetchTemplates);

const handleCreateNew = () => {
  selectedTemplate.value = null;
  showForm.value = true;
};

const handleEdit = (template) => {
  selectedTemplate.value = { ...template };
  showForm.value = true;
};

const handleDelete = async (id) => {
  if (confirm('¿Estás seguro de que quieres borrar este template?')) {
    try {
      await deleteTemplate(id);
      await fetchTemplates();
    } catch (e) {
      alert(`Error al borrar: ${e.message}`);
    }
  }
};

const onSave = async (templateData) => {
  try {
    if (templateData.id) {
      await updateTemplate(templateData.id, templateData);
    } else {
      await createTemplate(templateData);
    }
    await fetchTemplates();
    closeForm();
  } catch (e) {
    alert(`Error al guardar: ${e.message}`);
  }
};

const closeForm = () => {
  showForm.value = false;
  selectedTemplate.value = null;
};
</script>

<style scoped>
/* Reutilizando estilos del Dashboard/Clientes */
.content-container { font-family: Arial, sans-serif; }
h2 { margin-bottom: 1rem; }
.button-primary { background-color: #007bff; color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 4px; cursor: pointer; margin-bottom: 1rem; }
.item-table { width: 100%; border-collapse: collapse; margin-top: 1rem; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
.item-table th, .item-table td { border: 1px solid #ddd; padding: 0.75rem; text-align: left; }
.item-table thead { background-color: #f8f9fa; }
.actions { display: flex; gap: 0.5rem; }
.button-edit, .button-delete { padding: 0.4rem 0.8rem; border: none; border-radius: 4px; color: white; cursor: pointer; }
.button-edit { background-color: #ffc107; }
.button-delete { background-color: #dc3545; }
.error-text { color: #dc3545; }
</style>
