<template>
  <div class="text" ref="el">
    {{ text }}
  </div>
</template>

<script setup>

import SplitText from '@activetheory/split-text';
import { isFontReady } from '@activetheory/split-text';
import gsap from 'gsap'

import { onMounted, ref } from 'vue';

const el = ref(null)
const splitText = ref(null)

const props = defineProps({
  text: String,
  splitType: {
    type: String,
    default: 'words, lines',
  },
  type: {
    type: String,
  },
  useBalance: {
    type: Boolean,
    default: true,
  },
  balanceRatio: {
    type: Number,
    default: 1,
  },
})

const animateSet = () => {
  for (const item of splitText.value[props.type || 'words']) {
    gsap.set(item, {
      yPercent: 110,
    })
  }
}

const animateIn = (delay = 0) => {
  gsap.to(splitText.value[props.type || 'words'], {
    yPercent: 0,
    ease: 'power1.inOut',
    duration: 0.7,
    stagger: 0.1,
    delay: delay,
  })
}

const handleResize = () => {
  splitText.value.revert();
  splitText.value.split();
}

onMounted(async () => {
  await isFontReady();
  splitText.value = new SplitText(el.value, {
    type: props.splitType || 'words, lines',
    balanceRatio: props.balanceRatio,
    useBalance: props.useBalance,
  })
  animateSet()
  window.addEventListener('resize', handleResize)
})

defineExpose({
  animateIn,
  animateSet,
})


</script>

<style lang="scss">
.line {
  overflow: hidden;
}

.text {
  padding: 0px;
  width: 100%;
}
</style>
