<template>
  <div class="client-form-container">
    <form @submit.prevent="submitForm">
      <h3>{{ formTitle }}</h3>
      
      <!-- Pestañas para navegar entre secciones del formulario -->
      <div class="tabs">
        <button type="button" @click="activeTab = 'datos'" :class="{ active: activeTab === 'datos' }">Datos Principales</button>
        <button type="button" @click="activeTab = 'ceremonia'" :class="{ active: activeTab === 'ceremonia' }">Ceremonia</button>
        <button type="button" @click="activeTab = 'visibilidad'" :class="{ active: activeTab === 'visibilidad' }">Visibilidad</button>
        <button type="button" @click="activeTab = 'imagenes'" :class="{ active: activeTab === 'imagenes' }" :disabled="!isEditMode">Imágenes</button>
      </div>

      <!-- Contenido de la pestaña DATOS -->
      <div v-show="activeTab === 'datos'">
        <h4>Datos Principales</h4>
        <div class="form-grid">
          <div class="form-group"> <label for="nombre">Nombre</label> <input id="nombre" v-model="form.nombre" type="text" required /> </div>
          <div class="form-group"> <label for="titulo">Título</label> <input id="titulo" v-model="form.titulo" type="text" required /> </div>
          <div class="form-group"> <label for="slug">Slug</label> <input id="slug" v-model="form.slug" type="text" required /> </div>
          <div class="form-group"> <label for="email">Email</label> <input id="email" v-model="form.email" type="email" required /> </div>
          <div class="form-group"> <label for="telefono_envio_confirmacion">Teléfono para Confirmación</label> <input id="telefono_envio_confirmacion" v-model="form.telefono_envio_confirmacion" type="text" /> </div>
          <div class="form-group"> <label for="template_id">Template</label> <select id="template_id" v-model="form.template_id"> <option :value="null">-- Ninguno --</option> <option v-for="template in templates" :key="template.id" :value="template.id">{{ template.nombre }}</option> </select> </div>
        </div>

        <h4>Detalles del Evento (Fiesta)</h4>
        <div class="form-grid">
          <div class="form-group"> <label for="fecha_evento">Fecha del Evento</label> <input id="fecha_evento" v-model="form.fecha_evento" type="date" required /> </div>
          <div class="form-group"> <label for="hora_evento">Hora del Evento</label> <input id="hora_evento" v-model="form.hora_evento" type="time" /> </div>
          <div class="form-group"> <label for="tipo_evento">Tipo de Evento</label> <select id="tipo_evento" v-model="form.tipo_evento" required> <option value="15">Fiesta de 15</option> <option value="boda">Casamiento</option> <option value="cumple">Cumpleaños</option> <option value="infantil">Infantil</option> <option value="otros">Otros</option> </select> </div>
          <div class="form-group"> <label for="lugar_evento">Lugar del Evento</label> <input id="lugar_evento" v-model="form.lugar_evento" type="text" /> </div>
          <div class="form-group"> <label for="direccion_evento">Dirección del Evento</label> <textarea id="direccion_evento" v-model="form.direccion_evento"></textarea> </div>
        </div>
        
        <h4>Personalización</h4>
        <div class="form-grid">
          <div class="form-group"> <label for="mensaje_bienvenida">Mensaje de Bienvenida</label> <textarea id="mensaje_bienvenida" v-model="form.mensaje_bienvenida"></textarea> </div>
          <div class="form-group"> <label for="codigo_vestimenta">Código de Vestimenta</label> <input id="codigo_vestimenta" v-model="form.codigo_vestimenta" type="text" /> </div>
          <div class="form-group"> <label for="fuente_nombre">Fuente del Nombre</label> <select id="fuente_nombre" v-model="form.fuente_nombre"> <option value="Great+Vibes">Great Vibes</option> <option value="Dancing+Script">Dancing Script</option> <option value="Allura">Allura</option> <option value="Sacramento">Sacramento</option> <option value="Parisienne">Parisienne</option> </select> </div>
          <div class="form-group"> <label for="instagram_url">URL de Instagram</label> <input id="instagram_url" v-model="form.instagram_url" type="url" /> </div>
          <div class="form-group"> <label for="alias_regalos">Alias/CBU para Regalos</label> <input id="alias_regalos" v-model="form.alias_regalos" type="text" /> </div>
        </div>
      </div>

      <!-- Contenido de la pestaña CEREMONIA -->
      <div v-show="activeTab === 'ceremonia'">
        <h4>Detalles de la Ceremonia Religiosa</h4>
        <div class="form-grid">
          <div class="form-group"> <label for="fecha_ceremonia">Fecha de la Ceremonia</label> <input id="fecha_ceremonia" v-model="form.fecha_ceremonia" type="date" /> </div>
          <div class="form-group"> <label for="hora_ceremonia">Hora de la Ceremonia</label> <input id="hora_ceremonia" v-model="form.hora_ceremonia" type="time" /> </div>
          <div class="form-group"> <label for="lugar_ceremonia">Lugar de la Ceremonia</label> <input id="lugar_ceremonia" v-model="form.lugar_ceremonia" type="text" /> </div>
          <div class="form-group"> <label for="direccion_ceremonia">Dirección de la Ceremonia</label> <textarea id="direccion_ceremonia" v-model="form.direccion_ceremonia"></textarea> </div>
        </div>
      </div>

      <!-- Contenido de la pestaña VISIBILIDAD -->
      <div v-show="activeTab === 'visibilidad'">
        <h4>Mostrar/Ocultar Secciones</h4>
        <div class="form-grid">
          <div class="form-group form-group-checkbox"> <input type="checkbox" id="mostrar_ceremonia" v-model="form.mostrar_ceremonia" /> <label for="mostrar_ceremonia">Mostrar Ceremonia</label> </div>
          <div class="form-group form-group-checkbox"> <input type="checkbox" id="mostrar_galeria" v-model="form.mostrar_galeria" /> <label for="mostrar_galeria">Mostrar Galería</label> </div>
          <div class="form-group form-group-checkbox"> <input type="checkbox" id="mostrar_dresscode" v-model="form.mostrar_dresscode" /> <label for="mostrar_dresscode">Mostrar Dress Code</label> </div>
          <div class="form-group form-group-checkbox"> <input type="checkbox" id="mostrar_instagram" v-model="form.mostrar_instagram" /> <label for="mostrar_instagram">Mostrar Instagram</label> </div>
          <div class="form-group form-group-checkbox"> <input type="checkbox" id="mostrar_playlist" v-model="form.mostrar_playlist" /> <label for="mostrar_playlist">Mostrar Playlist</label> </div>
          <div class="form-group form-group-checkbox"> <input type="checkbox" id="mostrar_regalos" v-model="form.mostrar_regalos" /> <label for="mostrar_regalos">Mostrar Regalos</label> </div>
        </div>
      </div>

      <!-- Contenido de la pestaña IMÁGENES -->
      <div v-show="activeTab === 'imagenes'">
        <h4>Gestión de Imágenes</h4>
        <div v-if="!isEditMode" class="alert-info">Guarda el cliente primero para poder subir imágenes.</div>
        <div v-else class="image-grid">
          <div v-for="field in imageFields" :key="field.name" class="image-upload-group">
            <label>{{ field.label }}</label>
            <div class="image-path-display">{{ form[field.name] || 'No hay imagen' }}</div>
            <input type="file" @change="event => handleImageUpload(event, field.name)" accept="image/*" class="file-input" :id="'file-input-' + field.name" />
            <button type="button" @click="triggerFileInput(field.name)" class="button-secondary">
              {{ uploadStatus[field.name] === 'loading' ? 'Subiendo...' : 'Seleccionar...' }}
            </button>
            <div v-if="uploadStatus[field.name] && uploadStatus[field.name] !== 'loading'" :class="uploadStatus[field.name].startsWith('Error') ? 'error-text' : 'success-text'">
              {{ uploadStatus[field.name] }}
            </div>
          </div>
        </div>
      </div>

      <!-- Acciones del formulario -->
      <div class="form-actions">
        <button type="submit" class="button-primary">Guardar Cambios</button>
        <button type="button" @click="$emit('cancel')" class="button-secondary">Cerrar</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted } from 'vue';
