<template>
    <div class="container my-auto" id="app">
        <div class="heading center mb-4">
            <h1>Wartelobby</h1>
            <h2>Lobby-ID: Laden...</h2>
        </div>
        <div id="playerList"></div>
    </div>
</template>

<script>
import { useGameStore } from "@/store.js";

export default {
  name: 'WaitingLobbyComponent',
  setup() {
    const gameStore = useGameStore();
    console.log(JSON.stringify(gameStore.gameOptions));

  },
};

</script>