<template>
  <div class="center">
    <VText
      ref="titleRef"
      text="What activity would you like to do in Seattle?"
      variant="bold-80"
      gradient
    />
    <div class="choices">
      <MultiChoiceMenu
        @selection-change="handleSelectionChange"
        :items="[
          {
            label: 'I want to get some food',
            icon: 'Burger',
            value: 'food',
          },
          {
            label: 'I want to see a historical site',
            icon: 'Historical',
            value: 'historical',
          },
          {
            label: 'I want to go shopping',
            icon: 'Shopping',
            value: 'shopping',
          },
          {
            label: 'I want to see local wildlife',
            icon: 'Raven',
            value: 'wildlife',
          },
        ]"
        :square="true"
        ref="multiChoiceMenuRef"
      />
    </div>
    <div class="input">
      <InputMicrophone
        ref="inputMicrophoneRef"
        cta="I want to ..."
        language="en-US"
        @input-microphone-send="handleInputMicrophoneSend"
      />
    </div>
  </div>
</template>

<script setup>
import InputMicrophone from "@/components/input-microphone/InputMicrophone.vue";
import MultiChoiceMenu from "@/components/multi-choice/MultiChoiceMenu.vue";
import VText from "@/components/VText.vue";
import { ref } from "vue";
import { useKayakStore } from "@/store";
import { useRouteManager } from "@/router/useRouteManager";

const titleRef = ref(null);
const multiChoiceMenuRef = ref(null);
const inputMicrophoneRef = ref(null);

const { navigateTo } = useRouteManager();

const handleSelectionChange = ({ label }) => {
  useKayakStore().setPrompt(label);
  navigateTo("final");
};

const handleInputMicrophoneSend = ({ speechText }) => {
  useKayakStore().setPrompt(speechText);
  navigateTo("final");
};

defineExpose({
  animateSet: async () => {
    await titleRef.value.prepare();
    multiChoiceMenuRef.value.animateSet();
    inputMicrophoneRef.value.animateSet();
  },
  animateIn: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    titleRef.value.animateIn();
    multiChoiceMenuRef.value.animateIn(0.5);
    inputMicrophoneRef.value.animateIn(1);
  },
  animateOut: async () => {
    await Promise.all([
      titleRef.value.animateOut(),
      multiChoiceMenuRef.value.animateOut(),
      inputMicrophoneRef.value.animateOut(),
    ]);
  },
});
</script>

<style lang="scss" scoped>
.center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding-left: px-to-vw(280);
  padding-right: px-to-vw(280);
}

.choices {
  margin-top: px-to-vw(120);
  width: 100%;
}

.input {
  margin-top: px-to-vw(120);
  width: 100%;
}
</style>
