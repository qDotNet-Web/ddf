class Game {
    lobby_id = 0;
    round_started = false;
    set_round_timer = 180; //seconds per round
    round_timer = 180; //current game timer in round in seconds
    round = 1;
    players = [];
    current_player = 0;
    timer_running = false;
    active = false;


    constructor(round_timer, players) {
        this.round_timer = round_timer;
        this.setRoundTimer(round_timer);
        this.players = players;
    }

    getLobbyId() {
        return this.lobby_id;
    }
    getRoundTimer() {
        return this.round_timer;
    }
    getRound() {
        return this.round;
    }
    getPlayers() {
        return this.players;
    }
    getCurrentPlayer() {
        return this.players[this.current_player];
    }

    setLobbyId(lobby_id) {
        this.lobby_id = lobby_id;
    }
    setRoundTimer(round_timer) {
        this.round_timer = round_timer;
    }
    resetRoundTimer() {
        this.round_timer = this.set_round_timer;
    }
    setRound(round) {
        this.round = round;
    }
    setPlayers(players) {
        this.players = players;
    }
    addPlayer(player) {
        this.players.push(player);
    }
    setCurrentPlayer(current_player) {
        this.current_player = current_player;
    }



    startRound() {
        if (!this.round_started) {
            this.round_started = true;
            while (true) {
                if ((this.timer_running) && (this.getRoundTimer() > 0)){
                    this.setRoundTimer(this.getRoundTimer() - 1);
                    setTimeout(1000);
                } else if (this.getRoundTimer() <= 0) {
                    this.endRound();
                }
            } 
        }
    }

    endRound() {
        this.pauseRoundTimer();
        this.round++;
        this.resetRoundTimer();
    }

    endGame() {
        this.pauseRoundTimer();
        // send frontend message that round is over
        for (let i = 0; i < this.players.length; i++) {
            if (this.players[i].getIsOwner()) {
                // Send message to owner that round is over
                return;
            }
        }
    }

    pauseRoundTimer(currentTime){
        this.timer_running = false;
        this.round_timer = currentTime;
    }
    continueRoundTimer(){
        this.timer_running = true;
    }
    
}