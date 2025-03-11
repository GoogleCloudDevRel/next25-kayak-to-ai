<template>
  <SplashGallery
    ref="galleryRef"
    title="Kayak to AI"
    subtitle="Let Gemini guide your adventures"
  />
</template>

<script setup>
import SplashGallery from "@/components/splash-gallery/SplashGallery.vue";
import { ref } from "vue";

const galleryRef = ref(null);

defineExpose({
  animateIn: async () => {
    await galleryRef.value.animateIn(0.5);
  },
  animateOut: async () => {
    await galleryRef.value.animateOut();
  },
});
</script>
