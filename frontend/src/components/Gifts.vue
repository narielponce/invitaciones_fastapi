<template>
  <section ref="giftsSectionRef" v-if="cliente.cbu || cliente.alias_regalos"
    class="section gift-section animate-on-scroll" :class="{ 'animate-in': isIntersecting }">
    <div class="container has-text-centered">

      <div class="section-header">
        <h2 class="section-title" :style="{ fontFamily: `'${cliente.fuente_nombre}', cursive` }">Un Detalle Especial</h2>
        <p class="section-subtitle">
          Tu presencia es nuestro mejor regalo. Pero si deseas tener un detalle con nosotros, te lo agradeceremos de corazón.
        </p>
      </div>

      <div class="gift-options-container">
        <!-- Bank Transfer Info -->
        <div class="gift-card">
          <div class="gift-card-header">
            <span class="material-symbols-outlined">account_balance</span>
            <h3>Transferencia Bancaria</h3>
          </div>
          <div class="gift-card-body">
            <p class="bank-account-name" v-if="cliente.titular_cuenta">A nombre de: {{ cliente.titular_cuenta }}</p>
            <div class="copyable-field" v-if="cliente.cbu">
              <span class="field-label">CBU</span>
              <span class="field-value">{{ cliente.cbu }}</span>
              <button class="button copy-button" @click="copyToClipboard(cliente.cbu, 'cbu')">
                <span class="material-symbols-outlined">{{ cbuCopied ? 'check' : 'content_copy' }}</span>
                <span>{{ cbuCopied ? 'Copiado' : 'Copiar' }}</span>
              </button>
            </div>
            <div class="copyable-field" v-if="cliente.alias_regalos">
              <span class="field-label">Alias</span>
              <span class="field-value">{{ cliente.alias_regalos }}</span>
              <button class="button copy-button" @click="copyToClipboard(cliente.alias_regalos, 'alias')">
                <span class="material-symbols-outlined">{{ aliasCopied ? 'check' : 'content_copy' }}</span>
                <span>{{ aliasCopied ? 'Copiado' : 'Copiar' }}</span>
              </button>
            </div>
          </div>
        </div>

        <!-- QR Code -->
        <div class="gift-card" v-if="cliente.imagen_qr_regalos">
          <div class="gift-card-header">
            <span class="material-symbols-outlined">qr_code_2</span>
            <h3>Mercado Pago</h3>
          </div>
          <div class="gift-card-body qr-body">
            <img :src="getFullImageUrl(cliente.imagen_qr_regalos)" alt="Código QR para Mercado Pago" class="qr-image">
             <p class="qr-instruction">Escaneá el código para transferir</p>
          </div>
        </div>

      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const props = defineProps({
  cliente: { type: Object, required: true }
});

const API_BASE_URL = 'http://localhost:8000';

const cbuCopied = ref(false);
const aliasCopied = ref(false);

const copyToClipboard = async (text, type) => {
  try {
    await navigator.clipboard.writeText(text);
    if (type === 'cbu') {
      cbuCopied.value = true;
      setTimeout(() => cbuCopied.value = false, 2000);
    } else if (type === 'alias') {
      aliasCopied.value = true;
      setTimeout(() => aliasCopied.value = false, 2000);
    }
  } catch (err) {
    console.error('Error al copiar: ', err);
    // Opcional: mostrar un mensaje de error al usuario
  }
};

const getFullImageUrl = (relativePath) => {
  if (!relativePath) return '';
  return `${API_BASE_URL}/uploads/${relativePath}`;
};

const giftsSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(giftsSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.gift-section {
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

.gift-options-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 900px;
  margin: 0 auto;
}

.gift-card {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  padding: 2rem;
  text-align: left;
}

.gift-card-header {
  display: flex;
  align-items: center;
  gap: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  padding-bottom: 1rem;
  margin-bottom: 1.5rem;
}

.gift-card-header .material-symbols-outlined {
  font-size: 2rem;
  color: var(--theme-primary-color, #3498db);
}

.gift-card-header h3 {
  font-size: 1.25rem;
  font-weight: 700;
  color: #ffffff;
}

.bank-account-name {
  font-size: 0.9rem;
  color: #bdc3c7;
  margin-bottom: 1.5rem;
}

.copyable-field {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: 1rem;
  background: rgba(0, 0, 0, 0.2);
  padding: 0.5rem 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.field-label {
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  color: #95a5a6;
}

.field-value {
  font-family: monospace;
  font-size: 1rem;
  color: #ecf0f1;
  overflow-wrap: anywhere;
}

.copy-button {
  background: transparent;
  border: 1px solid #566573;
  color: #bdc3c7;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.25rem 0.75rem;
  transition: all 0.2s ease;
}
.copy-button:hover {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}
.copy-button .material-symbols-outlined {
  font-size: 1rem;
}

.qr-body {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}
.qr-image {
  max-width: 200px;
  width: 100%;
  aspect-ratio: 1/1;
  background: white;
  padding: 1rem;
  border-radius: 8px;
}
.qr-instruction {
  font-size: 0.9rem;
  color: #bdc3c7;
  text-align: center;
}
</style>