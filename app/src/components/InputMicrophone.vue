<template>
  <div class="input-microphone">
    <button @click="handleClick" id="record-button" class="input-microphone-button">
      {{ currentCta }}
    </button>
  </div>
</template>

<script setup>
const emit = defineEmits(['input-microphone-clicked', 'input-microphone-result', 'input-microphone-end', 'input-microphone-start'])

const props = defineProps({
  cta: {
    type: String,
    default: ''
  },
  ctaStopped: {
    type: String,
    default: ''
  },
  language: {
    type: String,
    default: 'en-US'
  }
})

import { ref, onMounted } from 'vue'

const currentCta = ref('')
const speechText = ref('')
const recognition = ref(null)
const recording = ref(false)

const initRecorder = () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
  if (!SpeechRecognition) {
    console.error('SpeechRecognition not supported')
    return
  }
  recognition.value = new SpeechRecognition()
  recognition.value.lang = props.language
  recognition.value.interimResults = true
  recognition.value.continuous = true
  initRecognitionEvents()
}

const initRecognitionEvents = () => {
  recognition.value.onstart = () => {
    speechText.value = ''
    emit('input-microphone-start')
  }

  recognition.value.onend = () => {
    speechText.value = ''
    emit('input-microphone-end')
  }

  recognition.value.onresult = (event) => {
    let text = ''
    for (let i = event.resultIndex; i < event.results.length; ++i) {
      if (event.results[i].isFinal) {
        text = event.results[i][0].transcript
      } else {
        text += event.results[i][0].transcript
      }
    }
    handleOnResult(text)
  }
}

const handleOnResult = (text) => {
  speechText.value = text
  emit('input-microphone-result', { speechText: text })
}

const handleClick = () => {
  recording.value = !recording.value
  //emit('input-microphone-clicked', { recordingState: recording.value })
  currentCta.value = recording.value ? props.ctaStopped : props.cta
  recording.value ? recognition.value.start() : recognition.value.stop()
}

// Initialize on component creation
onMounted(() => {
  currentCta.value = props.cta
  initRecorder()
})
</script>

<style lang="scss">
.input-microphone {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  .input-microphone-button {
    font-family: "Open Sans", serif;
    cursor: pointer;
    background-color: #007bff;
    color: white;
    border: none;
    border-radius: 20px;
    font-size: 32px;
    @include fluid(font-size, (tab: 22px, mob: 16px));
    @include fluid(padding, (tab: 10px 20px, mob: 15px 10px));
    @include fluid(border-radius, (tab: 20px, mob: 10px));
    transition: transform 0.3s ease;
    box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.1);

    &:hover {
      transform: scale(1.05);
      transition: transform 0.3s ease;
    }
  }
}
</style>
