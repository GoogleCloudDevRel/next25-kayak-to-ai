<template>
  <div
    ref="imageContainer"
    class="splash-gallery-item"
  >
    <VCaption
      ref="captionRef"
      :caption="caption"
    />
    <div
      ref="imageInner"
      class="splash-gallery-item__inner"
    >
      <img
        ref="image"
        :src="src"
      />
    </div>
  </div>
</template>

<script setup>
import gsap from 'gsap'
import { onMounted, ref, onBeforeUnmount } from 'vue'
import VCaption from '@/components/splash-gallery/VCaption.vue'

const image = ref(null)
const imageContainer = ref(null)
const imageInner = ref(null)
const captionRef = ref(null)
const tlRef = ref(null)
const isAnimatingOut = ref(false)

onMounted(() => {
  // set style of image
  if (imageContainer.value) {
    imageContainer.value.style.left = `${props.position.left}`
    imageContainer.value.style.top = `${props.position.top}`
    imageContainer.value.style.right = `${props.position.right}`
    imageContainer.value.style.bottom = `${props.position.bottom}`

    if (props.animate) {
      initAnimate()
    }
  }
})

onBeforeUnmount(() => {
  // Clean up any animations when component is unmounted
  if (tlRef.value) {
    tlRef.value.kill()
  }
})

function animateIn() {
  if (captionRef.value) {
    captionRef.value.animateIn()
  }
}

function animateOut(delay = 0) {
  // Prevent multiple animate out calls
  if (isAnimatingOut.value) return
  isAnimatingOut.value = true

  if (tlRef.value) {
    tlRef.value.kill()
  }

  if (!imageContainer.value) return

  // Create a new timeline for the out animation
  const outTl = gsap.timeline({
    onComplete: () => {
      emit('itemDone', props.id)
    },
  })

  outTl.to(imageContainer.value, {
    z: 300,
    opacity: 0,
    duration: 1.6,
    ease: 'power2.inOut',
    delay: delay,
  })
}

defineExpose({
  animateIn,
  animateOut,
})

const emit = defineEmits(['itemDone'])

function initAnimate() {
  if (!imageContainer.value || !imageInner.value || !image.value) return

  const x = props.position.left === 'auto' ? -Math.random() * 50 : Math.random() * 50
  const y = props.position.top === 'auto' ? -Math.random() * 50 : Math.random() * 50

  const tl = gsap.timeline({
    defaults: {
      ease: 'power1.out',
    },
    onComplete: () => {
      if (!isAnimatingOut.value) {
        isAnimatingOut.value = true
        emit('itemDone', props.id)
      }
    },
  })

  tlRef.value = tl

  tl.set(imageContainer.value, {
    x: `${x}%`,
    y: `${y}%`,
    z: -300,
    opacity: 1,
  })
    .set(imageInner.value, {
      scale: 0,
    })
    .set(image.value, {
      scale: 4,
    })
    .call(() => {
      if (captionRef.value) {
        captionRef.value.animateIn()
      }
    })
    .to(
      imageInner.value,
      {
        scale: 1,
        duration: 2,
        ease: 'power1.out',
      },
      1,
    )
    .to(
      image.value,
      {
        scale: 1,
        duration: 2,
        ease: 'power1.out',
      },
      1,
    )
    .to(
      imageContainer.value,
      {
        z: 0,
        duration: 10,
      },
      '<',
    )
    .to(
      image.value,
      {
        scale: 1.5,
        duration: 15,
        delay: 2,
      },
      '<',
    )
    .to(
      imageContainer.value,
      {
        opacity: 0,
        duration: 3,
        delay: 6,
      },
      '<',
    )
}

const props = defineProps({
  src: {
    type: String,
    required: true,
  },
  position: {
    type: Object,
    required: true,
  },
  id: {
    type: [Number, String],
    required: true,
  },
  animate: {
    type: Boolean,
    required: false,
    default: true,
  },
  caption: {
    type: String,
    required: false,
    default: 'Testing',
  },
})
</script>

<style lang="scss" scoped>
.splash-gallery-item {
  position: absolute;
  top: 0;
  left: 0;
  transform-style: preserve-3d;
  will-change: transform, opacity;
  backface-visibility: hidden;
  -webkit-backface-visibility: hidden;
  opacity: 0;

  @include fluid(
    'width',
    (
      xxl: 200px,
      fourk: 624px,
    )
  );

  @include fluid(
    'height',
    (
      xxl: 200px,
      fourk: 624px,
    )
  );

  @include fluid(
    'border-radius',
    (
      xxl: 10px,
      fourk: 32px,
    )
  );

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transform-origin: center;
    will-change: transform;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
  }

  &__inner {
    width: 100%;
    height: 100%;
    transform-origin: center;
    overflow: hidden;
    border-radius: inherit;
    will-change: transform;
    backface-visibility: hidden;
    -webkit-backface-visibility: hidden;
  }
  .vcaption {
    position: absolute;
    top: 40%;
    right: 0;
    transform: translateX(50%, -50%);
    z-index: 100;
  }
}
</style>
