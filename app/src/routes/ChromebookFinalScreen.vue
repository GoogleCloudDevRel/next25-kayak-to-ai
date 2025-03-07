<template>
  <div class="center" ref="centerRef">
    <div class="reco" ref="recoWrapperRef">
      <RecoBoxPrompt ref="recoBoxPromptRef" />
      <RecoBox ref="recoBoxRef" />
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

import { useKayakStore } from "@/store";
import { Flip } from "@/utils/gsap";
import { storeToRefs } from "pinia";

const recoBoxRef = ref(null);
const recoBoxPromptRef = ref(null);
const recoWrapperRef = ref(null);
const centerRef = ref(null);
const codeBlockRef = ref(null);
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
        props: "width,x",
      });
      codeBlockRef.value.animateIn(0.5);
    }
  }
);

defineExpose({
  animateSet: async () => {
    await Promise.all([
      recoBoxRef.value.animateSet(),
      recoBoxPromptRef.value.animateSet(),
      codeBlockRef.value.animateSet(),
    ]);
  },
  animateIn: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    await Promise.all([
      recoBoxPromptRef.value.animateIn(0),
      recoBoxRef.value.animateIn(0.2),
    ]);
    recoState = Flip.getState(recoWrapperRef.value, {
      props: "width,x",
    });
  },
  animateOut: async () => {
    await Promise.all([
      recoBoxRef.value.animateOut(),
      recoBoxPromptRef.value.animateOut(),
      codeBlockRef.value.animateOut(),
    ]);
  },
});
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
    gap: px-to-vw(12);
  }

  &.reco-with-code-exec {
    align-items: flex-start;
    padding-left: px-to-vw(116);

    .reco {
      width: 53vw;
    }

    :deep(.title .line) {
      white-space: nowrap;
    }
  }
}

.code-block {
  position: absolute;
  top: 0;
  right: 0;
  width: 35vw;
  height: 100%;
  z-index: -1;
}
</style>