import { getTemplates, uploadClienteImage } from '../api';

const props = defineProps({
  cliente: { type: Object, default: null },
});
const emit = defineEmits(['save', 'cancel', 'client-updated']);

const activeTab = ref('datos');

const initialFormState = {
  nombre: '', titulo: '', slug: '', email: '', telefono_envio_confirmacion: '',
  template_id: null, tipo_evento: 'otros', fecha_evento: '', fuente_nombre: 'Great+Vibes',
  mensaje_bienvenida: '', hora_evento: '', lugar_evento: '', direccion_evento: '',
  codigo_vestimenta: '', instagram_url: '', alias_regalos: '',

  // Nuevos campos de Ceremonia
  fecha_ceremonia: '', hora_ceremonia: '', lugar_ceremonia: '', direccion_ceremonia: '',

  // Nuevas banderas de Visibilidad
  mostrar_ceremonia: false, mostrar_galeria: true, mostrar_dresscode: true,
  mostrar_instagram: true, mostrar_playlist: true, mostrar_regalos: true,
  
  // Campos de imagen
  imagen_fondo: '', imagen_fondo_ig: '', imagen1: '', imagen2: '', imagen3: '', 
  imagen4: '', imagen5: '', imagen6: '', imagen7: '', imagen8: '', imagen9: '',
};

