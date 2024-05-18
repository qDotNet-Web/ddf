let ws;
let wsConnected;
import {logic} from './main.js';
function connectWebSocket(lobbyId){
    ws = new WebSocket('ws://localhost:8000/ws/'+ lobbyId);
    wsConnected = new Promise((resolve) => {
        ws.onopen = () => {
            resolve();
        }
        ws.onmessage = (event) => {
            const {data} = event;
            receive(data);
        }
    });
}

export async function sendWsMessage(action, data) {
    await wsConnected;
    const msg = {action, data};
    ws.send(JSON.stringify(msg));
}

function receive(type, data){
    switch (type) {
        case "updateLobby":
            logic.updateLobby(data);
            return;
        default:
            return;
    }
}