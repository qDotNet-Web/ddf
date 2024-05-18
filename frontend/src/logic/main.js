import {Game} from '@/logic/classes/Game.js'
import {GameState, PlayerState, GameType} from '@/logic/classes/Enums.js'
import {Player} from '@/logic/classes/Player.js'
import {getGameStore} from "@/store.js";
import Cookies from 'js-cookie';
import { sendWsMessage } from '@/logic/websocket.js';
let player;

function getGame(){
    return getGameStore().getGame();
}

async function createPlayer(name, avatar_id, lives){
    let playerResponse = await fetch('http://localhost:8000/player/create_player', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({name: name, avatar_id: avatar_id})
    });

    if (playerResponse.ok) {
        const playerData = await playerResponse.json();
        player = new Player(playerData.player_id, name, avatar_id, lives, true, true);
        return true;
    } else {    
        return false;
    }
}

async function createLobby(options, avatar_id){
    let gameOptions = options;
    // wait for player to be created
    await createPlayer(gameOptions.owner_name, avatar_id, gameOptions.lives_per_player);
    // set owner id to player id
    gameOptions['owner_id'] = player.getId();

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
            let players = [];
            players.push(player);
            let gameType = gameOptions.text_based ? GameType.TEXT : GameType.VOICE;
            let gameObj = new Game(gameOptions.code, gameOptions.round_timer, players, gameType);

            const gameStore = getGameStore();
            gameStore.setGame(gameObj);
            Cookies.set('game', JSON.stringify(getGame().toArray()));

            return true;
        });
}


async function joinLobby(lobbyCode, playerName){
    try {
        const response = await fetch(`http://localhost:8000/lobby/join_code/${lobbyCode}?player_name=${playerName}`, {
            method: 'POST',
            headers: {
                'accept': 'application/json',
            },
        });

        if (response.status == 404) {
            console.clear();
            return false;
        }

        const data = await response.json();
        let players = [];
        let playerData = data.players;
        for (let i = 0; i < playerData.length; i++) {
            let player = new Player(playerData[i].id, playerData[i].name, playerData[i].avatar_id, data.lives_per_player, false, false);
            players.push(player);
        }
        let gameType = data.text_based ? GameType.TEXT : GameType.VOICE;
        let gameState = data.game_state;
        
        let gameObj = new Game(lobbyCode, data.round_timer, players, gameType);
        gameObj.setGameState(gameState);
        getGameStore().setGame(gameObj);
        Cookies.set('game', JSON.stringify(getGame().toArray()));
        return true;




    } catch(error) {
        console.log(error);
        return false;
    }
}

function playerJoined(id, name, avatar_id, lives, self){
    player = new Player(id, name, avatar_id, lives, self);
    getGame().addPlayer(player);
    console.log("player joined", getGame().players);
}

function playerLeft(id, new_owner_id){
    player = getGame().players.find(player => player.id == id);
    player.setPlayerState(PlayerState.DISCONNECTED);
    player.setLobbyOwner(false);
    if (new_owner_id) {
        let newOwner = new_owner_id;
        getGame().players.find(player => player.id == newOwner).setLobbyOwner(true);
    }
}

function startedGame(){
    getGame().startGame();
}

function endedGame(){
    getGame().endGame();
}

function startedRound(){
    getGame().startRound();
}

function endedRound(){
    getGame().endRound();
}

function votedForPlayer(votingPlayerId, votedPlayerId){
    getGame().players.find(player => player.id == votingPlayerId).voteForPlayer(getGame().players.find(player => player.id == votedPlayerId));
}

function updateLobby(data){
    let game = getGame();
    // 
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
    votedForPlayer,
    getGame,
    updateLobby
}