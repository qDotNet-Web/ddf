ws = ddf.getWebSocket();

function send(message) {
    ws.send(JSON.stringify(message));
}