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
    <div class="container my-auto vertical-center dff-padding-vh homeContainer" id="app">
        <div class="howToPlay"></div> <!-- TODO -->
        <img src="@/assets/logo.png" alt="Logo" id="main_logo" class="icon mb-4 transition-05">
        <h1 class="dff-h1 mb-4 transition-05">Der Dümmste fliegt!</h1>
        <div class="d-flex justify-content-center gap-5 homeActions">
            <button class="btn btn-main-new fr-animate fr-move-up fr-delay-3" id="startButton" data-bs-toggle="modal"
                data-bs-target="#createLobbyModal" @click="modalCreate_visible = true">Erstellen</button>
            <button class="btn btn-main-new fr-animate fr-move-up fr-delay-5" data-bs-toggle="modal"
                data-bs-target="#joinLobbyModal" @click="modalJoin_visible = true">Beitreten</button>
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

        <Dialog v-model:visible="modalCreate_visible" modal :pt="{
            root: 'border-none',
            mask: {
                style: 'backdrop-filter: blur(2px)'
            }
        }">
            <template #container="{ closeCallback }">
                <div id="createLobbyModal" class="flex flex-column px-3 py-3 gap-4"
                    style="border-radius: 12px; background-color: var(--main-bg-color)"
                    aria-labelledby="createLobbyModalLabel">
                    <div class="gap-2 mb-pi" style="justify-content: center; display: flex;">
                        <div class="iconBox" style="display: inline-flex;">
                            <i class="pi pi-plus-circle text-5xl is-size-35 is-main-highlight-color"></i>
                        </div>

                    </div>
                    <div class="inline-flex flex-column gap-2 mb-4" style="text-align: center;">
                        <h5 class="modal-title" id="createLobbyModalLabel">Lobby erstellen</h5>
                    </div>
                    <div class="inline-flex flex-column gap-2 mb-3">
                        <FloatLabel class="ip_float">
                            <InputText id="ip_playerName" name="ip_playerName" v-model="ip_playerName"
                                class="w-full ip_float bg-white-alpha-20" maxlength="20" />
                            <label for="ip_playerName">Username</label>
                        </FloatLabel>
                    </div>
                    <div class="inline-flex flex-column gap-2 mb-3">
                        <label for="ip_roundLength" class="mb-3">Rundenlänge: {{ ip_roundLength }} min <i style="font-size: 14px;" class="pi pi-clock"></i></label>
                        <Slider name="ip_roundLength" id="ip_roundLength" v-model="ip_roundLength" class="w-full mb-3"
                            :min="1" :max="10" />
                    </div>
                    <div class="inline-flex flex-column gap-2 mb-3">
                        <label for="ip_playerLives" class="mb-3">Spielerleben: {{ ip_playerLives }} <i style="font-size: 14px;" class="pi pi-heart-fill"></i></label>
                        <Slider name="ip_playerLives" id="ip_playerLives" v-model="ip_playerLives" class="w-full mb-3"
                            :min="1" :max="10" />
                    </div>
                    <div class="inline-flex flex-column gap-2 mb-3">
                        <div class="input-switch mb-3">
                            <SelectButton :unselectable="false" v-model="ip_lobbyType" :options="lobbyType_options"
                                aria-labelledby="basic" />
                        </div>
                    </div>
                    <div class="flex align-items-center gap-3" style="display: flex;">
                        <button type="button" class="btn btn-main-new btn-modal-new" data-bs-dismiss="modal"
                            @click="closeCallback">Schließen</button>
                        <button type="button" id="createLobbyButton" class="btn btn-main-new btn-modal-new"
                            @click="createLobby()">Starten</button>
                    </div>
                </div>
            </template>
        </Dialog>
        <!-- Modal 4 JoinLobby -->
        <Dialog v-model:visible="modalJoin_visible" modal :pt="{
            root: 'border-none',
            mask: {
                style: 'backdrop-filter: blur(2px)'
            }
        }">
            <template #container="{ closeCallback }">
                <div id="joinLobbyModal" class="flex flex-column px-3 py-3 gap-4"
                    style="border-radius: 12px; background-color: var(--main-bg-color)"
                    aria-labelledby="joinLobbyModalLabel">
                    <div class="gap-2 mb-pi" style="justify-content: center; display: flex;">
                        <div class="iconBox" style="display: inline-flex;">
                            <i class="pi pi-arrow-circle-right text-5xl is-size-35 is-main-highlight-color"></i>
                        </div>

                    </div>
                    <div class="inline-flex flex-column gap-2 mb-4" style="text-align: center;">
                        <h5 class="modal-title" id="joinLobbyModalLabel">Lobby beitreten</h5>
                    </div>
                    <div class="inline-flex flex-column gap-2 mb-custom-4">
                        <FloatLabel class="ip_float">
                            <InputText id="ip_lobbyID" name="ip_lobbyID" v-model="ip_lobbyID" class="w-full ip_float" />
                            <label for="ip_lobbyID">Lobby-ID</label>
                        </FloatLabel>
                    </div>
                    <div class="inline-flex flex-column gap-2 mb-4">
                        <FloatLabel class="ip_float">
                            <InputText id="ip_playerName" name="ip_playerName" v-model="ip_playerName"
                                class="w-full ip_float" maxlength="20" />
                            <label for="ip_playerName">Username</label>
                        </FloatLabel>
                    </div>
                    <div class="flex align-items-center gap-3" style="display: flex;">
                        <button type="button" class="btn btn-main-new btn-modal-new" data-bs-dismiss="modal"
                            @click="closeCallback">Schließen</button>
                        <button type="button" class="btn btn-main-new btn-modal-new"
                            @click="joinLobby()">Beitreten</button>
                    </div>
                </div>
            </template>
        </Dialog>

        <!-- Footer -->
    </div>
