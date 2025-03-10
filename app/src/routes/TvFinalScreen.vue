<template>
  <div class="center" ref="centerRef">
    <div class="reco" ref="recoWrapperRef">
      <VText
        ref="titleRef"
        text="AI Location Recommendation"
        variant="tv-bold-180"
        gradient
      />
      <div class="box">
        <RecoBoxPrompt ref="recoBoxPromptRef" :is-tv="true" />
        <RecoBox ref="recoBoxRef" :is-tv="true" />
      </div>
    </div>
    <div class="code-block">
      <CodeBlock ref="codeBlockRef" language="python">
        <template #default>
          <pre class="line-numbers">
            <code ref="code" v-html="execCode"></code>
          </pre>
        </template>
      </CodeBlock>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";

import RecoBox from "@/components/RecoBox.vue";
import RecoBoxPrompt from "@/components/RecoBoxPrompt.vue";
import CodeBlock from "@/components/CodeBlock.vue";
import VText from "@/components/VText.vue";

import { useKayakStore } from "@/store";
import { Flip, gsap } from "@/utils/gsap";
import { storeToRefs } from "pinia";

const recoBoxRef = ref(null);
const recoBoxPromptRef = ref(null);
const recoWrapperRef = ref(null);
const centerRef = ref(null);
const codeBlockRef = ref(null);
const titleRef = ref(null);

const kayakStore = useKayakStore();

const { isMoving, code: execCode } = storeToRefs(kayakStore);

let recoState = null;

watch(
  () => isMoving.value,
  (value) => {
    if (value) {
      centerRef.value.classList.add("reco-with-code-exec");
      Flip.from(recoState, {
        duration: 1,
        ease: "power2.inOut",
        onLeave: (elements) => {
          gsap.set(elements, {
            display: "inherit",
            position: "absolute",
          });
          gsap.to(elements, {
            opacity: 0,
            y: (_, el) => -1.125 * el.clientHeight,
            display: "none",
            duration: 1,
            ease: "power2.inOut",
          });
        },
      });
      codeBlockRef.value.animateIn(0.5);

      // TODO: change final reveal logic
      setTimeout(() => {
        kayakStore.setArrived(true);
      }, 3000);
    }
  }
);

defineExpose({
  animateSet: async () => {
    await Promise.all([
      recoBoxRef.value.animateSet(),
      recoBoxPromptRef.value.animateSet(),
      codeBlockRef.value.animateSet(),
      titleRef.value.prepare(),
    ]);
  },
  animateIn: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    await Promise.all([
      titleRef.value.animateIn(),
      recoBoxPromptRef.value.animateIn(0.2),
      recoBoxRef.value.animateIn(0.4),
    ]);

    recoState = Flip.getState([
      recoWrapperRef.value,
      recoBoxRef.value.el(),
      recoBoxPromptRef.value.el(),
    ]);

    // TODO: implement this
    await new Promise((resolve) => setTimeout(resolve, 1000));

    useKayakStore().setLocation({
      name: "Name of the Location",
      description: "Location Description",
      image: "/images/kayak/image-grid-1.jpg",
    });

    await new Promise((resolve) => setTimeout(resolve, 2000));

    useKayakStore().setIsMoving(true);
  },
  animateOut: async () => {
    await Promise.all([
      recoBoxRef.value.animateOut(),
      recoBoxPromptRef.value.animateOut(),
      codeBlockRef.value.animateOut(),
    ]);
    kayakStore.reset();
  },
});
</script>

<style lang="scss" scoped>
.center {
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-direction: column;
  padding-left: px-to-vw(1000, 4k);
  padding-right: px-to-vw(1000, 4k);

  .box {
    text-align: initial;
    padding-top: px-to-vw(190, 4k);
  }

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
    z-index: -1;
  }

  &.reco-with-code-exec,
  &.reco-with-code-exec-reveal {
    align-items: flex-start;
    padding-left: px-to-vw(250, 4k);

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
