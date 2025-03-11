<template>
  <IconGC class="icon" />
  <div class="button">
    <VButton text="How it works" variant="outline" />
  </div>
  <div class="routes">
    <component
      v-for="route in activeRoutes"
      :is="route"
      ref="activeRoutesRef"
      :key="route.__name"
    />
  </div>
</template>

<script setup>
import { onMounted, shallowRef, nextTick, onUnmounted } from "vue";
import { useRouteManager } from "@/router/useRouteManager";
import ChromebookIntroScreen from "../routes/ChromebookIntroScreen.vue";
import { getQueryParam } from "@/utils/get-query-param";
import IconGC from "@/components/icons/IconGC.vue";
import ChromebookPromptScreen from "../routes/ChromebookPromptScreen.vue";
import ChromebookFinalScreen from "../routes/ChromebookFinalScreen.vue";
import VButton from "@/components/VButton.vue";
import { useKayakStore } from "@/store";
const activeRoutes = shallowRef([]);
const activeRoutesRef = shallowRef([]);

const routes = {
  intro: ChromebookIntroScreen,
  prompt: ChromebookPromptScreen,
  final: ChromebookFinalScreen,
};

const routeKeys = Object.keys(routes);

const {
  registerRoutes,
  navigateTo,
  isTransitioning,
  // Optional: Use this to customize how routes change behave
  onRouteChange,
} = useRouteManager();

onRouteChange((to, from) => {
  console.log("onRouteChange", to, from);
  useKayakStore().setRoute(to.id);
});

window.navigateTo = navigateTo;
let index = 0;
function handleClick(e) {
  e.preventDefault();
  if (isTransitioning.value) return;
  if (index === routeKeys.length - 1) return;
  navigateTo(routeKeys[++index]);
}

// Register routes with their animations
onMounted(async () => {
  registerRoutes(routes, activeRoutes, activeRoutesRef);

  await nextTick();

  const initialView = routeKeys.find(
    (key) => getQueryParam("view", false) === key
  );
  index = routeKeys.indexOf(initialView);
  index = index === -1 ? 0 : index;

  navigateTo(initialView ?? "intro");

  if (!getQueryParam("lock")) {
    document.body.addEventListener("click", handleClick);
  }
});

onUnmounted(() => {
  if (!getQueryParam("lock")) {
    document.body.removeEventListener("click", handleClick);
  }
});
</script>

<style lang="scss" scoped>
.routes > * {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}

.icon {
  position: absolute;
  top: px-to-vw(48);
  left: px-to-vw(48);
  width: px-to-vw(68);
  height: auto;
}

.button {
  position: absolute;
  top: px-to-vw(48);
  right: px-to-vw(48);
  z-index: 100;
}
</style>