</template>


<script>
import router from '@/router/index.js'
import { reactive, ref } from 'vue';
import Cookies from 'js-cookie';
import { logic } from '@/logic/main.js';
import { notify, showDialog } from '@/main.js';
import { Modal } from 'bootstrap';

Element.prototype.remove = function () {
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
        updatePlayerLives(originalEvent) {
            document.querySelector('label[for="ip_playerLives"]').innerText = `Spielerleben: ${originalEvent.value}`;
        },
        updateRoundlength(originalEvent) {
            document.querySelector('label[for="ip_roundLength"]').innerText = `Rundenlänge: ${originalEvent.value} min`;
        },
        animateElement() {
            document.querySelectorAll(".fr-animate").forEach((el) => {
                el.classList.add('fr-animate-init');
            });
        },
    },
    mounted() {
        // check for cookies and if lobby is still active
        let gameOptions = Cookies.get('gameOptions');
        if (gameOptions) {
            let gameOptionsObj = JSON.parse(gameOptions);
            let lobbyId = gameOptionsObj.lobby_id;

        }
        // animate elements
        setTimeout(() => {
            this.animateElement()
        }, 100);

    },
    setup() {

        const ip_roundLength = ref(3);
        const ip_playerName = ref(null);
        const ip_playerLives = ref(3);
        const ip_lobbyType = ref('Text');
        const lobbyType_options = ref(['Text', 'Voice']);
        const ip_lobbyID = ref(null);
        const modalCreate_visible = ref(false);
        const modalJoin_visible = ref(false);

        const data = reactive({
            lobbyId: '',
            playerName: '',
            currentView: null
        });

        function toggleLoadingScreen(toggle) {
            let loading = document.querySelector('.loading');
            let h1 = document.querySelector('h1');
            let homeActions = document.querySelector('.homeActions');
            let main_logo = document.getElementById('main_logo');
            if (toggle) {
                h1.classList.add('fade-out');
                homeActions.classList.add('fade-out');
                loading.classList.add('fade-in');
                main_logo.classList.add('spin');
            } else {
                h1.classList.remove('fade-out');
                homeActions.classList.remove('fade-out');
                loading.classList.remove('fade-in');
                main_logo.classList.remove('spin');
            }
        }

        async function joinLobby() {
            let lobbyId = ip_lobbyID.value;
            let playerName = ip_playerName.value;
            if (!lobbyId || lobbyId.length != 8) {
                notify("error", "Fehler", "Bitte gib eine gültige Lobby-ID ein.");
                return;
            }
            if (!playerName || playerName.length < 1) {
                notify("error", "Fehler", "Bitte gib einen gültigen Namen ein.");
                return;
            }

            let modalElement = document.getElementById('joinLobbyModal');
            let closeButton = modalElement.querySelector('[data-bs-dismiss="modal"]');
            closeButton.click();

            toggleLoadingScreen(true);

            let delay = new Promise(resolve => setTimeout(resolve, 1500));
            let joinResult = logic.joinLobby(lobbyId, playerName);
            let [joined] = await Promise.all([joinResult, delay]);
            toggleLoadingScreen(false);
            if (!joined) {
                notify("error", "Fehler", "Die Lobby konnte nicht gefunden werden.");
                return;
            }
            router.push("/waitingLobby");
        }

        async function createLobby() {
            let playerName = ip_playerName.value;
            if (!playerName || playerName.length < 1) {
                notify("error", "Fehler", "Bitte gib einen gültigen Namen ein.");
                return;
            }

            let modalElement = document.getElementById('createLobbyModal');
            let closeButton = modalElement.querySelector('[data-bs-dismiss="modal"]');
            closeButton.click();

            let roundLength = parseInt(ip_roundLength.value);
            let playerLives = parseInt(ip_playerLives.value);
            let isTextBased = true;

            toggleLoadingScreen(true);

            let gameOptions = {
                "owner_name": playerName,
                "is_active": true,
                "players": [
                    playerName,
                ],
                'round_timer': roundLength * 60,
                'lives_per_player': playerLives,
                'text_based': ip_lobbyType.value == 'Text' ? true : false,
                'used_questions': []

            }
            // pick number between 0 and 19
            let ownerAvatarId = Math.floor(Math.random() * 20);

            let delay = new Promise(resolve => setTimeout(resolve, 2000));
            let [created] = await Promise.all([logic.createLobby(gameOptions, ownerAvatarId), delay]);
            toggleLoadingScreen(false);
            router.push("/waitingLobby");
        }
        return { createLobby, joinLobby, ip_roundLength, ip_playerName, ip_playerLives, ip_lobbyType, lobbyType_options, ip_lobbyID, modalCreate_visible, modalJoin_visible }

    },
}
</script>
