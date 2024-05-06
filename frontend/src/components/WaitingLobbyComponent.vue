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
import Cookies from 'js-cookie';

export default {
  name: 'WaitingLobbyComponent',
  setup() {
    


  },
  mounted() {
    const gameStore = useGameStore();
    let gameOptions = gameStore.gameOptions;
    if (gameOptions == null) {
      if (Cookies.get('gameOptions') != null) {
        gameOptions = JSON.parse(Cookies.get('gameOptions'));
        gameStore.gameOptions = gameOptions;
        console.log("substituted gameOptions from cookies")
        // set lobby id to h2
        let h2 = document.querySelector('h2');
        h2.innerHTML = 'Lobby-ID: ' + gameOptions.lobby_id;
      } else {
        this.$router.push('/');
      }
    }
    console.log(JSON.stringify(gameOptions));

    let playerList = document.getElementById('playerList');
    let player1 = document.createElement('div');
    player1.innerHTML = 'Spieler 1: ' + gameOptions.owner_name;
    playerList.appendChild(player1);
    player1.classList.add('player');
    // add player status and append it to the player div
    let player1Status = document.createElement('div');
    player1Status.innerHTML = 'Status: Bereit';
    player1Status.classList.add('player-status');
    player1.appendChild(player1Status);
  }
};

</script>