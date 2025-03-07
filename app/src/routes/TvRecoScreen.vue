<template>
  <div class="center">
    <VText
      ref="titleRef"
      text="AI Location Recommendation"
      variant="tv-bold-180"
      gradient
    />
  </div>
</template>

<script setup>
import VText from '@/components/VText.vue'
import { ref } from 'vue'

const titleRef = ref(null)

defineExpose({
  animateSet: async () => {
    titleRef.value.prepare()
  },
  animateIn: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000))
    await titleRef.value.animateIn()
  },
  animateOut: async () => {
    await titleRef.value.animateOut()
  },
})
</script>

<style lang="scss" scoped>
.center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}
</style>
