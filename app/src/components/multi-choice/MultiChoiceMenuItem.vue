<template>
  <div
    class="multiChoiceMenuItemWrapper"
    :class="{ square }"
  >
    <div
      class="multiChoiceMenuItem"
      :class="{ selected }"
      @click="handleClick"
      ref="innerItem"
    >
      <div class="multiChoiceMenuItem__icon">
        <IconBase
          class="multiChoiceMenuItem__icon__icon"
          :variant="icon"
        />
      </div>
      <div class="multiChoiceMenuItem__label">
        <VText
          ref="vtext"
          :text="label"
          :gradient="selected"
          variant="medium-28"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import IconBase from '@/components/IconBase.vue'
import VText from '@/components/VText.vue'
import { pxToVw } from '@/utils/px'
import gsap from 'gsap'
import { ref, onMounted } from 'vue'

const innerItem = ref(null)
const vtext = ref(null)

const props = defineProps({
  value: {
    type: String,
    default: '',
    required: true,
  },
  square: {
    type: Boolean,
    default: false,
  },
  label: {
    type: String,
    default: '',
    required: true,
  },
  icon: {
    type: String,
    default: '',
    required: false,
  },
  solidColor: {
    type: String,
    required: false,
    validator: (value) => ['red', 'greeb', 'yellow', 'blue'].includes(value),
  },
  selected: {
    type: Boolean,
    default: false,
  },
})

onMounted(() => {
  vtext.value.prepare()
})

const animateSet = () => {
  gsap.set(innerItem.value, {
    clipPath: `inset(33% round ${pxToVw(24)})`,
    opacity: 0,
  })
  vtext.value.animateSet()
}

const animateIn = (delay = 0) => {
  gsap.to(innerItem.value, {
    clipPath: `inset(-1px round ${pxToVw(24)})`,
    opacity: 1,
    duration: 0.8,
    ease: 'power2.out',
    delay,
  })
  vtext.value.animateIn(delay - 0.4)
}

const animateOut = (delay) => {
  gsap.to(innerItem.value, {
    clipPath: `inset(33% round ${pxToVw(24)})`,
    opacity: 0,
    duration: 0.8,
    ease: 'power2.inOut',
    delay,
  })
}

const emit = defineEmits(['select'])

const handleClick = () => {
  emit('select', { value: props.value, label: props.label })
}

defineExpose({
  animateIn,
  animateSet,
  animateOut,
})
</script>

<style lang="scss" scoped>
.shopping {
  .multiChoiceMenuItemWrapper {
    .multiChoiceMenuItem {
      background:
        linear-gradient(61.53deg, rgba(72, 87, 113, 0.1) -39.88%, rgba(137, 166, 215, 0.1) 121.44%),
        linear-gradient(0deg, rgba(37, 49, 75, 0.15), rgba(37, 49, 75, 0.15));

      &__label {
        color: #fff;
      }

      &__icon {
        color: linear-gradient(207.21deg, #4285f4 -27.19%, #d9e7ff 175.32%);
        justify-content: flex-start;
        align-items: flex-start;
      }

      &.selected {
        background: linear-gradient(
          50.24deg,
          rgba(66, 133, 244, 0.1) -4.95%,
          rgba(217, 231, 255, 0.2) 117.88%
        );
        @include gradient-border((45deg, #ffffff, #4285f4), 1px);
      }
    }
  }
}

.kayak {
  .multiChoiceMenuItemWrapper {
    .multiChoiceMenuItem {
      background:
        linear-gradient(
          215.08deg,
          rgba(48, 50, 57, 0.32) 23.97%,
          rgba(75, 137, 93, 0.1664) 120.38%
        ),
        linear-gradient(0deg, rgba(0, 0, 0, 0.3), rgba(0, 0, 0, 0.3));

      border-image-source: linear-gradient(222.58deg, rgba(78, 78, 78, 0.2) 7.2%, 100.18%);

      @include gradient-border((45deg, rgba(78, 78, 78, 0.2), rgba(225, 225, 225, 0.2)), 1px);

      &:hover,
      &.selected {
        background:
          linear-gradient(
            215.08deg,
            rgba(48, 50, 57, 0.32) 23.97%,
            rgba(75, 137, 93, 0.1664) 120.38%
          ),
          linear-gradient(0deg, rgba(0, 0, 0, 0), rgba(0, 0, 0, 0));
        @include gradient-border((45deg, #e6f4ea, #34a853), 1px);
      }

      &__icon {
        color: #1c1b1f;
        background: linear-gradient(82.43deg, #e6f4ea -69.88%, #34a853 229.35%);
      }

      &__label {
        color: #cecece;
      }
    }
  }
}

.multiChoiceMenuItemWrapper {
  overflow: hidden;
  &.square {
    padding: 2px;
    aspect-ratio: 1;
    width: 100%;
    height: auto;
  }
}

.multiChoiceMenuItem {
  text-align: left;
  padding: px-to-vw(32);
  border-radius: px-to-vw(24);
  border-width: 1px;
  justify-content: space-between;
  flex-direction: column;
  display: flex;
  height: 100%;
  box-sizing: border-box;
  cursor: pointer;
  transition: background-color 0.3s linear;

  &::before {
    border-radius: px-to-vw(24);
    transition: all 0.9s linear;
  }

  // base styles

  &__icon {
    width: px-to-vw(48);
    height: px-to-vw(48);
    border-radius: 100%;
    display: flex;
    align-items: center;
    justify-content: center;

    &__icon {
      width: px-to-vw(29) !important;
      height: px-to-vw(29) !important;
      svg {
        width: 100% !important;
        height: 100% !important;
      }
    }
  }

  &__label {
    color: #bebebe;
  }
}
</style>
