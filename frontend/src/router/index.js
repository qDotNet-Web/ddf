import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
// import CreateLobbyView from '../views/CreateLobbyView.vue'
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
    //   path: '/createLobby',
    //   name: 'createLobby',
    //   component: CreateLobbyView
    // },
    // {
    //   path: '/joinLobby',
    //   name: 'joinLobby',
    //   component: JoinLobbyView
    // },
  ]
})

export default router
