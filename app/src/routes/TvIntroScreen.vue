<template>
  <SplashGallery
    ref="galleryRef"
    title="Kayak to AI"
    subtitle="Let Gemini guide your adventures"
  />
</template>

<script setup>
import SplashGallery from "@/components/splash-gallery/SplashGallery.vue";
import { ref, watch } from "vue";
import { useKayakStore } from "@/store";
import { storeToRefs } from "pinia";
import { useRouteManager } from "@/router/useRouteManager";

const galleryRef = ref(null);

const kayakStore = useKayakStore();

const { isStarted } = storeToRefs(kayakStore);

const { navigateTo } = useRouteManager();

watch(
  () => isStarted.value,
  (value) => {
    console.log("isStarted", value);
    if (value) {
      navigateTo("locations");
    }
  }
);

defineExpose({
  animateIn: async () => {
    await galleryRef.value.animateIn(0.5);
  },
  animateOut: async () => {
    await galleryRef.value.animateOut();
  },
});
</script>
