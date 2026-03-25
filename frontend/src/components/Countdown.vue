<template>
  <section ref="countdownSectionRef" class="section countdown-section animate-on-scroll"
    :class="{ 'animate-in': isIntersecting }" id="cuenta-regresiva">
    <div class="container has-text-centered">
      <div class="section-header">
        <!--<div class="section-ornament"></div>-->
        <p class="countdown-message">¡Te espero para festejar este gran momento!</p>
        <!--<h2 class="section-title">Solo faltan</h2>-->
      </div>

      <div class="countdown-wrapper">
        <div class="countdown-item">
          <div class="countdown-number" :class="{ bump: animateDays }">{{ days }}</div>
          <div class="countdown-label">Días</div>
        </div>

        <div class="countdown-item">
          <div class="countdown-number" :class="{ bump: animateHours }">{{ hours }}</div>
          <div class="countdown-label">Horas</div>
        </div>

        <div class="countdown-item">
          <div class="countdown-number" :class="{ bump: animateMinutes }">{{ minutes }}</div>
          <div class="countdown-label">Min</div>
        </div>

        <div class="countdown-item">
          <div class="countdown-number" :class="{ bump: animateSeconds }">{{ seconds }}</div>
          <div class="countdown-label">Seg</div>
        </div>
      </div>

    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue';
import { useIntersectionObserver } from '../composables/useIntersectionObserver';

const animateDays = ref(false);
const animateHours = ref(false);
const animateMinutes = ref(false);
const animateSeconds = ref(false);

const props = defineProps({
  cliente: {
    type: Object,
    required: true
  }
});

const eventDate = ref(null);
const days = ref('--');
const hours = ref('--');
const minutes = ref('--');
const seconds = ref('--');
let countdownInterval = null;

const formatTime = (time) => String(Math.max(0, time)).padStart(2, '0');

const triggerAnimation = () => {
  numbers.forEach(el => {
    el.classList.add('bump');
    setTimeout(() => el.classList.remove('bump'), 200);
  });
};

const updateCountdown = () => {
  if (!eventDate.value) return;

  const now = new Date();
  const distance = eventDate.value.getTime() - now.getTime();

  if (distance < 0) {
    clearInterval(countdownInterval);
    days.value = hours.value = minutes.value = seconds.value = '00';
    return;
  }

  const newDays = formatTime(Math.floor(distance / (1000 * 60 * 60 * 24)));
  const newHours = formatTime(Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)));
  const newMinutes = formatTime(Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60)));
  const newSeconds = formatTime(Math.floor((distance % (1000 * 60)) / 1000));

  if (newDays !== days.value) {
    animateDays.value = true;
    setTimeout(() => animateDays.value = false, 200);
  }

  if (newHours !== hours.value) {
    animateHours.value = true;
    setTimeout(() => animateHours.value = false, 200);
  }

  if (newMinutes !== minutes.value) {
    animateMinutes.value = true;
    setTimeout(() => animateMinutes.value = false, 200);
  }

  // segundos siempre cambian
  animateSeconds.value = true;
  setTimeout(() => animateSeconds.value = false, 200);

  days.value = newDays;
  hours.value = newHours;
  minutes.value = newMinutes;
  seconds.value = newSeconds;
};

const initializeCountdown = () => {
  clearInterval(countdownInterval);
  if (props.cliente && props.cliente.fecha_evento && props.cliente.hora_evento) {
    const dateStr = props.cliente.fecha_evento;
    const timeStr = props.cliente.hora_evento;
    eventDate.value = new Date(`${dateStr}T${timeStr}`);
    if (!isNaN(eventDate.value)) {
      updateCountdown();
      countdownInterval = setInterval(updateCountdown, 1000);
    } else {
      days.value = hours.value = minutes.value = seconds.value = '--';
    }
  } else {
    days.value = hours.value = minutes.value = seconds.value = '--';
  }
};

onMounted(initializeCountdown);
onUnmounted(() => clearInterval(countdownInterval));
watch(() => props.cliente, initializeCountdown, { deep: true });

const countdownSectionRef = ref(null);
const { isIntersecting } = useIntersectionObserver(countdownSectionRef, { threshold: 0.1 });
</script>

<style scoped>
.countdown-section {
  padding: 4rem 1.5rem;
  background-color: hsl(51, 20%, 67%);
}

.section-header {
  margin-bottom: 2rem;
}

.section-ornament {
  width: 60px;
  height: 2px;
  background: var(--theme-primary-color);
  margin: 0 auto 1.5rem;
  opacity: 0.6;
}

.countdown-wrapper {
  display: flex;
  justify-content: center;
  gap: clamp(1.5rem, 4vw, 3rem);
  margin-top: 3rem;
  text-align: center;
}

.countdown-item {
  display: flex;
  flex-direction: column;
}

.countdown-number {
  font-size: clamp(2.5rem, 6vw, 4rem);
  font-weight: 600;
  color: white;
  line-height: 1;
  transition: transform 0.25s ease;
}

.countdown-label {
  font-size: 0.75rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  opacity: 0.6;
  margin-top: 0.6rem;
  color: white;
}
.countdown-number.bump {
  transform: scale(1.12);
}
.countdown-message {
  font-size: 1.2rem;
  color: white
}

.section-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #444;
  margin-top: 0.5rem;
}

.number {
  transition: transform 0.15s ease-out;
}

/* Media Query para dispositivos pequeños */
@media (max-width: 768px) {
  .countdown-section {
    padding: 3rem 1rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
}
</style>
