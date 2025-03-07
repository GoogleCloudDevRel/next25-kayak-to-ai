<template>
  <IconGC class="icon" />
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
import { onMounted, shallowRef, nextTick, onUnmounted } from 'vue'
import { useRouteManager } from '@/router/useRouteManager'
import TvIntroScreen from '../routes/TvIntroScreen.vue'
import { getQueryParam } from '@/utils/get-query-param'
import TvLocationListScreen from '../routes/TvLocationListScreen.vue'
import TvRecoScreen from '../routes/TvRecoScreen.vue'
import TvFinalScreen from '../routes/TvFinalScreen.vue'
import IconGC from '@/components/icons/IconGC.vue'

const activeRoutes = shallowRef([])
const activeRoutesRef = shallowRef([])

const routes = {
  intro: TvIntroScreen,
  locations: TvLocationListScreen,
  reco: TvRecoScreen,
  final: TvFinalScreen,
}

const routeKeys = Object.keys(routes)

const {
  registerRoutes,
  navigateTo,
  isTransitioning,
  // Optional: Use this to customize how routes change behave
  // onRouteChange,
} = useRouteManager()

let index = 0
function handleClick(e) {
  e.preventDefault()
  if (isTransitioning.value) return
  if (index === routeKeys.length - 1) return
  navigateTo(routeKeys[++index])
}

window.navigateTo = navigateTo

// Register routes with their animations
onMounted(async () => {
  registerRoutes(routes, activeRoutes, activeRoutesRef)

  await nextTick()

  const initialView = routeKeys.find((key) => getQueryParam('view', false) === key)
  index = routeKeys.indexOf(initialView)
  index = index === -1 ? 0 : index

  navigateTo(initialView ?? 'intro')

  document.body.addEventListener('click', handleClick)
})

onUnmounted(() => {
  document.body.removeEventListener('click', handleClick)
})
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
  top: px-to-vw(120, 4k);
  left: px-to-vw(120, 4k);
  width: px-to-vw(163, 4k);
  height: auto;
}
</style>
