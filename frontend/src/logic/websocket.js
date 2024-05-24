const { io } = require("socket.io-client");
import {logic} from './main.js';

let socket = null;

export function connectToSocket(){
    socket = io("http://localhost:3000");
    socket.on("connect", () => {
        console.log("connected to server");
    });
    socket.on("lobby", (data) => {
        logic.updateLobby(data);
    });
    socket.on("player_joined", (data) => {
        logic.playerJoined(data.id, data.name, data.avatar_id, data.lives, data.self);
    });
    socket.on("player_left", (data) => {
        logic.playerLeft(data.id, data.new_owner_id);
    });
    socket.on("game_started", () => {
        logic.startedGame();
    });
    socket.on("game_ended", () => {
        logic.endedGame();
    });
    socket.on("round_started", () => {
        logic.startedRound();
    });
    socket.on("round_ended", () => {
        logic.endedRound();
    });
    socket.on("player_voted", (data) => {
        logic.votedForPlayer(data.votingPlayerId, data.votedPlayerId);
    });
}

export function emitEvent(event, data){
    socket.emit(event, data);
}

export function disconnect(){
    socket.disconnect();
    socket = null;
}