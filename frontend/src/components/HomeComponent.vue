/* eslint-disable */
<style scoped></style>

<template>
        <div class="loading">
            <div class="circle"></div>
            <div class="circle"></div>
            <div class="circle"></div>
            <div class="shadow"></div>
            <div class="shadow"></div>
            <div class="shadow"></div>
            </div>
    <div class="container my-auto vertical-center dff-padding-top" id="app">
        <div class="howToPlay">
            
        </div>
        <img src="@/assets/logo.png" alt="Logo" class="icon mb-4">
        <h1 class="dff-h1 mb-4">Der Dümmste fliegt!</h1>
        <div class="d-flex justify-content-center gap-5 homeActions">
            <button class="btn btn-main-new fr-animate fr-move-up fr-delay-3" id="startButton" data-bs-toggle="modal" data-bs-target="#createLobbyModal">Erstellen</button>
            <button class="btn btn-main-new fr-animate fr-move-up fr-delay-5" data-bs-toggle="modal" data-bs-target="#joinLobbyModal">Beitreten</button>

        </div>
        <div class="container my-auto vertical-center dff-padding-top homeContainer" id="app">
            <div class="howToPlay"></div> <!-- TODO -->
            <img src="@/assets/logo.png" alt="Logo" id="main_logo" class="icon mb-4 transition-05">
            <h1 class="dff-h1 mb-4 transition-05">Der Dümmste fliegt!</h1>
            <div class="d-flex justify-content-center gap-5 homeActions">
                <button class="btn btn-main" id="startButton" data-bs-toggle="modal"
                    data-bs-target="#createLobbyModal">Erstellen</button>
                <button class="btn btn-main" data-bs-toggle="modal" data-bs-target="#joinLobbyModal">Beitreten</button>
            </div>
            <!-- Modal 2 -->
            <div class="modal fade" id="anleitungsModal" tabindex="-1" aria-labelledby="anleitungsModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content bg-dark text-light">
                        <div class="modal-header">
                            <h5 class="modal-title" id="anleitungsModalLabel">Wie wird gespielt?</h5>
                            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">
                            <p>Das Spiel besteht aus 3 Runden. In jeder Runde wird eine Frage gestellt, die von den
                                Spielern beantwortet werden muss...</p>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-modal" data-bs-dismiss="modal">Schließen</button>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Modal 3 / createLobby-->
            <div class="modal fade" id="createLobbyModal" tabindex="-1" aria-labelledby="createLobbyModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content bg-dark text-light">
                        <div class="modal-header">
                            <h5 class="modal-title" id="createLobbyModalLabel">Lobby erstellen</h5>
                        </div>
                        <div class="modal-body">
                            <div class="input-text mb-3">
                                <label for="ip_playerName">Dein Name</label>
                                <input type="text" id="ip_playerName" name="ip_playerName"
                                    placeholder="Schlaubischlumpf" maxlength="20">
                            </div>
                            <div class="input-slide mb-3">
                                <label for="ip_roundLength">Rundenlänge: 3 min</label>
                                <input type="range" id="ip_roundLength" name="ip_roundLength" min="1" max="10" value="3"
                                    @input="updateRoundlength">
                            </div>
                            <div class="input-slide mb-3">
                                <label for="ip_playerLives">Spielerleben: 3</label>
                                <input type="range" id="ip_playerLives" name="ip_playerLives" min="1" max="10" value="3"
                                    @input="updatePlayerLives">
                            </div>
                        </div>
                        <div class="modal-footer space-between">
                            <button type="button" class="btn btn-modal" data-bs-dismiss="modal">Schließen</button>
                            <button type="button" id="createLobbyButton" class="btn btn-modal" data-bs-dismiss="modal"
                                @click="createLobby()">Starten</button>
                        </div>
                    </div>


                    <div class="modal-footer space-between">
                        <button type="button" class="btn btn-main-new btn-modal-new" data-bs-dismiss="modal">Schließen</button>
                        <button type="button" class="btn btn-main-new btn-modal-new" data-bs-dismiss="modal" @click="createLobby()">Starten</button>
                    </div>

                </div>
            </div>
            <!-- Modal 4 JoinLobby -->
            <div class="modal fade" id="joinLobbyModal" tabindex="-1" aria-labelledby="joinLobbyModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered">
                    <div class="modal-content bg-dark text-light">
                        <div class="modal-header">
                            <h5 class="modal-title" id="joinLobbyModalLabel">Lobby beitreten</h5>
                        </div>
                        <div class="modal-body">
                            <div class="input-text mb-3">
                                <label for="ip_playerName">Lobby-ID</label>
                                <input type="text" name="ip_lobbyID" placeholder="1B3C5D7E" maxlength="8"
                                    v-model="lobbyId">
                            </div>
                            <div class="input-text mb-3">
                                <label for="ip_playerName">Dein Name</label>
                                <input type="text" name="ip_playerName" placeholder="Schlaubischlumpf" maxlength="20"
                                    v-model="playerName">
                            </div>
                            <div class="modal-footer space-between">
                                <button type="button" class="btn btn-modal" data-bs-dismiss="modal">Schließen</button>
                                <button type="button" class="btn btn-modal" data-bs-dismiss="modal"
                                    @click="joinLobby()">Beitreten</button>
                            </div>
                        </div>


                        </div>
                    <div class="modal-footer space-between">
                        <button type="button" class="btn btn-main-new btn-modal-new" data-bs-dismiss="modal">Schließen</button>
                        <button type="button" class="btn btn-main-new btn-modal-new" data-bs-dismiss="modal" @click="joinLobby()">Beitreten</button>

                    </div>
                </div>
            </div>
            <!-- Footer -->
        </div>
    </div>
   
        <!-- Footer -->
        <footer class="mt-auto mb-4 text-center fw-bold">
            © 2024 <br>
            qdotnet.de <br>
            └ <router-link to="/impressum" class="custom-link">Impressum</router-link> ┘
        </footer>
