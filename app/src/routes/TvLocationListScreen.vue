<template>
  <div class="center">
    <VText
      ref="titleRef"
      text="Name an activity to get a location recommendation"
      variant="tv-bold-180"
      gradient
    />
    <ImageGrid
      :items="[
        {
          image: '/images/kayak/image-grid-1.jpg',
          caption: 'Shopping at Whidbey Island',
        },
        {
          image: '/images/kayak/image-grid-2.jpg',
          caption: 'Washington Park Arboretum',
        },
        {
          image: '/images/kayak/image-grid-3.jpg',
          caption: 'Hikes at Carkeek Park',
        },
        {
          image: '/images/kayak/image-grid-4.jpg',
          caption: 'Wildlife at Rattlesnake Ledge',
        },
      ]"
      ref="imageGridRef"
    />
  </div>
</template>

<script setup>
import ImageGrid from "@/components/image-grid/ImageGrid.vue";
import VText from "@/components/VText.vue";
import { ref, watch } from "vue";
import { useKayakStore } from "@/store";
import { storeToRefs } from "pinia";
import { useRouteManager } from "@/router/useRouteManager";

const imageGridRef = ref(null);
const titleRef = ref(null);

const kayakStore = useKayakStore();
const { prompt } = storeToRefs(kayakStore);
const { navigateTo } = useRouteManager();

watch(
  () => prompt.value,
  (value) => {
    console.log("prompt", value);
    if (value) {
      navigateTo("final");
    }
  }
);

defineExpose({
  animateSet: async () => {
    titleRef.value.prepare();
  },
  animateIn: async () => {
    await new Promise((resolve) => setTimeout(resolve, 2000));
    imageGridRef.value.animateIn();
    titleRef.value.animateIn();
  },
  animateOut: () => {
    imageGridRef.value.animateOut();
    titleRef.value.animateOut();
  },
});
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
