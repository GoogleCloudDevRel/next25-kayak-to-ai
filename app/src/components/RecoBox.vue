<template>
  <div
    class="wrapper"
    ref="wrapperRef"
  >
    <div
      class="content"
      ref="contentRef"
    >
      <div class="title">
        <div class="subtitle-container">
          <div
            class="skeleton"
            :ref="setSkeletonRef"
          />
          <TitleWithIcon
            ref="subtitleRef"
            icon="gemini"
            title="Recommended Location"
            :textVariant="isTv ? 'tv-medium-34' : 'medium-18'"
          />
        </div>
        <div :class="['title-container', isTv ? 'text-tv-bold-180' : 'text-medium-80']">
          <div
            class="skeleton"
            :ref="setSkeletonRef"
          />
          <VText
            ref="titleRef"
            :text="locationName"
            :variant="isTv ? 'tv-bold-180' : 'medium-80'"
            :min-lines="2"
          />
        </div>
      </div>
      <div class="image">
        <div
          class="image-container"
          ref="imageRef"
        >
          <img
            :src="locationImage"
            :alt="locationName"
          />
        </div>
        <div
          class="skeleton image-skeleton"
          :ref="setSkeletonRef"
        />
      </div>
    </div>
    <div
      class="collapse"
      ref="collapseRef"
      v-if="!isTv"
    >
      <div class="collapse-content">
        <div class="divider"></div>
        <VText
          ref="textRef"
          text="Do you want to move the Kayak to this location?"
          variant="medium-24"
        />
        <div class="group">
          <VButton
            text="No, Try Again"
            variant="outline"
            text-variant="bold-24"
            size="large"
            :onClick="() => navigateTo('prompt')"
          />
          <VButton
            text="Yes, Let's Go"
            variant="primary"
            text-variant="bold-24"
            size="large"
            :onClick="moveKayakAndGetCode"
          />
        </div>
      </div>
    </div>
    <div
      class="collapse"
      ref="collapse2Ref"
    >
      <div class="collapse-content text-color-gray">
        <div class="divider"></div>
        <VText
          text="Watch the map to see AI move the Kayak"
          variant="medium-24"
        />
        <div class="progress-group">
          <IconPin class="pin" />
          <IconKayak
            class="kayak"
            ref="kayakIconRef"
          />
          <div class="progress-bar">
            <div
              class="progress-bar-fill"
              ref="progressRef"
            />
          </div>
          <IconPin class="pin pin-right" />
        </div>
      </div>
    </div>
    <div
      class="collapse"
      ref="collapse3Ref"
    >
      <div class="collapse-content">
        <div class="divider"></div>
        <VText
          :text="locationDescription"
          variant="body-24"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import VText from '@/components/VText.vue'
import { gsap } from '@/utils/gsap'
import { computed, ref, watch } from 'vue'
import VButton from './VButton.vue'
import IconPin from '@/components/icons/IconPin.vue'
import { useKayakStore } from '@/store'
import IconKayak from '@/components/icons/IconKayak.vue'
import { pxToVw } from '@/utils/px'
import { useRouteManager } from '@/router/useRouteManager'
import { storeToRefs } from 'pinia'
import TitleWithIcon from './TitleWithIcon.vue'
import { moveKayakAndGetCode } from '@/utils/api'
const titleRef = ref(null)
const collapseRef = ref(null)
const collapse2Ref = ref(null)
const collapse3Ref = ref(null)
const contentRef = ref(null)
const wrapperRef = ref(null)
const subtitleRef = ref(null)
const imageRef = ref(null)
const progressRef = ref(null)
const kayakIconRef = ref(null)

const skeletonRef = ref([])

const setSkeletonRef = (el) => {
  if (el) {
    skeletonRef.value.push(el)
  }
}

const props = defineProps({
  isTv: {
    type: Boolean,
    default: false,
  },
})

const kayakStore = useKayakStore()

const { isMoving, isArrived, location } = storeToRefs(kayakStore)

const locationName = computed(() => {
  return location.value?.name || 'Name of the Location'
})

const locationImage = computed(() => {
  return location.value?.image || '/images/kayak/image-grid-1.jpg'
})

const locationDescription = computed(() => {
  return location.value?.description || 'Description of the Location'
})

const { navigateTo } = useRouteManager()

async function changeSubtitle(text) {
  const subtitle = subtitleRef.value.text()
  await subtitle.prepare(false)
  await subtitle.animateSet(false)
  subtitle.animateOut(0, { duration: 0.6 }).then(async () => {
    await subtitle.setText(text)
    subtitle.animateIn()
  })
}

