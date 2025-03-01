<template>
  <div class="system-execution-container">
    <div class="system-logs">
      <div v-for="(log, index) in logs" :key="index" class="log-entry" :class="log.type">
        {{ log.message }}
        <span class="timestamp">{{ log.timestamp }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const logs = ref([]);

const addLog = (message, type) => {
  const now = new Date();
  const timestamp = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}:${now.getSeconds().toString().padStart(2, '0')}`;
  logs.value.push({ message, type, timestamp });
};

onMounted(() => {
  // Simulate system logs
  addLog('System started.', 'info');
  setTimeout(() => {
    addLog('Loading modules...', 'info');
    addLog('Module A loaded.', 'success');
    addLog('Module B loaded.', 'success');
    addLog('Warning: Low memory detected.', 'warning');
    addLog('Error: Failed to connect to database.', 'error');
    addLog('System ready.', 'info');
  }, 500);
});



</script>

<style scoped>
.system-execution-container {
  width: 100%;
  height: 100%;
  background-color: #222;
  color: #eee;
  font-family: monospace;
  padding: 20px;
  box-sizing: border-box;
  overflow: auto;
}

.system-logs {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.log-entry {
  padding: 5px 10px;
  border-radius: 4px;
  font-size: 14px;
  white-space: pre-wrap;
}
.timestamp {
  font-size: 12px;
  color: #999;
  margin-left: 10px;
}

.info {
  color: #eee;
}

.success {
  color: #4caf50;
}

.warning {
  color: #ffc107;
}

.error {
  color: #f443
}
</style>