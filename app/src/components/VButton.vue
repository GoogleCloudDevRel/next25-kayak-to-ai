<template>
  <button
    ref="el"
    :class="{ VButton: true, [variant]: true, [size]: true }"
    @click="handleClick"
    @mouseenter="() => handleHover(true)"
    @mouseleave="() => handleHover(false)"
  >
    <div
      ref="bg"
      class="bg"
      :class="[backgroundColor ? `background-${backgroundColor}` : '']"
    />
    <div class="content">
      <IconBase v-if="iconLeft || size === 'icon'" :variant="icon" />
      <VText
        v-if="size !== 'icon'"
        :text="text"
        :variant="textVariant || 'medium-18'"
      />
      <IconBase v-if="iconRight" :variant="icon" />
    </div>
  </button>
</template>

<script setup>
import { gsap } from "@/utils/gsap";
import IconBase from "./IconBase.vue";
import VText from "./VText.vue";

import { shallowRef } from "vue";

const el = shallowRef(null);
const bg = shallowRef(null);

const props = defineProps({
  text: {
    type: String,
    required: true,
  },
  variant: {
    type: String,
    // 'primary' | 'outline'
    default: "primary",
  },
  textVariant: {
    type: String,
  },
  size: {
    type: String,
    // 'default' | 'icon' | 'large'
    default: "default",
  },
  onClick: {
    type: Function,
    default: () => {},
  },
  onHover: {
    type: Function,
    default: () => {},
  },
  iconLeft: {
    type: Boolean,
    default: false,
  },
  iconRight: {
    type: Boolean,
    default: false,
  },
  icon: {
    type: String,
    default: "gemini",
  },
  backgroundColor: {
    type: String,
    default: "primary",
  },
});

const handleClick = (e) => {
  e.preventDefault();
  // Add any additional click handling logic here
  props.onClick();
};

const handleHover = (isHovering) => {
  // Add any additional hover handling logic here
  props.onHover(isHovering);
};

defineExpose({
  animateSet: async () => {
    gsap.set(el.value, {
      clipPath: "inset(50% round 999px)",
    });
  },
  animateIn: async (delay = 0) => {
    await gsap.to(el.value, {
      clipPath: "inset(0% round 999px)",
      duration: 0.6,
      ease: "power2.out",
      delay,
    });
  },
  animateOut: async () => {
    await gsap.to(el.value, {
      clipPath: "inset(50% round 999px)",
      duration: 0.6,
      ease: "power2.out",
    });
  },
});
</script>

<style lang="scss" scoped>
.VButton {
  position: relative;
  appearance: none;
  border: none;
  background: none;
  font: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
  border-radius: 999px;
  cursor: pointer;

  &.default {
    height: 54px;
    padding: 0 24px;
  }

  &.icon {
    height: 54px;
    width: 54px;
    padding: 0;
  }

  &.large {
    height: 65px;
    padding: 0 24px;
    min-width: px-to-vw(264);
  }

  .content {
    display: flex;
    gap: 8px;
    align-items: center;
  }
}

.content {
  z-index: 3;
}

