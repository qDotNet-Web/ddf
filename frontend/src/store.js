import { defineStore } from 'pinia';
import {Game} from './logic/classes/Game.js';
export const getGameStore = defineStore({
  id: 'game',
  state: () => ({
    game: new Game(0, 0, [], 0),
  }),
  actions: {
    setGame(game) {
      this.game = game;
    },
    destroyGame() {
      this.game = null;
    },
    getGame() {
      return this.game;
    }
  },
});
