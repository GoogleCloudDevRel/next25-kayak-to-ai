<template>
  <div class="splash-gallery-container">
    <div class="splash-gallery-title">
      <div
        class="logo"
        ref="logoRef"
      />
      <VText
        ref="titleRef"
        :text="title"
        variant="tv-bold-500"
        class="title"
        gradient
      />
      <VText
        ref="subTitleRef"
        :text="subTitle"
        variant="tv-bold-100"
        class="sub-title"
        gradient
      />
    </div>
    <div class="splash-gallery">
      <SplashGalleryItem
        v-for="image in images"
        :key="image.uniqueId"
        ref="galleryItemsRef"
        :src="image.src"
        :alt="image.alt"
        :position="image.position"
        :caption="image.caption"
        :id="image.id"
        @item-done="handleItemDone"
      />
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from 'vue'
import SplashGalleryItem from './SplashGalleryItem.vue'
import VText from '@/components/VText.vue'
import gsap from 'gsap'
const images = ref([])
const imagesMap = ref(new Map())

const count = ref(0)
const intervalId = ref(null)
const isVisible = ref(true)
const titleRef = ref(null)
const subTitleRef = ref(null)
const logoRef = ref(null)
const galleryItemsRef = ref([])
const maxImagesDisplayed = ref(12)
const uniqueIdCounter = ref(0)

const props = defineProps({
  title: {
    type: String,
    required: false,
    default: 'Kayak to AI',
  },
  subTitle: {
    type: String,
    required: false,
    default: 'Let Gemini guide your adventures',
  },
  imageContent: {
    type: Array,
    default: () => [
      {
        src: 'https://storage.cloud.google.com/next-25-kayak-images/daniels_broiler.jpeg',
        alt: 'Image 1',
        caption: 'Have lunch',
        position: {
          left: '10%',
          top: '-10%',
          right: 'auto',
          bottom: 'auto',
        },
      },
      {
        src: 'https://storage.cloud.google.com/next-25-kayak-images/fremont_troll.jpeg',
        alt: 'Image 2',
        caption: 'See local art',
        position: {
          left: 'auto',
          top: '-7%',
          right: '7%',
          bottom: 'auto',
        },
      },
      {
        src: 'https://storage.cloud.google.com/next-25-kayak-images/husky_stadium.jpeg',
        alt: 'Image 3',
        caption: 'Watch American football',
        position: {
          left: '3%',
          right: 'auto',
          top: 'auto',
          bottom: '-8%',
        },
      },
      {
        src: 'https://storage.cloud.google.com/next-25-kayak-images/kirkland_urban.jpeg',
        alt: 'Image 4',
        caption: 'Go shopping!',
        position: {
          left: 'auto',
          top: 'auto',
          right: '5%',
          bottom: '-5%',
        },
      },
      {
        src: 'https://storage.cloud.google.com/next-25-kayak-images/luther_burbank.jpeg',
        alt: 'Image 5',
        caption: 'Enjoy a park day',
        position: {
          left: 'auto',
          top: 'auto',
          right: '30%',
          bottom: '-8%',
        },
      },
    ],
  },
})

const imageContentRef = ref(props.imageContent)

async function spawnImage() {
  if (count.value >= imageContentRef.value.length) {
    count.value = 0
  }

  if (imagesMap.value.size >= maxImagesDisplayed.value) {
    return
  }

  const uniqueId = uniqueIdCounter.value++
  const imageId = `img-${Date.now()}-${count.value}`

  const obj = {
    src: imageContentRef.value[count.value].src,
    position: imageContentRef.value[count.value].position,
    alt: imageContentRef.value[count.value].alt || '',
    id: imageId,
    uniqueId: uniqueId,
    caption: imageContentRef.value[count.value].caption,
  }

  images.value.push(obj)
  imagesMap.value.set(imageId, obj)

  count.value++
}

function startInterval() {
  if (!intervalId.value) {
    spawnImage()
    intervalId.value = setInterval(spawnImage, 2000)
  }
}

function stopInterval() {
  if (intervalId.value) {
    clearInterval(intervalId.value)
    intervalId.value = null
  }
}

