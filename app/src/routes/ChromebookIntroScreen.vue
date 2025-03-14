<template>
  <div class="center">
    <div
      class="logo"
      ref="logoRef"
    />
    <div class="title">
      <VText
        ref="titleRef"
        text="Kayak Seattle’s lakes with Gemini"
        variant="bold-128"
        gradient
      />
    </div>
    <div class="subtitle">
      <VText
        ref="subtitleRef"
        animate-by="lines"
        text="See how Gemini can take you where you want to go, through rapid prototyping with Gemini’s function calling, streaming, and multimodal APIs. Learn how you can build your own immersive AI experiences faster than ever."
        variant="bold-24"
      />
    </div>
    <div class="button">
      <VButton
        ref="buttonRef"
        text="Start Adventure"
        variant="primary"
        text-variant="bold-24"
        size="large"
        :onClick="() => navigateTo('prompt')"
      />
    </div>
  </div>
</template>
<script setup>
import VButton from '@/components/VButton.vue'
import VText from '@/components/VText.vue'
import { ref } from 'vue'
import { useRouteManager } from '@/router/useRouteManager'
import { gsap } from '@/utils/gsap'

const { navigateTo } = useRouteManager()

const titleRef = ref(null)
const subtitleRef = ref(null)
const buttonRef = ref(null)
const logoRef = ref(null)
defineExpose({
  animateSet: async () => {
    buttonRef.value.animateSet()
    await titleRef.value.prepare()
    await subtitleRef.value.prepare()
    gsap.set(logoRef.value, {
      scale: 0,
      rotate: 180,
    })
  },
  animateIn: async (to, from) => {
    if (from?.id === 'final') {
      await new Promise((resolve) => setTimeout(resolve, 1000))
    }
    gsap.to(logoRef.value, {
      duration: 1.2,
      ease: 'power2.inOut',
      scale: 1,
      rotate: 0,
    })
    titleRef.value.animateIn(0.2)
    subtitleRef.value.animateIn(0.8, { stagger: 0.2 })
    buttonRef.value.animateIn(1.2)
  },
  animateOut: async () => {
    await Promise.all([
      gsap.to(logoRef.value, {
        scale: 0,
        rotate: -180,
        duration: 1,
        ease: 'power2.inOut',
      }),
      titleRef.value.animateOut(),
      subtitleRef.value.animateOut(),
      buttonRef.value.animateOut(),
    ])
  },
})
</script>

<style lang="scss" scoped>
.logo {
  width: px-to-vw(74);
  height: px-to-vw(74);
  background: linear-gradient(77.26deg, #e6f4ea -40.68%, $brandGreen 106.27%);
  clip-path: polygon(
    50% 100%,
    50% 100%,
    48.424% 93.121%,
    45.936% 86.536%,
    42.593% 80.292%,
    38.452% 74.434%,
    33.568% 69.009%,
    27.999% 64.064%,
    21.801% 59.644%,
    15.031% 55.796%,
    7.745% 52.566%,
    0% 50%,
    0% 50%,
    7.745% 47.434%,
    15.031% 44.204%,
    21.801% 40.356%,
    27.999% 35.936%,
    33.568% 30.991%,
    38.452% 25.566%,
    42.593% 19.708%,
    45.936% 13.464%,
    48.424% 6.879%,
    50% 0%,
    50% 0%,
    51.576% 6.879%,
    54.064% 13.464%,
    57.407% 19.708%,
    61.548% 25.566%,
    66.432% 30.991%,
    72.001% 35.936%,
    78.199% 40.356%,
    84.969% 44.204%,
    92.255% 47.434%,
    100% 50%,
    100% 50%,
    92.255% 52.566%,
    84.969% 55.796%,
    78.199% 59.644%,
    72.001% 64.064%,
    66.432% 69.009%,
    61.548% 74.434%,
    57.407% 80.292%,
    54.064% 86.536%,
    51.576% 93.121%,
    50% 100%
  );
}

.title {
  margin-top: px-to-vw(134);
}

.center {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
}

.subtitle {
  margin-top: px-to-vw(60);
  max-width: px-to-vw(800);
}

.button {
  margin-top: px-to-vw(120);
}
</style>
