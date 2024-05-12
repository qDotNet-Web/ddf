import router from '@/router/index.js'
import { useGameStore } from "@/store.js";
import Cookies from 'js-cookie';
let game;

function createLobby(options){
    let gameOptions = options;
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
            // h1.classList.remove('fade-out');
            // homeActions.classList.remove('fade-out');
            // loading.classList.remove('fade-in');
            // main_logo.classList.remove('spin');
            router.push('/waitingLobby');
            game = new Game(gameOptions.round_timer, gameOptions.round, gameOptions.players);
        });
}

function joinLobby(lobbyId){
    let gameOptions;
    connectWebSocket(lobbyId);
    try {
       gameOptions = send({type: 'joinLobby', lobbyId: lobbyId});
    } catch (error) {
        console.error(error);
    }
    game = new Game(gameOptions.round_timer, gameOptions.round, gameOptions.players);

}

function playerJoined(id, name, lives, self){
    player = new Player(id, name, lives, self);
    game.addPlayer(player);
}

function playerLeft(id, new_owner_id){
    player = game.players.find(player => player.id == id);
    player.setActive(false);
    player.setLobbyOwner(false);
    if (new_owner_id) {
        let newOwner = new_owner_id;
        game.players.find(player => player.id == newOwner).setLobbyOwner(true);
    }
}

function startedGame(){
    game.startGame();
}

function endedGame(){
    game.endGame();
}

function startedRound(){
    game.startRound();
}

function endedRound(){
    game.endRound();
}

function votedForPlayer(){
}