</template>

<script>
import router from '@/router/index.js'
import { reactive, ref } from 'vue';
import { useGameStore } from "@/store.js";
import Cookies from 'js-cookie';


window.onload = function() {
    document.querySelectorAll(".fr-animate").forEach((el) => {
        el.classList.add('fr-animate-init');
    });
}

Element.prototype.remove = function() {
    this.parentElement.removeChild(this);
}
NodeList.prototype.remove = HTMLCollection.prototype.remove = function () {
    for (var i = this.length - 1; i >= 0; i--) {
        if (this[i] && this[i].parentElement) {
            this[i].parentElement.removeChild(this[i]);
        }
    }
}

export default {
    components: {
    },
    data() {
        return {

        }
    },
    methods: {
        updatePlayerLives(event) {
            document.querySelector('label[for="ip_playerLives"]').innerText = `Spielerleben: ${event.target.value}`;
        },
        updateRoundlength(event) {
            document.querySelector('label[for="ip_roundLength"]').innerText = `Rundenlänge: ${event.target.value} min`;
        },
    },
    mounted() {
        // see if cookies  are set
        let gameStore = useGameStore();
        if (Cookies.get('gameOptions') != null) {
            gameStore = JSON.parse(Cookies.get('gameOptions'));
            // console.log(JSON.stringify(gameStore.gameOptions), Cookies.get('gameOptions'));
        }
    },
    setup() {
        const data = reactive({
            lobbyId: '',
            playerName: '',
            currentView: null
        });
        function joinLobby() {
            if (data.lobbyId.length != 6) {
                // this.$swal({
                //     title: 'Fehler',
                //     text: 'Die Lobby-ID muss 6 Zeichen lang sein.',
                //     icon: 'error',
                //     confirmButtonText: 'OK'
                // });
                return;
            }
            if (data.playerName.length < 1) {
                // this.$swal({
                //     title: 'Fehler',
                //     text: 'Bitte gib deinen Namen ein.',
                //     icon: 'error',
                //     confirmButtonText: 'OK'
                // });
                return;
            }
        }

        async function createLobby() {
            let playerName = document.getElementById('ip_playerName').value;
            let roundLength = document.getElementById('ip_roundLength').value;
            let playerLives = document.getElementById('ip_playerLives').value;
            if (playerName.length < 1) {
                // this.$swal({
                //     title: 'Fehler',
                //     text: 'Bitte gib deinen Namen ein.',
                //     icon: 'error',
                //     confirmButtonText: 'OK'
                // });
                return;
            }
            let loading = document.querySelector('.loading');
            let h1 = document.querySelector('h1');
            let homeActions = document.querySelector('.homeActions');
            let main_logo = document.getElementById('main_logo');
            h1.classList.add('fade-out');
            homeActions.classList.add('fade-out');
            loading.classList.add('fade-in');
            main_logo.classList.add('spin');
            

            let gameOptions = {
                    'owner_name': playerName,
                    'is_active': true,
                    'players': [
                        playerName,
                    ],
                    'round_timer': roundLength * 60,
                    'lives_per_player': playerLives
                }
            // wait 3 seconds
            setTimeout(() => {
                fetch('http://localhost:8000/lobby/create_lobby', {
                    method: 'POST',
                    headers: {
                        'accept': 'application/json',
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(gameOptions)
                }).then(response => response.json())
                    .then(data => {
                        gameOptions['code'] = data.code;
                        const gameStore = useGameStore();
                        gameStore.setGameOptions(gameOptions);
                        Cookies.set('gameOptions', JSON.stringify(gameStore.gameOptions));
                        h1.classList.remove('fade-out');
                        homeActions.classList.remove('fade-out');
                        loading.classList.remove('fade-in');
                        main_logo.classList.remove('spin');
                        router.push('/waitingLobby');
                    });
            }, 3000);
        }
        return { createLobby, joinLobby}
    },
}
</script>