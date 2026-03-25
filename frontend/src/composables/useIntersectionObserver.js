import { ref, onMounted, onUnmounted } from 'vue';

export function useIntersectionObserver(targetRef, options = {}) {
  const isIntersecting = ref(false);
  const observer = ref(null);

  onMounted(() => {
    observer.value = new IntersectionObserver(([entry]) => {
      isIntersecting.value = entry.isIntersecting;
    }, options);

    if (targetRef.value) {
      observer.value.observe(targetRef.value);
    }
  });

  onUnmounted(() => {
    if (observer.value) {
      observer.value.disconnect();
    }
  });

  return { isIntersecting };
}
