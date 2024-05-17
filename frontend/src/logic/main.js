import {Game} from '@/logic/classes/Game.js'
import {GameState, PlayerState} from '@/logic/classes/Enums.js'
import {Player} from '@/logic/classes/Player.js'
import { useGameStore } from "@/store.js";
import Cookies from 'js-cookie';
import { sendWsMessage } from '@/logic/websocket.js';
let game;
let player;

async function createLobby(options, avatar_id){
    let gameOptions = options;
    let playerResponse = await fetch('http://localhost:8000/player/create_player', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({name: gameOptions.owner_name, avatar_id: avatar_id})
    });

    if (playerResponse.ok) {
        const playerData = await playerResponse.json();
        player = new Player(playerData.id, playerData.name, playerData.avatar_id, gameOptions.lives_per_player, true, true);
        gameOptions['owner_id'] = playerData.id;
    } else {    
        // throw error @TODO
        return false;
    }


    fetch('http://localhost:8000/lobby/create_lobby', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(gameOptions)
    }).then(response => console.log(response.json()))
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
            console.log(JSON.stringify(data));
        } else {
            // throw error @TODO
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