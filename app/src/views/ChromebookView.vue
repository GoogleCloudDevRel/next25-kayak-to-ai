<template>

  <InputMicrophone :cta="'Start Recording'" :ctaStopped="'Stop Recording'" :language="'en-US'"
    @input-microphone-clicked="handleInputMicrophoneClick" @input-microphone-result="handleInputMicrophoneResult"
    @input-microphone-end="handleInputMicrophoneEnd" @input-microphone-start="handleInputMicrophoneStart" />

  <div class="result">
    <span contenteditable="true" id="text-input-editable" class="transition-text">{{ text }}</span>
  </div>

</template>

<script setup>
import { ref } from 'vue';
import InputMicrophone from "../components/InputMicrophone.vue"

const text = ref('');
const handleInputMicrophoneClick = () => {
  text.value = '';
}
const handleInputMicrophoneEnd = () => {
  text.value = '';
}
const handleInputMicrophoneStart = () => {
  text.value = '';
}
const handleInputMicrophoneResult = ({ speechText }) => {
  text.value = speechText;
}

</script>

<style scoped>
.input-microphone {
  width: 100%;
}

.result {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

span.transition-text {
  display: inline-block;
  width: 100%;
  height: 100%;
  max-width: 50%;
  margin-top: 50px;
  border: none;
  background-color: #f0f0f0;
  border-radius: 20px;
  padding: 20px 80px;
  color: #000;
  font-size: 32px;
  font-family: "Open Sans", serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
  font-variation-settings:
    "wdth" 100;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 1);
}
</style>
