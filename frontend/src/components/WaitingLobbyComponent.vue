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
    let gameOptions = gameStore.gameOptions;
    let gameSettings = gameStore.gameSettings;
    let ownerName = gameOptions.owner.name;
    let round_timer = gameSettings.round_timer;
    let lives_per_player = gameSettings.lives_per_player;

  },
};

</script>