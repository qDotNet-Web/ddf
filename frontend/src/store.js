import { defineStore } from 'pinia';

export const useGameStore = defineStore({
  id: 'game',
  state: () => ({
    gameOptions: null,
  }),
  actions: {
    setGameOptions(options) {
      this.gameOptions = options;
    },
  },
});