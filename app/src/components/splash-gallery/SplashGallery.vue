<template>
  <div class="splash-gallery-container">
    <div class="splash-gallery-title">
      <div class="logo" ref="logoRef" />
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
        v-for="(image, index) in images"
        ref="galleryItemsRef"
        :key="index"
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
import { onMounted, onUnmounted, ref } from "vue";
import SplashGalleryItem from "./SplashGalleryItem.vue";
import VText from "@/components/VText.vue";
import gsap from "gsap";
const images = ref([]);

const count = ref(0);
const intervalId = ref(null);
const isVisible = ref(true);
const titleRef = ref(null);
const subTitleRef = ref(null);
const logoRef = ref(null);
const galleryItemsRef = ref([]);

const props = defineProps({
  title: {
    type: String,
    required: false,
    default: "Kayak to AI",
  },
  subTitle: {
    type: String,
    required: false,
    default: "Let Gemini guide your adventures",
  },
  imageContent: {
    type: Array,
    default: () => [
      {
        src: "https://fastly.picsum.photos/id/813/300/300.jpg?hmac=P1QaCX9HgZK2OE_XcRiYdFI9wkhiSmgYKor-9yDp00c",
        alt: "Image 1",
        caption: "Caption 1",
        position: {
          left: "10%",
          top: "10%",
          right: "auto",
          bottom: "auto",
        },
      },
      {
        src: "https://fastly.picsum.photos/id/960/300/300.jpg?hmac=33HCKWbjLrPghX-xdgDHytx4nbiWfmdQdI-Fwsgj_00",
        alt: "Image 2",
        caption: "Caption 2",
        position: {
          left: "auto",
          top: "10%",
          right: "10%",
          bottom: "auto",
        },
      },
      {
        src: "https://fastly.picsum.photos/id/813/300/300.jpg?hmac=P1QaCX9HgZK2OE_XcRiYdFI9wkhiSmgYKor-9yDp00c",
        alt: "Image 3",
        caption: "Caption 3 testing long caption",
        position: {
          left: "10%",
          right: "auto",
          top: "auto",
          bottom: "10%",
        },
      },
      {
        src: "https://fastly.picsum.photos/id/960/300/300.jpg?hmac=33HCKWbjLrPghX-xdgDHytx4nbiWfmdQdI-Fwsgj_00",
        alt: "Image 4",
        caption: "Caption 4",
        position: {
          left: "auto",
          top: "auto",
          right: "10%",
          bottom: "0%",
        },
      },
      {
        src: "https://fastly.picsum.photos/id/813/300/300.jpg?hmac=P1QaCX9HgZK2OE_XcRiYdFI9wkhiSmgYKor-9yDp00c",
        alt: "Image 5",
        caption: "Caption 5",
        position: {
          left: "auto",
          top: "auto",
          right: "30%",
          bottom: "10%",
        },
      },
      {
        src: "https://fastly.picsum.photos/id/960/300/300.jpg?hmac=33HCKWbjLrPghX-xdgDHytx4nbiWfmdQdI-Fwsgj_00",
        alt: "Image 6",
        caption: "Caption 6",
        position: {
          top: "0%",
          left: "30%",
          right: "auto",
          bottom: "auto",
        },
      },
    ],
  },
});

const imageContentRef = ref(props.imageContent);

async function spawnImage() {
  if (count.value >= imageContentRef.value.length) {
    count.value = 0;
  }

  const obj = {
    src: imageContentRef.value[count.value].src,
    position: imageContentRef.value[count.value].position,
    id: count.value,
    caption: imageContentRef.value[count.value].caption,
  };
  images.value.push(obj);
  count.value++;
}

function startInterval() {
  if (!intervalId.value) {
    spawnImage();
    intervalId.value = setInterval(spawnImage, 1500);
  }
}

function stopInterval() {
  if (intervalId.value) {
    clearInterval(intervalId.value);
    intervalId.value = null;
  }
}

function handleVisibilityChange() {
  if (document.hidden) {
    isVisible.value = false;
    stopInterval();
  } else {
    isVisible.value = true;
    startInterval();
  }
}

function handleItemDone(id) {
  console.log("item done", id);
}

async function animateIn(delay = 0) {
  startInterval();
  document.addEventListener("visibilitychange", handleVisibilityChange);

  await Promise.all([
    gsap.to([logoRef.value, titleRef.value.$el, subTitleRef.value.$el], {
      opacity: 1,
      duration: 3,
      z: 0,
      ease: "power2.out",
      delay: delay,
      stagger: 0.25,
    }),
  ]);
}

function animateOut() {
  gsap.to([logoRef.value, titleRef.value.$el, subTitleRef.value.$el], {
    opacity: 0,
    duration: 1,
    z: (index) => 100 + index * 50,
    ease: "power2.out",
  });
  galleryItemsRef.value.forEach((item) => {
    item.animateOut();
  });
  // animate out all the
  stopInterval();
}

defineExpose({
  animateIn,
  animateOut,
});

onMounted(() => {
  imageContentRef.value = props.imageContent;

  gsap.set([logoRef.value, titleRef.value.$el, subTitleRef.value.$el], {
    opacity: 0,
    z: -100,
  });

  //animateIn()
});

onUnmounted(() => {
  stopInterval();
  document.removeEventListener("visibilitychange", handleVisibilityChange);
});
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
