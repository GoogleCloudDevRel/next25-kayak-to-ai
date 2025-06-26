<template>
  <div
    class="qr-code"
    ref="qrCodeRef"
  >
    <img
      :src="src"
      alt="QR Code"
    />
    <VText
      text="Learn more"
      variant="tv-bold-40"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { generateQR } from '@/utils/qr'
import VText from './VText.vue'
const qrCodeRef = ref(null)

const props = defineProps({
  value: {
    type: String,
    required: true,
  },
})

const src = ref(null)

onMounted(async () => {
  src.value = await generateQR(props.value)
})
</script>

<style lang="scss">
.qr-code {
  position: absolute;
  bottom: px-to-vw(144, 4k);
  right: px-to-vw(144, 4k);
  background: linear-gradient(70.04deg, #e6f4ea -100.01%, #34a853 182.1%);
  border-radius: px-to-vw(32, 4k);
  width: px-to-vw(350, 4k);
  padding: px-to-vw(48, 4k);
  padding-bottom: px-to-vw(32, 4k);
  gap: px-to-vw(32, 4k);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  color: #0e0d0d;

  * {
    white-space: nowrap;
  }

  img {
    width: 100%;
  }
}
</style>