watch(
  () => location.value,
  async () => {
    if (!location.value) return

    await titleRef.value.setText(location.value.name)

    await Promise.all([
      subtitleRef.value.animateIn(),
      titleRef.value.animateIn(0.1),
      gsap.to(imageRef.value, {
        opacity: 1,
        scale: 1,
        duration: 1,
        ease: 'power2.inOut',
      }),
      gsap.fromTo(
        skeletonRef.value,
        {
          clipPath: `inset(0% 0% 0% 0% round ${pxToVw(32)})`,
        },
        {
          clipPath: `inset(0% 0% 0% 100% round ${pxToVw(32)})`,
          duration: 1,
          ease: 'power2.inOut',
        },
      ),
    ])

    if (!props.isTv) {
      await new Promise((resolve) => setTimeout(resolve, 1000))

      gsap.to(contentRef.value, {
        height: Math.max(
          contentRef.value.scrollHeight - collapseRef.value.scrollHeight,
          (300 / 1920) * window.innerWidth,
        ),
        duration: 1,
        ease: 'power2.inOut',
      })

      gsap.to(collapseRef.value, {
        height: collapseRef.value.scrollHeight,
        duration: 1,
        ease: 'power2.inOut',
        onComplete: () => {
          gsap.set(collapseRef.value, {
            height: 'auto',
          })
        },
      })
    }
  },
)

watch(
  () => isMoving.value,
  async (isMoving) => {
    if (!isMoving) return
    await changeSubtitle('Moving Kayak to:')

    if (props.isTv) {
      gsap.to(contentRef.value, {
        height: Math.max(
          contentRef.value.scrollHeight - collapse2Ref.value.scrollHeight,
          (869 / 3840) * window.innerHeight,
        ),
        duration: 1,
        ease: 'power2.inOut',
      })
    } else {
      gsap.to(collapseRef.value, {
        height: 0,
        duration: 1,
        ease: 'power2.inOut',
      })
    }

    gsap.to(collapse2Ref.value, {
      height: collapse2Ref.value.scrollHeight,
      duration: 0.3,
      ease: 'power2.out',
      onComplete: () => {
        gsap.set(collapse2Ref.value, {
          height: 'auto',
        })

        handleProgress()
      },
    })
  },
)

const handleProgress = () => {
  const progress = 0.6
  gsap.to(progressRef.value, {
    width: progress * 72 + '%',
    duration: 5,
    ease: 'power2.inOut',
  })
  gsap.to(kayakIconRef.value.ref(), {
    left: progress * 68.35 + '%',
    duration: 5,
    ease: 'power2.inOut',
  })
}

watch(
  () => isArrived.value,
  async (isArrived) => {
    if (!isArrived) return

    gsap.killTweensOf(progressRef.value)
    gsap.killTweensOf(kayakIconRef.value.ref())

    changeSubtitle('Arrived at:')

    await Promise.all([
      gsap.to(progressRef.value, {
        width: 72 + '%',
        duration: 1,
        ease: 'power2.inOut',
      }),

      gsap.to(kayakIconRef.value.ref(), {
        left: 68.35 + '%',
        duration: 1,
        ease: 'power2.inOut',
      }),
    ])

    gsap.to(collapse2Ref.value, {
      height: 0,
      duration: 1,
      ease: 'power2.inOut',
    })

    gsap.to(collapse3Ref.value, {
      height: collapse3Ref.value.scrollHeight,
      duration: 1,
      ease: 'power2.inOut',
      onComplete: () => {
        gsap.set(collapse3Ref.value, {
          height: 'auto',
        })
      },
    })
  },
)

