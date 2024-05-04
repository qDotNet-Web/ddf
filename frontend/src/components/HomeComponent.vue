/* eslint-disable */
<style scoped>

</style>

<template>
    <div class="container my-auto vertical-center dff-padding-top" id="app">
        <img src="@/assets/logo.png" alt="Logo" class="icon mb-4">
        <h1 class="dff-h1 mb-4">Der Dümmste fliegt!</h1>
        <div class="d-flex justify-content-center gap-5">
            <button class="btn btn-main" data-bs-toggle="modal" data-bs-target="#playModal">Start</button>
            <button class="btn btn-main" data-bs-toggle="modal" data-bs-target="#anleitungsModal">Anleitung</button>
        </div>
        <!-- Modal 1 -->
        <div class="modal fade" id="playModal" tabindex="-1" aria-labelledby="playModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content bg-dark text-light">
                    <div class="modal-header">
                        <h5 class="modal-title" id="playModalLabel">Möchtest du einem Spiel beitreten, oder erstellen?</h5>
                    </div>
                    <div class="modal-body space-between">
                        <button type="button" class="btn btn-modal" data-bs-dismiss="modal" id="createGameButton" data-bs-toggle="modal" data-bs-target="#createLobbyModal">Erstellen</button>
                        <button type="button" class="btn btn-modal" id="joinGameButton" data-bs-toggle="modal" data-bs-target="#joinLobbyModal">Beitreten</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Modal 2 -->
        <div class="modal fade" id="anleitungsModal" tabindex="-1" aria-labelledby="anleitungsModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content bg-dark text-light">
                    <div class="modal-header">
                        <h5 class="modal-title" id="anleitungsModalLabel">Wie wird gespielt?</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <p>Das Spiel besteht aus 3 Runden. In jeder Runde wird eine Frage gestellt, die von den Spielern beantwortet werden muss...</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-modal" data-bs-dismiss="modal">Schließen</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Modal 3 / createLobby-->
        <div class="modal fade" id="createLobbyModal" tabindex="-1" aria-labelledby="createLobbyModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content bg-dark text-light">
                    <div class="modal-header">
                        <h5 class="modal-title" id="createLobbyModalLabel">Lobby erstellen</h5>
                    </div>
                    <div class="modal-body">
                        <div class="input-text mb-3">
                            <label for="ip_playerName">Dein Name</label>
                            <input type="text" id="ip_playerName" name="ip_playerName" placeholder="Schlaubischlumpf" maxlength="20">
                        </div>
                        <div class="input-slide mb-3">
                            <label for="ip_roundLength">Rundenlänge: 3 min</label>
                            <input type="range" id="ip_roundLength" name="ip_roundLength" min="1" max="3" value="3" @input="updateRoundlength">
                        </div>
                        <div class="input-slide mb-3">
                            <label for="ip_maxPlayers">Spieleranzahl: 4</label>
                            <input type="range" id="ip_maxPlayers" name="ip_maxPlayers" min="2" max="8" value="4" @input="updateMaxPlayers">
                        </div>

                        <div class="input-slide mb-3">
                            <label for="ip_playerLives">Spielerleben: 3</label>
                            <input type="range" id="ip_playerLives" name="ip_playerLives" min="1" max="10" value="3" @input="updatePlayerLives">
                        </div>
                    </div>
                    <div class="modal-footer space-between">
                        <button type="button" class="btn btn-modal" data-bs-dismiss="modal">Schließen</button>
                        <button type="button" class="btn btn-modal" data-bs-dismiss="modal" @click="createLobby">Starten</button>
                    </div>
                </div>
            </div>
        </div>
        <!-- Modal 4 JoinLobby -->
        <div class="modal fade" id="joinLobbyModal" tabindex="-1" aria-labelledby="joinLobbyModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content bg-dark text-light">
                    <div class="modal-header">
                        <h5 class="modal-title" id="joinLobbyModalLabel">Lobby beitreten</h5>
                    </div>
                    <div class="modal-body">
                        <div class="input-text mb-3">
                            <label for="ip_playerName">Lobby-ID</label>
                            <input type="text" name="ip_lobbyID" placeholder="123456" maxlength="6" v-model="lobbyId">
                        </div>
                        <div class="input-text mb-3">
                            <label for="ip_playerName">Dein Name</label>
                            <input type="text" name="ip_playerName" placeholder="Schlaubischlumpf" maxlength="20" v-model="playerName">
                        </div>
                    <div class="modal-footer space-between">
                        <button type="button" class="btn btn-modal" data-bs-dismiss="modal">Schließen</button>
                        <button type="button" class="btn btn-modal" data-bs-dismiss="modal" @click="joinLobby">Beitreten</button>
                    </div>
                </div>
            </div>
        </div>
    </div>

        <!-- Footer -->
        <footer class="mt-auto mb-4 text-center fw-bold">
        © 2024 qdotnet <br>
        Es werden keine personenbezogenen Daten erhoben.
        </footer>
    </div>
</template>

<script>
export default {
  components: {
  },
  data() {
    return {
        lobbyId: '',
        playerName: '',
        currentView: null
    }
  },
  methods: {
    updateMaxPlayers(event) {
        document.querySelector('label[for="ip_maxPlayers"]').innerText = `Spieleranzahl: ${event.target.value}`;
    },
    updatePlayerLives(event) {
        document.querySelector('label[for="ip_playerLives"]').innerText = `Spielerleben: ${event.target.value}`;
    },
    updateRoundlength(event) {
        document.querySelector('label[for="ip_roundLength"]').innerText = `Rundenlänge: ${event.target.value} min`;
    },
    joinLobby() {
        let lobbyId = this.lobbyId;
        let playerName = this.playerName;
        if (lobbyId.length != 6) {
            this.$swal({
                title: 'Fehler',
                text: 'Die Lobby-ID muss 6 Zeichen lang sein.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return;
        }
        if  (playerName.length < 1) {
            this.$swal({
                title: 'Fehler',
                text: 'Bitte gib deinen Namen ein.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return;
        }
    },
    createLobby() {
        let playerName = document.getElementById('ip_playerName').value;
        let roundLength = document.getElementById('ip_roundLength').value;
        let maxPlayers = document.getElementById('ip_maxPlayers').value;
        let playerLives = document.getElementById('ip_playerLives').value;
        if  (playerName.length < 1) {
            this.$swal({
                title: 'Fehler',
                text: 'Bitte gib deinen Namen ein.',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return;
        }
        this.$swal({
            title: 'Lobby erstellt',
            text: 'Deine Lobby wurde erstellt. Die Lobby-ID lautet: 123456',
            icon: 'success',
            confirmButtonText: 'OK'
        });
        
    }
  }
}
</script>