.bg {
  position: absolute;
  width: 100%;
  height: 100%;
  border-radius: 999px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Button */
.shopping,
.kayak,
.drive {
  .VButton.outline {
    .bg::before {
      content: "";
      position: absolute;
      width: calc(100% - 4px);
      height: calc(100% - 4px);
      border-radius: 999px;
      mask:
        linear-gradient(#000 0 0) content-box,
        linear-gradient(#000 0 0);
      mask-composite: exclude;
      padding: 3px;
      z-index: 1;
    }

    .bg::after {
      content: "";
      position: absolute;
      width: calc(100% - 4px);
      aspect-ratio: 1;
      border-radius: 50%;
      padding: 3px;
      z-index: 2;
      transform: scale(0);
      transition: transform 0.3s ease-in-out;
    }
  }

  .VButton.primary {
    .bg::after {
      content: "";
      position: absolute;
      width: 100%;
      aspect-ratio: 1;
      border-radius: 50%;
      transform: scale(0);
    }
  }
}

.shopping {
  .VButton.outline {
    color: #fff;
    transition: color 0.01s ease-in;

    .bg::before {
      background: linear-gradient(
        70.04deg,
        rgba(255, 255, 255, 0.5) -100.01%,
        rgba(66, 133, 244, 0.5) 182.1%
      );
    }

    .bg::after {
      background: linear-gradient(
        70.04deg,
        #ffffff -100.01%,
        $brandBlue 182.1%
      );
    }

    &:hover {
      .bg::after {
        transform: scale(1);
        transition: transform 0.3s ease-in-out;
      }

      color: #2a2a2a;
      transition: color 0.01s ease-out;
    }
  }

  .VButton.primary {
    color: #2a2a2a;

    .bg {
      background: linear-gradient(
        70.04deg,
        #ffffff -100.01%,
        $brandBlue 182.1%
      );

      &::after {
        background: $brandBlue;
        transition: transform 0.3s ease-in-out;
      }
    }

    &:hover {
      .bg::after {
        transform: scale(1);
      }
    }
  }
}

.kayak {
  .VButton.outline {
    color: #fff;
    transition: color 0.01s ease-in;

    .bg::before {
      background: linear-gradient(
        84.76deg,
        rgba(230, 244, 234, 0.5) -28.87%,
        rgba(52, 168, 83, 0.5) 163.54%
      );
    }

    .bg::after {
      background: linear-gradient(
        77.26deg,
        #e6f4ea -40.68%,
        $brandGreen 106.27%
      );
    }

    &:hover {
      .bg::after {
        transform: scale(1);
        transition: transform 0.3s ease-in-out;
      }

      color: #2a2a2a;
      transition: color 0.01s ease-out;
    }
  }

  .VButton.primary {
    color: #2a2a2a;

    .bg {
      background: linear-gradient(
        77.26deg,
        #e6f4ea -40.68%,
        $brandGreen 106.27%
      );

      &::after {
        background: $brandGreen;
        transition: transform 0.3s ease-in-out;
      }
    }

    &:hover {
      .bg::after {
        transform: scale(1);
      }
    }
  }
}

.drive {
  .VButton.outline {
    color: #fff;
    transition: color 0.01s ease-in;

    .bg::before {
      border: 1.5px solid;
      background: linear-gradient(
        87.08deg,
        rgba(255, 255, 255, 0.6) -9.68%,
        rgba(243, 178, 1, 0.6) 17.02%,
        rgba(227, 123, 36, 0.2) 101.2%
      );
    }

    .bg::after {
      background: linear-gradient(270deg, #e37b24 27.65%, #f3b201 118.57%);
    }

    &:hover {
      .bg::after {
        transform: scale(1);
        transition: transform 0.3s ease-in-out;
      }

      color: #2a2a2a;
      transition: color 0.01s ease-out;
    }
  }

  .VButton.primary {
    color: #2a2a2a;

    .bg {
      background: linear-gradient(270deg, #e37b24 27.65%, #f3b201 118.57%);

      &::after {
        background: $brandYellow;
        transition: transform 0.3s ease-in-out;
      }
    }

    &:hover {
      .bg::after {
        transform: scale(1);
      }
    }
  }
}

.skeeball {
  .VButton.primary {
    color: #fff;
    box-shadow:
      0px 0px 0px 1px rgba(0, 0, 0, 1),
      2px 4px 0px 0px rgba(0, 0, 0, 1);

    .bg {
      background: $brandGreen;
      &.background-yellow {
        background: $brandYellow;
      }
    }

    &:hover {
      box-shadow: 0px 0px 0px 1px rgba(0, 0, 0, 1);
      transform: translateX(1px) translateY(3px);
    }
  }
}
</style>
