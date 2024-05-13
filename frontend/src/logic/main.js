import {Game} from '@/logic/classes/Game.js'
import {GameState, PlayerState} from '@/logic/classes/Enums.js'
import {Player} from '@/logic/classes/Player.js'

import router from '@/router/index.js'
import { useGameStore } from "@/store.js";
import Cookies from 'js-cookie';
let game;
let player;

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
            game = new Game(gameOptions.round_timer, gameOptions.round, gameOptions.players);
            return true;
        });
}


async function joinLobby(lobbyCode){
    try {
        const response = await fetch('http://localhost:8000/lobby/get_by_code/'+lobbyCode);
        if (response.ok) {
            const data = await response.json();
            // const gameStore = useGameStore();
            // gameStore.setGameOptions(data);
            // Cookies.set('gameOptions', JSON.stringify(gameStore.gameOptions));
            // router.push('/waitingLobby');
            // game = new Game(data.round_timer, data.round, data.players);
            console.log(JSON.stringify(data));
        } else {
            // throw error
            alert('Lobby not found');
        }
    } catch(error) {
    }
}


// event handlers

function playerJoined(id, name, avatar_id, lives, self){
    player = new Player(id, name, avatar_id, lives, self);
    game.addPlayer(player);
}

function playerLeft(id, new_owner_id){
    player = game.players.find(player => player.id == id);
    player.setPlayerState(PlayerState.DISCONNECTED);
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

function votedForPlayer(votingPlayerId, votedPlayerId){
    game.players.find(player => player.id == votingPlayerId).voteForPlayer(game.players.find(player => player.id == votedPlayerId));
}

export const logic = {
    createLobby,
    joinLobby,
    playerJoined,
    playerLeft,
    startedGame,
    endedGame,
    startedRound,
    endedRound,
    votedForPlayer
}