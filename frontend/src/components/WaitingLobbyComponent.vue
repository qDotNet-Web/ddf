<style scoped>
h2 i{
  transition: 0.5s;
}
h2 i:hover {
  cursor: pointer;
  color: rgb(0, 68, 255);
}
#editAvatar:hover {
    padding: .5em;
    color: #57f1f7;
}
#editAvatar {
    position: absolute;
    padding: .4em;
    background-color: #393939;
    border-radius: 50%;
    right: 2.5em;
    top: 5.3em;
    transition: 0.3s;
}
</style>

<template>
  <div class="container my-auto dff-padding-top-3" id="app">
    <div class="heading center mb-4 is-header-waitingLobby">
      <h1 style="margin-bottom: 0;">Wartelobby</h1>
      <hr style="width: 50%; color: var(--gray-400)">
      <h2>ID: {{ lobby_code }} <i @click="copyLobbyCode" class="pi pi-copy" style="font-size: 30px;"></i></h2>

    </div>
    <!--<div id="playerList">
      <div v-for="(player, index) in players" :key="index" class="player fr-animate-2 fr-move-up fr-delay-3">
        <img :src="logo" class="avatar">
        <span class="player-name">
          <span v-if="(player.getId() == lobby_owner)" v-tooltip.top="'Spielbesitzer'"><i class="pi pi-crown"></i></span>
          {{ player.getName() }}
          <span v-if="player.getIsSelf()">(Du)</span>
        </span>
        <div class="player-status">Bereit</div>
      </div>
    </div> -->
    <Dialog v-model:visible="showDialog" modal header="Avatar auswählen" :style="{width: '35rem'}">
    <div class="select-avatar-container">
      <img v-for="(avatar, index) in avatars" :key="index" :src="avatar.src" class="avatar" @click="selectAvatar(index)">
    </div>

  </Dialog>

    <div id="playerList" class="mb-5">
        <Card v-for="(player, index) in players" :key="index" stlye="overflow: hidden" class="fr-animate-2 fr-move-up fr-delay-3">
          <template #header>
            <div class="avatar-container" @mouseover="showEditIcon = player.getIsSelf()" @mouseleave="showEditIcon = false">
              <img :src="logo" :class="{'blur': showEditIcon}" class="avatar" @click="showDialog = player.getIsSelf()">
              <i class="pi pi-user-edit editAvatar" v-if="showEditIcon" @click="showDialog = true"></i>
            </div>
          </template>
          <template #title>
            <hr>
            <span v-if="player.getId() == lobby_owner" v-tooltip.top="'Spielbesitzer'"><i class="pi pi-crown" style="font-size: 30px;"></i></span>
          </template>
          <template #subtitle>
            {{ player.getName() }}
                <span v-if="player.getIsSelf()"> (Du)</span>
          </template>
          <template #content>
            <span>{{ player.getLives() }} <i style="font-size: 26px;" class="pi pi-heart-fill"></i></span>
            <div class="player-status" style="font-size: 18px;">Bereit</div>
          </template>
        </Card>
        
    </div>
    <div class="center">
      <Button class="btn btn-main-new" @click="startGame">Spiel starten</Button>
      </div>
  </div>
</template>

<script>
import router from '@/router/index.js'
import { computed } from 'vue';
import {getGameStore} from "@/store.js";
import {logic} from '@/logic/main.js';

import logo from '@/assets/logo.png';
import { notify, showDialog } from '@/main.js';

export default {
  name: 'WaitingLobbyComponent',
  setup() {
    const gameStore = getGameStore();
    const game = gameStore.getGame();

    if (!game) {
      router.push({path: '/'});
    }

    const logoSrc = logo;

    return {
      players: computed(() => game.getPlayers()),
      lobby_code: computed(() => game.getLobbyCode()),
      lobby_owner: computed(() => game.getLobbyOwner()),
      logo: logoSrc
    };
  },
  data() {
    return {
      showDialog: false,
      selectedAvatar: null,
      showEditIcon: false,
      avatars: [
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        { src: logo },
        // ...
      ],
    }
  },
  methods: {
    animateElement() {
      document.querySelectorAll(".fr-animate-2").forEach((el) => {
        el.classList.add('fr-animate-init');
      });
    },
    copyLobbyCode() {
      let lobby_code = this.lobby_code;
      navigator.clipboard.writeText(lobby_code);
      notify('success', 'Lobby-ID kopiert', 'Die Lobby-ID wurde in die Zwischenablage kopiert.');
    },
    selectAvatar(avatar) {
      this.showDialog = false;
      console.log(avatar)
    },
    startGame() {
      if (this.players.length < 2) {
        notify('error', 'Spiel kann nicht gestartet werden', 'Es müssen mindestens 2 Spieler in der Lobby sein.');
        return;
      }
      logic.startGame();
    }
  },
  mounted() {
    setTimeout(() => {
      this.animateElement()
    }, 50);
  },
}






// export default {
//   name: 'WaitingLobbyComponent',
//   data() {
//     return {
//         logo: logo,
//     };
//   },
//   methods: {
//     animateElement() {
//       document.querySelectorAll(".fr-animate-2").forEach((el) => {
//         el.classList.add('fr-animate-init');
//       });
//     },
//   },
//   mounted() {
//     let game = logic.getGame();
//     let lobby_code = game.getLobbyCode();

//     let h2 = document.querySelector('h2');
//     h2.innerHTML = 'Lobby-ID: ' + lobby_code;
//     let players = game.getPlayers();
//     console.log(players);
//     for (let i = 0; i < players.length; i++) {
//       console.log(players[i])
//       let playerList = document.getElementById('playerList');
//       let player = document.createElement('div');
//       // avatar: use logo for now and player name
//       player.innerHTML = '<img src="'+logo+'" class="avatar"><span class="player-name">' + players[i].name + '</span>'
//       if (players[i].getIsOwner()) {
//         player.querySelector('.player-name').innerHTML = '👑 ' + player.querySelector('.player-name').innerHTML;
//         // add v-tooltip to owner
//         player.setAttribute('v-tooltip', '"Spielbesitzer"');
//       }
//       if (players[i].getIsSelf()) {
//         player.querySelector('.player-name').innerHTML += ' (Du)';
//       }
//       playerList.appendChild(player);
//       player.classList.add('player', 'fr-animate-2', 'fr-move-up', 'fr-delay-3');

//       // add player status and append it to the player div
//       let playerStatus = document.createElement('div');
//       playerStatus.innerHTML = 'Status: Bereit';
//       playerStatus.classList.add('player-status');
//       player.appendChild(playerStatus);
//     }
//     setTimeout(() => {
//       this.animateElement()
//     }, 100); // 100 Millisekunden Verzögerung


//     // let playerList = document.getElementById('playerList');
//     // let player1 = document.createElement('div');
//     // player1.innerHTML = '#1: ' + gameOptions.owner_name;
//     // playerList.appendChild(player1);
//     // player1.classList.add('player', 'fr-animate-2', 'fr-move-up', 'fr-delay-3');
//     // player1.setAttribute("id", "singlePlayer");

//     // // add player status and append it to the player div
//     // let player1Status = document.createElement('div');
//     // player1Status.innerHTML = 'Status: Bereit';
//     // player1Status.classList.add('player-status');
//     // player1.appendChild(player1Status);
//     // setTimeout(() => {
//     //   this.animateElement()
//     // }, 100); // 100 Millisekunden Verzögerung
//   }
// };
</script>