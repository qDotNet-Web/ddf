import {Game} from '@/logic/classes/Game.js'
import {GameState, PlayerState, GameType} from '@/logic/classes/Enums.js'
import {Player} from '@/logic/classes/Player.js'
import {getGameStore} from "@/store.js";
import {Cookies} from '@/logic/obfuscation.js';
let player;


function getGame(){
    return getGameStore().getGame();
}

async function createPlayer(name, avatar_id, lives, self){
    let playerResponse = await fetch('https://api.derduemmstefliegt.online/player/create_player', {
        method: 'POST',
        headers: {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({player_name: name, avatar_id: avatar_id, player_state: PlayerState.WAITING, lives: lives})
    });

    if (playerResponse.ok) {
        const playerData = await playerResponse.json();
        player = new Player(playerData.player_id, name, avatar_id, lives, self);
        Cookies.set('playerData', JSON.stringify(player.toArray()));
        return true;
    } else {    
        return false;
    }
}

async function createLobby(options, avatar_id){
    let gameOptions = options;
    // wait for player to be created
    await createPlayer(gameOptions.owner_name, avatar_id, gameOptions.lives_per_player, true);
    // set owner id to player id
    gameOptions['owner_id'] = player.getId();

    fetch('https://api.derduemmstefliegt.online/lobby/create_lobby', {
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
            let gameType = gameOptions.game_type
            let gameObj = new Game(gameOptions.code, gameOptions.round_timer, players, gameType, player.getId());

            const gameStore = getGameStore();
            gameStore.setGame(gameObj);
            Cookies.set('game', JSON.stringify(getGame().toArray()));
            return true;
        });
}


async function joinLobby(lobbyCode, playerName, savedPlayerData){
    try {
        // get lobby info
        const info = await fetch(`https://api.derduemmstefliegt.online/lobby/get_by_code/${lobbyCode}`);
        const lobbyInfo = await info.json();
        if (lobbyInfo.error) {
            throw new Error(lobbyInfo.error);
        }

        let lobbyState = lobbyInfo.lobby_state;
        if (lobbyState == GameState.WAITING) {
            if (!savedPlayerData) {
                // create player
                await createPlayer(playerName, 0, lobbyInfo.lives_per_player, false);

            }
        }
        
        // TODO



        let gameState = lobbyInfo.game_state;

        return true, gameState;
    } catch(error) {
        console.clear();
        return false;
    }
}

// event handlers

function playerJoined(id, name, avatar_id, lives, self){
    let player = new Player(id, name, avatar_id, lives, self);
    getGame().addPlayer(player);
    console.log("player joined", getGame().players);
}

function playerLeft(id, new_owner_id){
    let leftPlayer = getGame().players.find(player => player.id == id);
    leftPlayer.setPlayerState(PlayerState.DISCONNECTED);
    leftPlayer.setActive(false);
    leftPlayer.setLobbyOwner(false);
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
    for (const [key, value] of Object.entries(data)) {
        
    }
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
    updateLobby,
}