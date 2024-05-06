import { createRouter, createWebHistory } from 'vue-router'
// views
import HomeComponent from '@/components/HomeComponent.vue'
import LegalNoticeComponent from '@/components/LegalNoticeComponent.vue'
import WaitingLobbyComponent from '@/components/WaitingLobbyComponent.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeComponent
    },
    {
      path: '/impressum',
      name: 'impressum',
      component: LegalNoticeComponent
    },
    {
      path: '/waitingLobby',
      name: 'waitingLobby',
      component: WaitingLobbyComponent,
      props: true
    },
  ]
})

export default router
