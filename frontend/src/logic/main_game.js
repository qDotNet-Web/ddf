// ddf = {}
// ddf.game;
// ddf.ws;

// ddf.connectWebSocket = function(lobbyId) {
//     ddf.ws = new WebSocket('ws://localhost:8000/' + lobbyId);
//     ddf.ws.onopen = function() {
//         console.log('Connected to the socket: ' + lobbyId);
//     };
//     ddf.ws.onmessage = function(event) {
//         const message = JSON.parse(event.data);
//         postMessage(message);
//     };
//     ddf.ws.onclose = function() {
//         console.log('Disconnected from the server');
//     };
// }

// ddf.getWebSocket = function() {
//     return ddf.ws;
// }

// export default ddf;

const ws = new WebSocket('ws://localhost:8000/ws');
ws.onopen = function() {
    console.log('Connected to the socket');
}
ws.onmessage = function(event) {
    const message = JSON.parse(event.data);
    console.log(message);
}
ws.onclose = function() {
    console.log('Disconnected from the server');
}

