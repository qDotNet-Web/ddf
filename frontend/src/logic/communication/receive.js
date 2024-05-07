addEventListener('message', (event) => {
    const { data } = event;
    const { type, payload } = data;
    switch (type) {
        case 'createdLobby':
            game = new Game(payload.round_timer, payload.round, payload.players);
            return;
        case 'joinLobby':
            game = new Game(payload.round_timer, payload.round, payload.players);
            return;
        case 'playerJoined':
            player = new Player(payload.id, payload.name, payload.lives, payload.lobbyOwner);
            game.addPlayer(player);
            return;
        case 'playerLeft':
            player = game.players.find(player => player.id == payload.id);
            player.setActive(false);
            if (payload.new_owner_id) {
                let newOwner = payload.new_owner_id;
                game.players.find(player => player.id == newOwner).setLobbyOwner(true);
            }
            return;
        case 'startRound':
            game.startRound();
            return;
        case 'endRound':
            game.endRound();
            return;
        case 'endGame':
            game.endGame();
            return;
        case 'votedForPlayer':
            return;
        default:
            return;
    }

});