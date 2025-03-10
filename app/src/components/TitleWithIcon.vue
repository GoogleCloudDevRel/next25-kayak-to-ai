<template>
  <div class="title-with-icon">
    <IconBase v-if="icon" :variant="icon" ref="iconRef" />
    <VText ref="textRef" :text="title" :variant="textVariant" />
  </div>
</template>

<script setup>
defineProps({
  icon: {
    type: String,
    default: null,
  },
  title: {
    type: String,
    default: null,
  },
  textVariant: {
    type: String,
    default: "text-bold-24",
  },
});

import { onMounted, ref } from "vue";
import IconBase from "./IconBase.vue";
import VText from "./VText.vue";

const textRef = ref(null);
const iconRef = ref(null);
const animateIn = (delay = 0) => {
  textRef.value.animateIn(delay);
  iconRef.value.$el.classList.remove("hidden");
};

const animateOut = async (delay = 0) => {
  await textRef.value.animateOut(delay);
};

const animateSet = () => {
  textRef.value.animateSet();
  iconRef.value.$el.classList.add("hidden");
};

const prepare = async () => {
  await textRef.value.prepare();
};

onMounted(() => {
  iconRef.value.$el.classList.add("hidden");
});

defineExpose({
  animateIn,
  animateOut,
  animateSet,
  prepare,
  text: () => textRef.value,
});
</script>

<style lang="scss" scoped>
.title-with-icon {
  display: flex;
  align-items: center;
  gap: 10px;
}

.iconBase {
  transition: transform 0.3s ease-in-out;
}

.iconBase.hidden {
  transform: scale(0);
}
</style>
