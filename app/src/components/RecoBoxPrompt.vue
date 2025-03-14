<template>
  <div
    class="wrapper reco-box-prompt"
    ref="wrapperRef"
  >
    <div class="title">
      <VText
        ref="titleRef"
        :text="prompt"
        :variant="isTv ? 'tv-body-48' : 'body-24'"
      />
    </div>
    <IconExit
      v-if="!isTv"
      class="icon"
      :onClick="() => navigateTo('prompt')"
    />
  </div>
</template>

<script setup>
import VText from '@/components/VText.vue'
import { ref } from 'vue'
import IconExit from './icons/IconExit.vue'
import { useKayakStore } from '@/store'
import { gsap } from '@/utils/gsap'
import { pxToVw } from '@/utils/px'
import { useRouteManager } from '@/router/useRouteManager'
import { storeToRefs } from 'pinia'

const titleRef = ref(null)
const wrapperRef = ref(null)
const kayakStore = useKayakStore()

const { prompt } = storeToRefs(kayakStore)

const { navigateTo } = useRouteManager()

defineProps({
  isTv: {
    type: Boolean,
    default: false,
  },
})

defineExpose({
  animateSet: async () => {
    await titleRef.value.prepare()
    gsap.set(wrapperRef.value, {
      clipPath: `inset(33% round ${pxToVw(32)})`,
      opacity: 0,
    })
  },
  animateIn: async (delay = 0) => {
    await Promise.all([
      titleRef.value.animateIn(delay),
      gsap.to(wrapperRef.value, {
        clipPath: `inset(-1px round ${pxToVw(32)})`,
        opacity: 1,
        duration: 1.2,
        ease: 'power2.inOut',
        delay,
      }),
    ])
  },
  animateOut: async () => {
    await gsap.to(wrapperRef.value, {
      clipPath: `inset(33% round ${pxToVw(32)})`,
      opacity: 0,
      duration: 0.8,
      ease: 'power2.inOut',
    })
  },
  el: () => wrapperRef.value,
})
</script>

<style lang="scss" scoped>
.wrapper {
  width: 100%;
  display: flex;
  align-items: center;
  gap: px-to-vw(24);
  padding: px-to-vw(36) px-to-vw(54);
  border-radius: px-to-vw(32);
  background: rgba(230, 244, 234, 0.1);
  @include gradient-border((45deg, rgba(78, 78, 78, 0.2), rgba(225, 225, 225, 0.2)), 2px);
  margin-bottom: px-to-vw(12);

  &::before {
    border-radius: px-to-vw(32);
  }

  .title {
    flex: 1;
  }

  .image {
    flex: 1;
  }

  img {
    width: 100%;
    aspect-ratio: 1;
    object-fit: cover;
    border-radius: px-to-vw(32);
  }

  .icon {
    cursor: pointer;
    position: absolute;
    right: px-to-vw(32);
    width: px-to-vw(48);
    height: px-to-vw(48);
  }
}
</style>