function handleVisibilityChange() {
  if (document.hidden) {
    isVisible.value = false
    stopInterval()
  } else {
    isVisible.value = true
    startInterval()
  }
}

function handleItemDone(id) {
  imagesMap.value.delete(id)

  const index = images.value.findIndex((image) => image.id === id)
  if (index !== -1) {
    images.value.splice(index, 1)
  }
}

async function animateIn(delay = 0) {
  startInterval()
  document.addEventListener('visibilitychange', handleVisibilityChange)

  await Promise.all([
    gsap.to([logoRef.value, titleRef.value.$el, subTitleRef.value.$el], {
      opacity: 1,
      duration: 3,
      z: 0,
      ease: 'power2.out',
      delay: delay,
      stagger: 0.25,
    }),
  ])
}

function animateOut() {
  gsap.killTweensOf([logoRef.value, titleRef.value.$el, subTitleRef.value.$el])

  gsap.to([logoRef.value, titleRef.value.$el, subTitleRef.value.$el], {
    opacity: 0,
    duration: 1.6,
    z: (index) => 100 + index * 50,
    ease: 'power2.inOut',
    stagger: 0.1,
  })

  // Animate out all gallery items
  if (galleryItemsRef.value) {
    // Convert to array if it's not already
    const itemsArray = Array.isArray(galleryItemsRef.value)
      ? galleryItemsRef.value
      : Object.values(galleryItemsRef.value)

    itemsArray.forEach((item, i) => {
      if (item && typeof item.animateOut === 'function') {
        item.animateOut(i * 0.1)
      }
    })
  }

  stopInterval()
}

defineExpose({
  animateIn,
  animateOut,
})

onMounted(() => {
  imageContentRef.value = props.imageContent

  gsap.set([logoRef.value, titleRef.value.$el, subTitleRef.value.$el], {
    opacity: 0,
    z: -100,
  })

  //animateIn()
})

onUnmounted(() => {
  stopInterval()
  document.removeEventListener('visibilitychange', handleVisibilityChange)
  images.value = []
  imagesMap.value.clear()
})
</script>

<style lang="scss" scoped>
.splash-gallery-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  z-index: 1000;
}
.splash-gallery {
  position: relative;
  width: 100vw;
  height: 100vh;
  perspective: 600px;
}
.splash-gallery-title {
  position: absolute;
  width: 100vw;
  height: 100vh;
  left: 0;
  top: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  perspective: 600px;
  padding-bottom: 3%;
  .title,
  .sub-title {
    line-height: 1.2;
    transform-style: preserve-3d;
    opacity: 0;
  }
  .sub-title {
    margin-top: 0.5vw;
  }
}

.logo {
  width: px-to-vw(74);
  height: px-to-vw(74);
  background: linear-gradient(77.26deg, #e6f4ea -40.68%, $brandGreen 106.27%);
  clip-path: polygon(
    50% 100%,
    50% 100%,
    48.424% 93.121%,
    45.936% 86.536%,
    42.593% 80.292%,
    38.452% 74.434%,
    33.568% 69.009%,
    27.999% 64.064%,
    21.801% 59.644%,
    15.031% 55.796%,
    7.745% 52.566%,
    0% 50%,
    0% 50%,
    7.745% 47.434%,
    15.031% 44.204%,
    21.801% 40.356%,
    27.999% 35.936%,
    33.568% 30.991%,
    38.452% 25.566%,
    42.593% 19.708%,
    45.936% 13.464%,
    48.424% 6.879%,
    50% 0%,
    50% 0%,
    51.576% 6.879%,
    54.064% 13.464%,
    57.407% 19.708%,
    61.548% 25.566%,
    66.432% 30.991%,
    72.001% 35.936%,
    78.199% 40.356%,
    84.969% 44.204%,
    92.255% 47.434%,
    100% 50%,
    100% 50%,
    92.255% 52.566%,
    84.969% 55.796%,
    78.199% 59.644%,
    72.001% 64.064%,
    66.432% 69.009%,
    61.548% 74.434%,
    57.407% 80.292%,
    54.064% 86.536%,
    51.576% 93.121%,
    50% 100%
  );
}
</style>
