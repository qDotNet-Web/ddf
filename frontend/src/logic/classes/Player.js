import { PlayerState } from "@/logic/classes/Enums.js";
export class Player {
    id = "0";
    player_name = "Schlaubischlumpf";
    lives = 3;
    player_state = PlayerState.WAITING;
    self = false;
    avatar_id = 0;

    constructor(id, name, avatar_id, lives, self) {
        this.id = id;
        this.name = name;
        this.avatar_id = avatar_id;
        this.lives = lives;
        this.self = self;
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
    getAvatarId() {
        return this.avatar_id;
    }
    getIsSelf() {
        return this.self;
    }


    setAvatarId(avatar_id) {
        this.avatar_id = avatar_id;
    }
    setPlayerState(playerState) {
        this.playerState = playerState;
        switch (playerState) {
            // TODO: implement these cases
            case PlayerState.ANSWERING:
                // start timer
                break;
            case PlayerState.VOTING:
                // show voting screen
                break;
            case PlayerState.VOTED:
                // show voted screen
                break;
            case PlayerState.DISCONNECTED:
                // show disconnected screen
                break;
            default:
                break;
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
    removeLive() {
        this.lives--;
        if (this.lives <= 0) {
            this.dead = true;
        }
    }
    voteForPlayer(player) {
        // Vote for player using websockets
    }
    answerQuestion(questionId, answer) {
        // Answer question using websockets
    }

    toArray(){
        return {
            id: this.id,
            name: this.name,
            avatar_id: this.avatar_id,
            lives: this.lives,
            is_alive: this.is_alive,
            playerState: this.playerState,
            self: this.self
        }
    }
}