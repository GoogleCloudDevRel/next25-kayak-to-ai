<template>
  <SplashGallery
    ref="galleryRef"
    title="Kayak to AI"
    subtitle="Take a virtual kayaking adventure guided by Gemini"
  />
</template>

<script setup>
import SplashGallery from '@/components/splash-gallery/SplashGallery.vue'
import { ref } from 'vue'

const galleryRef = ref(null)

defineExpose({
  animateIn: async (to, from) => {
    if (from?.id === 'final') {
      await new Promise((resolve) => setTimeout(resolve, 1000))
    }
    galleryRef.value.animateIn()
  },
  animateOut: async () => {
    await galleryRef.value.animateOut()
  },
})
</script>
