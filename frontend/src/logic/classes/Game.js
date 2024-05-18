import { GameState, GameType } from '@/logic/classes/Enums.js';
export class Game {
    lobby_code = 0;
    round_started = false;
    set_round_timer = 180; //seconds per round
    round_timer = 180; //current game timer in round in seconds
    round = 1;
    players = [];
    current_player_id = 0;
    timer_running = false;
    active = false;
    gameState = GameState.WAITING;
    gameType = GameType.TEXT;


    constructor(lobby_code, round_timer, players, gameType) {
        this.lobby_code = lobby_code;
        this.round_timer = round_timer;
        this.set_round_timer = round_timer;
        this.players = players;
        this.active = true;
        this.gameType = gameType;
    }

    getLobbyCode() {
        return this.lobby_code;
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

    setLobbyCode(lobby_code) {
        this.lobby_code = lobby_code;
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
    setCurrentPlayer(current_player_id) {
        this.current_player_id = current_player_id;
        let player = this.players.find(player => player.id == current_player_id);
        player.setPlayerState(PlayerState.ANSWERING);
    }
    setGameState(gameState) {
        this.gameState = gameState;
    }

    startGame() {
        this.gameState = GameState.RUNNING;
        this.startRound();
    }

    startRound() {
        if (!this.round_started) {
            this.round_started = true;

            let alive = 0;
            for (let i = 0; i < this.players.length; i++) {
                if (this.players[i].getLives() > 0) {
                    alive++;
                }
            }
            if (alive <= 1) {
                
                this.endGame();
            }

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

    toArray() {
        return {
            lobby_code: this.lobby_code,
            round_timer: this.round_timer,
            round: this.round,
            players: this.players,
            gameType: this.gameType,
            gameState: this.gameState,
        }
    }
}