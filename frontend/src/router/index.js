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


router.afterEach(() => {
  console.log("Wird Aufgerufen!");

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      if (mutation.addedNodes) {
        mutation.addedNodes.forEach((node) => {
          // Überprüfe, ob es sich um ein Element handelt und die richtige Klasse hat
          if (node.nodeType === 1 && node.classList.contains('fr-animate')) {
            node.classList.add('fr-animate-init');
          }
        });
      }
    });
  });

  // Konfiguration des Observers: beobachte nur das Hinzufügen von Elementen
  const config = { childList: true, subtree: true };

  // Starte die Beobachtung des Body für die Konfiguration
  observer.observe(document.body, config);

  // Optional: Beobachtung nach einer gewissen Zeit stoppen, um Ressourcen zu schonen
  setTimeout(() => {
    observer.disconnect();
  }, 5000); // Stoppe nach 5 Sekunden
});

export default router
