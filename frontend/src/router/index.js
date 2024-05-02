import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { join } from 'path'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    // {
    //   path: '/joinLobby',
    //   name: 'joinLobby',
    //   component: JoinLobbyView
    // },
    // {
    //   path: '/createLobby',
    //   name: 'createLobby',
    //   component: CreateLobbyView
    // }
  ]
})

export default router
