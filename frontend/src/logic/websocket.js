let ws;
let wsConnected;
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

async function send(message) {
    await wsConnected;
    ws.send(JSON.stringify(message));
}

function receive(data){
    const {type, msg} = data;
    switch (type) {
        case 'playerJoined':
            playerJoined(msg.id, msg.name, msg.lives);
            return;
        case 'playerLeft':
            playerLeft(msg.id, msg.new_owner_id);
            return;
        case 'startRound':
            startedRound();
            return;
        case 'endRound':
            endedRound();
            return;
        case 'endGame':
            endedGame();
            return;
        case 'votedForPlayer':
            votedForPlayer(msg.votingPlayerId, msg.votedPlayerId);
            return;
        default:
            return;
    }
}