defineExpose({
  setProgressHeight: () => {
    const padding = (54 / 1920) * window.innerWidth
    const minHeight = (869 / 3840) * window.innerHeight
    gsap.set(wrapperRef.value, {
      height: props.isTv
        ? Math.max(contentRef.value.scrollHeight - collapse2Ref.value.scrollHeight, minHeight) +
          collapse2Ref.value.scrollHeight +
          padding * 2
        : contentRef.value.scrollHeight + collapse2Ref.value.scrollHeight + padding * 2,
    })
  },
  animateSet: async () => {
    await Promise.all([
      titleRef.value.prepare(),
      subtitleRef.value.prepare(),
      gsap.set(wrapperRef.value, {
        clipPath: `inset(33% round ${pxToVw(32)})`,
        opacity: 0,
      }),
      gsap.set(imageRef.value, {
        opacity: 0,
        scale: 1.2,
      }),
      gsap.set(skeletonRef.value, {
        height: (_, el) => el.scrollHeight,
        clipPath: `inset(0% 100% 0% 0% round ${pxToVw(32)})`,
      }),
    ])
  },
  animateIn: async (delay = 0) => {
    await Promise.all([
      gsap.to(wrapperRef.value, {
        clipPath: `inset(-1px round ${pxToVw(32)})`,
        opacity: 1,
        duration: 1.2,
        ease: 'power2.inOut',
        delay,
      }),
      gsap.to(skeletonRef.value, {
        clipPath: `inset(0% 0% 0% 0% round ${pxToVw(32)})`,
        duration: 1.2,
        ease: 'power2.inOut',
        delay: delay + 0.6,
        stagger: 0.1,
      }),
    ])
  },
  animateOut: async () => {
    await gsap.to(wrapperRef.value, {
      clipPath: `inset(33% round ${pxToVw(32)})`,
      opacity: 0,
      duration: 0.8,
      ease: 'power2.inOut',
    })
  },
  el: () => wrapperRef.value,
})
</script>

<style lang="scss" scoped>
.wrapper {
  width: 100%;
  gap: px-to-vw(24);
  padding: px-to-vw(54);
  border-radius: px-to-vw(32);
  background: rgba(230, 244, 234, 0.1);
  @include gradient-border((45deg, rgba(78, 78, 78, 0.2), rgba(225, 225, 225, 0.2)), 2px);
  clip-path: inset(0% 0% round px-to-vw(32));

  &::before {
    border-radius: px-to-vw(32);
  }

  .content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: px-to-vw(32);
  }

  .title {
    position: relative;
    flex: 1 1;

    & > * + * {
      margin-top: px-to-vw(16);
    }

    .title-with-icon {
      color: $brandGreen;

      :deep(svg) {
        width: px-to-vw(16);
        height: px-to-vw(16);
      }
    }
  }

  .image {
    position: relative;
    flex: 0.95;
    overflow: hidden;
    height: 100%;
    border-radius: px-to-vw(32);
    display: flex;
    align-items: center;
    justify-content: center;
  }

  .image-container {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  img {
    width: 100%;
    aspect-ratio: 1.05;
    object-fit: cover;
    border-radius: px-to-vw(32);
  }

  .collapse {
    width: 100%;
    height: 0;
    overflow: hidden;
    text-align: center;
  }

  .divider {
    width: calc(100% + px-to-vw(48));
    height: 1px;
    background: rgba(255, 255, 255, 0.2);
    margin: 0 px-to-vw(-24);
  }

  .collapse-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: px-to-vw(54) 0 0;
    gap: px-to-vw(54);

    .text-body-24 {
      text-align: left;
      text-wrap: auto;
    }
  }

  .group {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: px-to-vw(16);
  }

  .text-color-gray {
    color: #999999;
  }

  .kayak {
    position: absolute;
    z-index: 2;
    bottom: px-to-vw(-25);
    width: px-to-vw(287);
    height: auto;
    left: -10%;
  }

  .progress-group {
    width: 100%;
    display: flex;
    justify-content: space-between;
    position: relative;
    margin-bottom: px-to-vw(26);

    .progress-bar {
      top: calc(100% + px-to-vw(16));
      position: absolute;
      width: 100%;
      height: px-to-vw(8);
      background: rgba(255, 255, 255, 0.2);
      border-radius: px-to-vw(10);
      overflow: hidden;

      .progress-bar-fill {
        height: 100%;
        // background: linear-gradient(77.26deg, #e6f4ea -40.68%, $brandGreen 106.27%);
        background: #fff;
        border-radius: px-to-vw(10);
        width: 15%;
        transform-origin: left;
      }
    }
  }

  .title-container,
  .subtitle-container {
    position: relative;
    width: 100%;
  }
  .title-container {
    max-height: 2em;
    height: 2em;
  }
  .subtitle-container {
    width: max-content;
  }

  .skeleton {
    position: absolute;
    width: 100%;
    height: 100%;
    background: linear-gradient(58.9deg, rgba(230, 244, 234, 0.6) 7%, rgba(52, 168, 83, 0.6) 120%);
    z-index: 10;
    clip-path: inset(0% 0% 0% 100% round px-to-vw(32));
  }

  .pin {
    width: px-to-vw(27);
    height: auto;
  }
}
</style>
