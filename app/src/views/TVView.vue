<template>
  <div class="tv-screen">
    <h1>TV Screen</h1>
    <LeaderboardView :leaderboard="leaderboardData" />
  </div>

</template>

<script setup>
import { onMounted, ref } from 'vue';
import { getLeaderBoard } from '../API.js';
import LeaderboardView from '../components/LeaderboardView.vue';

const leaderboardData = ref([]);

onMounted(async () => {
  leaderboardData.value = await getLeaderBoard();
});

</script>

<style scoped>
.tv-screen {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: space-around;
  width: 100%;
  height: 100;
  font-size: 32px;
  font-family: "Open Sans", serif;
  font-optical-sizing: auto;
  font-weight: 400;
  font-style: normal;
  font-variation-settings:
    "wdth" 100;
}
</style>
