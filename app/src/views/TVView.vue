<template>
  <IconGC class="icon" />
  <div class="routes is-tv">
    <component
      v-for="route in activeRoutes"
      :is="route"
      ref="activeRoutesRef"
      :key="route.__name"
    />
  </div>
  <QRCode :value="'https://www.google.com'" />
</template>

<script setup>
import { onMounted, shallowRef, nextTick, onUnmounted, watch } from 'vue'
import { useRouteManager } from '@/router/useRouteManager'
import TvIntroScreen from '@/routes/TvIntroScreen.vue'
import { getQueryParam } from '@/utils/get-query-param'
import TvPromptScreen from '@/routes/TvPromptScreen.vue'
import TvFinalScreen from '@/routes/TvFinalScreen.vue'
import IconGC from '@/components/icons/IconGC.vue'
import { useKayakStore } from '@/store'
import { storeToRefs } from 'pinia'
import QRCode from '@/components/QRCode.vue'

const activeRoutes = shallowRef([])
const activeRoutesRef = shallowRef([])

const routes = {
  intro: TvIntroScreen,
  prompt: TvPromptScreen,
  final: TvFinalScreen,
}

const kayakStore = useKayakStore()
const { route } = storeToRefs(kayakStore)

const routeKeys = Object.keys(routes)

const {
  registerRoutes,
  navigateTo,
  isTransitioning,
  // Optional: Use this to customize how routes change behave
} = useRouteManager()

let index = 0
function handleClick(e) {
  e.preventDefault()
  if (isTransitioning.value) return
  if (index === routeKeys.length - 1) return
  navigateTo(routeKeys[++index])
}

watch(
  () => route.value,
  (value) => {
    console.log('route', value)
    navigateTo(value)
  },
)

window.navigateTo = navigateTo

// Register routes with their animations
onMounted(async () => {
  registerRoutes(routes, activeRoutes, activeRoutesRef)

  await nextTick()

  const initialView = routeKeys.find((key) => getQueryParam('view', false) === key)
  index = routeKeys.indexOf(initialView)
  index = index === -1 ? 0 : index

  navigateTo(initialView ?? 'intro')

  if (getQueryParam('manual')) {
    document.body.addEventListener('click', handleClick)
  }
})

onUnmounted(() => {
  if (getQueryParam('manual')) {
    document.body.removeEventListener('click', handleClick)
  }
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
