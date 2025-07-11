<template>
  <div
    class="center"
    ref="centerRef"
  >
    <div
      class="reco"
      ref="recoWrapperRef"
    >
      <RecoBoxPrompt ref="recoBoxPromptRef" />
      <RecoBox ref="recoBoxRef" />
      <div
        class="reco-group"
        ref="recoGroupRef"
      >
        <VButton
          ref="moveAgainButtonRef"
          text="Move Again"
          variant="outline"
          text-variant="bold-24"
          size="large"
          :onClick="() => navigateTo('prompt')"
        />
        <VButton
          ref="finishButtonRef"
          text="Finish"
          variant="primary"
          text-variant="bold-24"
          size="large"
          :onClick="() => navigateTo('intro')"
        />
      </div>
    </div>
    <div class="code-block">
      <CodeBlock
        ref="codeBlockRef"
        language="python"
        :codeSnippet="execCode"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

import RecoBox from '@/components/RecoBox.vue'
import RecoBoxPrompt from '@/components/RecoBoxPrompt.vue'
import CodeBlock from '@/components/CodeBlock.vue'

import { useKayakStore } from '@/store'
import { Flip, gsap } from '@/utils/gsap'
import { storeToRefs } from 'pinia'
import VButton from '@/components/VButton.vue'
import { useRouteManager } from '@/router/useRouteManager'
import { sendPrompt, checkIfKayakArrived } from '@/utils/api'

const recoBoxRef = ref(null)
const recoBoxPromptRef = ref(null)
const recoWrapperRef = ref(null)
const centerRef = ref(null)
const codeBlockRef = ref(null)
const recoGroupRef = ref(null)
const moveAgainButtonRef = ref(null)
const finishButtonRef = ref(null)

const kayakStore = useKayakStore()

const { isMoving, code: execCode, isArrived } = storeToRefs(kayakStore)

const { navigateTo } = useRouteManager()

let recoState = null

watch(
  () => isMoving.value,
  (value) => {
    if (!value) return
    recoState = Flip.getState([
      recoWrapperRef.value,
      recoBoxRef.value.el(),
      recoBoxPromptRef.value.el(),
      recoGroupRef.value,
    ])
    centerRef.value.classList.add('reco-with-code-exec')
    recoBoxRef.value.setProgressHeight()
    Flip.from(recoState, {
      duration: 1,
      ease: 'power2.inOut',
      onLeave: (elements) => {
        gsap.set(elements, {
          display: 'inherit',
          position: 'absolute',
        })
        gsap.to(elements, {
          opacity: 0,
          y: (_, el) => -1.125 * el.clientHeight,
          display: 'none',
          duration: 1,
          ease: 'power2.inOut',
        })
      },
      onComplete: () => {
        gsap.set(recoBoxRef.value.el(), {
          clearProps: 'height',
        })
      },
    })

    codeBlockRef.value.animateIn(0.5)

    checkIfKayakArrived()
  },
)

watch(
  () => isArrived.value,
  (value) => {
    if (value) {
      gsap.to(recoGroupRef.value, {
        height: recoGroupRef.value.scrollHeight + 2,
        duration: 1,
        ease: 'power2.inOut',
        delay: 3,
      })
    }
  },
)
defineExpose({
  animateSet: async () => {
    await Promise.all([
      recoBoxRef.value.animateSet(),
      recoBoxPromptRef.value.animateSet(),
      codeBlockRef.value.animateSet(),
      gsap.set(recoGroupRef.value, {
        height: 0,
      }),
    ])
  },
  animateIn: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000))
    await Promise.all([recoBoxPromptRef.value.animateIn(0), recoBoxRef.value.animateIn(0.2)])
    sendPrompt()
  },
  animateOut: async () => {
    await Promise.all([
      recoBoxRef.value.animateOut(),
      recoBoxPromptRef.value.animateOut(),
      codeBlockRef.value.animateOut(),
      moveAgainButtonRef.value.animateOut(),
      finishButtonRef.value.animateOut(),
    ])
    kayakStore.reset()
  },
})
</script>

<style lang="scss" scoped>
.center {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  padding-left: px-to-vw(277);
  padding-right: px-to-vw(277);

  .reco {
    display: flex;
    flex-direction: column;
    width: 100%;
    position: relative;
  }

  .code-block {
    position: absolute;
    top: 0;
    right: 0;
    width: 35vw;
    height: 100%;
    pointer-events: none;
  }

  .reco-group {
    display: flex;
    justify-content: center;
    width: 100%;
    gap: px-to-vw(16);
    padding-top: px-to-vw(54);
    overflow: hidden;
  }

  &.reco-with-code-exec,
  &.reco-with-code-exec-reveal {
    align-items: flex-start;
    padding-left: px-to-vw(116);

    .reco {
      width: 53vw;
    }

    :deep(.title .line) {
      white-space: nowrap;
    }

    :deep(.reco-box-prompt) {
      display: none;
    }
  }
}
</style>
