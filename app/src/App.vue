<template>
  <BackgroundBase v-slot="{ oglState }">
    <BackgroundGradient
      :oglState="oglState"
      v-bind="{
        bgColor: '#000000',
        fade: 0.5,
        disk1: {
          color: '#137c2e',
          center: {
            x: -0.6,
            y: -0.34,
          },
          radius: 0.1,
          type: 'group',
        },
        disk2: {
          color: '#276136',
          center: {
            x: 0.75,
            y: -0.44,
          },
          radius: 0.31599999999999995,
          type: 'group',
        },
        disk3: {
          color: '#90f5aa',
          center: {
            x: -0.26,
            y: -0.13,
          },
          radius: -0.27,
          type: 'group',
        },
        disk4: {
          color: '#d2ffdd',
          center: {
            x: 1.62,
            y: 0.09,
          },
          radius: -0.06,
          type: 'group',
        },
      }"
      :animate="true"
    />
  </BackgroundBase>
  <main class="kayak">
    <component :is="currentRoute" ref="currentRouteRef" />
  </main>
</template>

<script setup>
import "@/styles/global.scss";

import { ref, computed } from "vue";

import TvView from "@/views/TVView.vue";
import ChromebookView from "@/views/ChromebookView.vue";
import NotFoundView from "@/views/NotFoundView.vue";
import BackgroundBase from "@/components/background/BackgroundBase.vue";
import BackgroundGradient from "@/components/background/BackgroundGradient.vue";

const routes = {
  "/": TvView,
  "/chromebook": ChromebookView,
};

const currentPath = ref(window.location.hash);

window.addEventListener("hashchange", () => {
  currentPath.value = window.location.hash;
});

const currentRoute = computed(() => {
  return routes[currentPath.value.slice(1) || "/"] || NotFoundView;
});
</script>

<style lang="scss">
.hidden-svg {
  position: absolute;
  width: 0;
  height: 0;
}
</style>
