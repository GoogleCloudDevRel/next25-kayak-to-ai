<template>
  <div class="chat-container">
    <div class="chat-history">
      <div v-for="chat in chatHistory" :key="chat.id" class="chat-bubble" :class="{ 'user-message': chat.type === 'user', 'bot-message': chat.type === 'bot' }">
        {{ chat.message }}
      </div>
      <div v-if="isLoading" class="chat-bubble bot-message">
        <div class="loading-dots">
          <div class="dot"></div>
          <div class="dot"></div>
          <div class="dot"></div>
        </div>
      </div>
    </div>
    <form class="chat-form" @submit.prevent="handleSubmit">
      <input
        type="text"
        class="chat-input"
        v-model="message"
        placeholder="Enter your message or start recording"
        @input="handleInput"
      />
      <InputMicrophone :cta="'Start Recording'" :ctaStopped="'Stop Recording'" :language="'en-US'"
        @input-microphone-clicked="handleInputMicrophoneClick" @input-microphone-result="handleInputMicrophoneResult"
        @input-microphone-end="handleInputMicrophoneEnd" @input-microphone-start="handleInputMicrophoneStart" />
      
      <button class="action-button" type="button" @click="handleAction">
        <i v-if="hasMessage" class="fas fa-paper-plane"></i>
        <i v-else class="fas fa-microphone"></i>
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { onMounted } from 'vue';

const chatHistory = ref([]);
const isLoading = ref(false);

onMounted(async () => {
  isLoading.value = true;
  // Simulate API call delay
  setTimeout(() => {
    chatHistory.value = [{ id: 1, type: 'bot', message: 'Hello! How can I help you today?' }, { id: 2, type: 'user', message: 'Hi there!' }];
    isLoading.value = false;
  }, 1000);
});

const message = ref('');
const hasMessage = computed(() => message.value.trim().length > 0);

const handleInput = () => {
  // Input changed, no additional logic needed here
};

const handleAction = () => {
  if (hasMessage.value) {
    sendMessage();
  } else {
    startRecording();
  }
};

const handleSubmit = () => {
  if (hasMessage.value) {
    sendMessage();
  } else {
      startRecording();
  }
};

const sendMessage = () => {
  if (message.value.trim() !== '') {
    chatHistory.value.push({ id: Date.now(), type: 'user', message: message.value });
    message.value = '';
    isLoading.value = true;
    // Simulate API call delay
    setTimeout(() => {
      chatHistory.value.push({ id: Date.now() + 1, type: 'bot', message: 'You said: ' + message.value });
      isLoading.value = false;
    }, 1000);
  }
};




const startRecording = () => {
  console.log('Starting recording...');
  // Add your recording logic here
};


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

<style lang="scss" scoped>
@use '@/styles/global.scss';
.chat-container {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 10px;
  border: 1px solid #ccc;
  width: 80%;
  max-width: 800px;
  margin: auto;
  background-color: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.chat-history {
  width: 100%;
  height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #eee;
  border-radius: 5px;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.chat-bubble {
  padding: 10px 15px;
  border-radius: 10px;
  max-width: 70%;
  word-wrap: break-word;
}

.user-message {
  background-color: #e0f7fa;
  align-self: flex-end;
}

.bot-message {
  background-color: #f0f0f0;
  align-self: flex-start;
}

.loading-dots {
  display: flex;
}

.chat-form {
  display: flex;
  flex-grow: 1;
  width: 100%;
}

.chat-input {
  flex-grow: 1;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-right: 5px;
  width: 100%;
}

.action-button {
  background-color: #4caf50;
  border: none;
  color: white;
  padding: 8px 12px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  border-radius: 4px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-button i {
  font-size: 20px;
}

.action-button i.fa-paper-plane {
  transform: rotate(45deg);
}

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

.loading-dots {
  display: flex;
  align-items: center;
  justify-content: center;
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: #ccc;
  margin: 0 4px;
  animation: pulse 1s infinite;
}

.dot:nth-child(2) {
  animation-delay: 0.2s;
}

.dot:nth-child(3) {
  animation-delay: 0.4s;
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}
</style>
