class Player {
    id = 0;
    name = "Schlaubischlumpf";
    lives = 3;
    lobbyOwner = false;
    dead = false;
    active = true;
    constructor(id, name, lives, lobbyOwner) {
        this.id = id;
        this.name = name;
        this.lives = lives;
        this.lobbyOwner = lobbyOwner;
    }


    getId() {
        return this.id;
    }
    getName() {
        return this.name;
    }
    getLives() {
        return this.lives;
    }
    getIsOwner() {
        return this.lobbyOwner;
    }

    setActive(active){
        this.active = active;
        if (!active){
            // get player card and add class inactive
            document.getElementById(this.id).classList.add("inactive");
        }
    }
    setId(id) {
        this.id = id;
    }
    setName(name) {
        this.name = name;
    }
    setLives(lives) {
        this.lives = lives;
    }
    setLobbyOwner(lobbyOwner) {
        this.lobbyOwner = lobbyOwner;
    }


    removeLive() {
        this.lives--;
        if (this.lives <= 0) {
            this.dead = true;
        }
    }
    voteForPlayer(player) {
        // Vote for player using websockets
        if (this.lobbyOwner) {
            let alivePlayers = this.players.filter(player => !player.dead);
            if (alivePlayers.length == 1) {
                Game.endGame();
            }
        }
    }
    answerQuestion(questionId, answer) {
        // Answer question using websockets
    }
}