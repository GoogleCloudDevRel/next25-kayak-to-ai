<template>
    <div class="leaderboard">
        <div class="leaderboard-item" v-for="item in leaderboard" :key="item.id">
            <div class="leaderboard-item-rank">{{ item.rank }}</div>
            <div class="leaderboard-item-name">{{ item.name }}</div>
            <div class="leaderboard-item-score">{{ item.score }}</div>
        </div>
    </div>
</template>

<script setup>
defineProps({
    leaderboard: Array
});
</script>

<style scoped>
.leaderboard {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 30%;
    margin-bottom: -10px;

    .leaderboard-item {
        width: 100%;
        gap: 10px;
        margin-bottom: 10px;
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        background-color: #f0f0f0;
        border-radius: 10px;
        padding: 10px;
        color: #000;
    }
}
</style>