const form = ref({ ...initialFormState });
const templates = ref([]);
const uploadStatus = ref({});

const isEditMode = computed(() => !!props.cliente);
const formTitle = computed(() => (isEditMode.value ? `Editar Cliente: ${props.cliente.nombre}` : 'Crear Nuevo Cliente'));

const imageFields = [
  { name: 'imagen_fondo', label: 'Imagen de Fondo' },
  { name: 'imagen_fondo_ig', label: 'Imagen Fondo (Instagram)' },
  ...Array.from({ length: 9 }, (_, i) => ({ name: `imagen${i + 1}`, label: `Imagen de Galería ${i + 1}` }))
];

watch(() => props.cliente, (newCliente) => {
  if (newCliente) {
    form.value = { ...initialFormState, ...newCliente };
    activeTab.value = 'datos';
  } else {
    form.value = { ...initialFormState };
  }
}, { immediate: true, deep: true });

const submitForm = () => {
  const dataToSave = { ...form.value };
  
  // Limpiar campos opcionales para que el backend los acepte
  if (dataToSave.template_id === '-- Ninguno --') dataToSave.template_id = null;
  if (dataToSave.hora_evento === '') dataToSave.hora_evento = null;
  if (dataToSave.fecha_ceremonia === '') dataToSave.fecha_ceremonia = null;
  if (dataToSave.hora_ceremonia === '') dataToSave.hora_ceremonia = null;

  emit('save', dataToSave);
};

onMounted(async () => {
  try {
    templates.value = await getTemplates();
  } catch (error) { console.error("Error al cargar los templates:", error); }
});

const triggerFileInput = (fieldName) => {
  document.getElementById(`file-input-${fieldName}`).click();
};

const handleImageUpload = async (event, fieldName) => {
  const file = event.target.files[0];
  if (!file) return;

  uploadStatus.value[fieldName] = 'loading';

  try {
    const updatedClient = await uploadClienteImage(props.cliente.id, fieldName, file);
    form.value = { ...initialFormState, ...updatedClient };
    uploadStatus.value[fieldName] = '¡Subido!';
    emit('client-updated');
    setTimeout(() => { uploadStatus.value[fieldName] = null; }, 3000);
  } catch (error) {
    console.error(`Error subiendo ${fieldName}:`, error);
    uploadStatus.value[fieldName] = `Error: ${error.message}`;
  }
};
</script>

<style scoped>
h3, h4 { border-bottom: 2px solid #eee; padding-bottom: 0.5rem; margin-bottom: 1.5rem; }
.form-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
.form-group label { display: block; margin-bottom: 0.5rem; font-weight: 500; }
.form-group input, .form-group select, .form-group textarea { width: 100%; padding: 0.75rem; border: 1px solid #ccc; border-radius: 4px; font-size: 1rem; box-sizing: border-box; }
.form-group textarea { min-height: 100px; resize: vertical; }
.form-actions { display: flex; justify-content: flex-end; gap: 1rem; margin-top: 2rem; }
.button-primary, .button-secondary { padding: 0.75rem 1.5rem; border: none; border-radius: 4px; font-size: 1rem; cursor: pointer; }
.button-primary { background-color: #007bff; color: white; }
.button-secondary { background-color: #6c757d; color: white; }

/* Estilos de pestañas e imágenes */
.tabs { display: flex; border-bottom: 1px solid #ccc; margin-bottom: 1.5rem; }
.tabs button { background: none; border: none; padding: 10px 15px; cursor: pointer; font-size: 1rem; color: #555; transition: all 0.3s ease; border-radius: 5px 5px 0 0; margin-right: 5px; }
.tabs button:hover:not(.active) { background-color: #f0f0f0; }
.tabs button.active { color: #007bff; border-bottom: 3px solid #007bff; font-weight: bold; }
.tabs button:disabled { color: #ccc; cursor: not-allowed; }

.alert-info { background-color: #e9ecef; padding: 1rem; border-radius: 4px; text-align: center; margin-bottom: 1.5rem; }

.image-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
.image-upload-group { background: #f8f9fa; padding: 1rem; border-radius: 4px; }
.image-upload-group label { font-weight: bold; display: block; margin-bottom: 0.5rem; }
.image-path-display { background: #fff; padding: 0.5rem; border-radius: 4px; border: 1px solid #eee; margin-bottom: 0.5rem; font-size: 0.9em; color: #555; word-wrap: break-word; }
.file-input { display: none; }
.error-text { color: #dc3545; font-size: 0.9em; margin-top: 0.5rem; }
.success-text { color: #28a745; font-size: 0.9em; margin-top: 0.5rem; }

.form-group-checkbox { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 1rem; }
.form-group-checkbox input[type="checkbox"] { width: auto; }
</style>
