<template>
  <div class="wrapper" ref="wrapperRef">
    <div class="content" ref="contentRef">
      <div class="title">
        <VText ref="titleRef" text="Name of the Location" variant="medium-80" />
      </div>
      <div class="image">
        <img src="/images/kayak/image-grid-1.jpg" alt="Kayak" />
      </div>
    </div>
    <div class="collapse" ref="collapseRef">
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
            :onClick="() => kayakStore.setIsMoving(true)"
          />
        </div>
      </div>
    </div>
    <div class="collapse" ref="collapse2Ref">
      <div class="collapse-content text-color-gray">
        <div class="divider"></div>
        <VText
          text="Watch the map to see AI move the Kayak"
          variant="medium-24"
        />
        <div class="progress-group">
          <IconPin class="pin" />
          <IconKayak class="kayak" />
          <div class="progress-bar">
            <div class="progress-bar-fill" />
          </div>
          <IconPin class="pin pin-right" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import VText from "@/components/VText.vue";
import { gsap } from "@/utils/gsap";
import { ref, watch } from "vue";
import VButton from "./VButton.vue";
import IconPin from "@/components/icons/IconPin.vue";
import { useKayakStore } from "@/store";
import IconKayak from "@/components/icons/IconKayak.vue";
import { pxToVw } from "@/utils/px";
import { useRouteManager } from "@/router/useRouteManager";
const titleRef = ref(null);
const collapseRef = ref(null);
const collapse2Ref = ref(null);
const contentRef = ref(null);
const wrapperRef = ref(null);

const kayakStore = useKayakStore();

const { navigateTo } = useRouteManager();

watch(
  () => kayakStore.isMoving,
  (isMoving) => {
    if (isMoving) {
      gsap.to(collapseRef.value, {
        height: 0,
        duration: 1,
        ease: "power2.inOut",
      });
      gsap.to(collapse2Ref.value, {
        height: collapse2Ref.value.scrollHeight,
        duration: 1,
        ease: "power2.inOut",
        onComplete: () => {
          gsap.set(collapse2Ref.value, {
            height: "auto",
          });
        },
      });
    }
  }
);

defineExpose({
  animateSet: async () => {
    await titleRef.value.prepare();
    gsap.set(wrapperRef.value, {
      clipPath: `inset(50% round ${pxToVw(32)})`,
    });
  },
  animateIn: async (delay = 0) => {
    await Promise.all([
      titleRef.value.animateIn(delay),
      gsap.to(wrapperRef.value, {
        clipPath: `inset(0% round ${pxToVw(32)})`,
        duration: 1,
        ease: "power2.inOut",
        delay,
      }),
    ]);
    await new Promise((resolve) => setTimeout(resolve, 1000));
    gsap.to(contentRef.value, {
      height: contentRef.value.scrollHeight - collapseRef.value.scrollHeight,
      duration: 1,
      ease: "power2.inOut",
    });
    gsap.to(collapseRef.value, {
      height: collapseRef.value.scrollHeight,
      duration: 1,
      ease: "power2.inOut",
      onComplete: () => {
        gsap.set(collapseRef.value, {
          height: "auto",
        });
      },
    });
  },
  animateOut: async () => {
    gsap.to(wrapperRef.value, {
      clipPath: `inset(50% round ${pxToVw(32)})`,
      duration: 1,
      ease: "power2.inOut",
    });
  },
});
</script>

<style lang="scss" scoped>
.wrapper {
  width: 100%;
  gap: px-to-vw(24);
  padding: px-to-vw(54);
  border-radius: px-to-vw(32);
  background: rgba(230, 244, 234, 0.1);
  @include gradient-border(
    (45deg, rgba(78, 78, 78, 0.2), rgba(225, 225, 225, 0.2)),
    2px
  );

  &::before {
    border-radius: px-to-vw(32);
  }

  .content {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: px-to-vw(54);
  }

  .title {
    flex: 1 1;
  }

  .image {
    flex: 0.95;
    overflow: hidden;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: px-to-vw(32);
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
    bottom: px-to-vw(-22.5);
    width: px-to-vw(66);
    height: auto;
    left: 8%;
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
      height: px-to-vw(10);
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
}
</style>
