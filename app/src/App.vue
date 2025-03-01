<template>
  <main>
    <template v-if="!isTVScreen">
      <div class="main-content">
        <ChatForm class="chat-form-container" />
        <SystemExecution class="system-execution-container" />
      </div>
    </template>

    <template v-else>
      <TVView />
      <ChatForm />
    </template>
  </main>
</template>

<script setup>
import { ref } from 'vue';
import { getQueryParam } from './Utils.js';
import TVView from './views/TVView.vue';
import ChromebookView from './views/ChromebookView.vue';
import ChatForm from './components/ChatForm.vue'; // Import the ChatForm component
import SystemExecution from './components/SystemExecution.vue'

const isTVScreen = ref(false);
isTVScreen.value = getQueryParam('tv');
</script>

<style lang="scss" scoped>
main {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: #2e2e2e;
}

.main-content {
  display: flex;
  width: 100%;
  height: 100%;
  justify-content: center;
  align-items: center;
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
}
.chat-form-container {
  width: 50%;
  height: 80%;
}

.system-execution-container {
  width: 50%;
  height: 80%;
}
</style>
