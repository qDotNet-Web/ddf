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
                        <button type="button" class="btn btn-modal" id="createGameButton" @click="Vue.component("CreateLobbyComponent")">Erstellen</button>
                        <button type="button" class="btn btn-modal" id="joinGameButton">Beitreten</button>
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

        <!-- Footer -->
        <footer class="mt-auto mb-4 text-center fw-bold">
        © 2024 qdotnet <br>
        Es werden keine personenbezogenen Daten erhoben.
        </footer>
    </div>
</template>

<script>
export default {
    name: 'HomeComponent'
}
</script>