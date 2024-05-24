
import {createApp, provide, inject} from 'vue'
import {createPinia} from 'pinia'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'
import './assets/css/animate.css'
import './assets/css/animate.min.css'
import './assets/css/main.css'
import './assets/css/loading.css'
import './assets/css/primevue.css'
import 'primeicons/primeicons.css'

import PrimeVue from 'primevue/config'
import Slider from 'primevue/slider'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import SelectButton from 'primevue/selectbutton'
import ToastService from 'primevue/toastservice'
import ConfirmDialog from 'primevue/confirmdialog'
import ConfirmationService from 'primevue/confirmationservice'
import Tooltip from 'primevue/tooltip'
import Card from 'primevue/card'
import Dialog from 'primevue/dialog'
import DialogService from 'primevue/dialogservice'
import AnimateOnScroll from 'primevue/animateonscroll'
import BadgeDirective from "primevue/badgedirective"
import Badge from 'primevue/badge'
import Ripple from 'primevue/ripple'
import StyleClass from 'primevue/styleclass'
import FocusTrap from 'primevue/focustrap'



import 'primevue/resources/themes/aura-dark-green/theme.css'

import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService)
app.use(DialogService)

app.directive('tooltip', Tooltip);
app.directive('badge', BadgeDirective);
app.directive('ripple', Ripple);
app.directive('styleclass', StyleClass);
app.directive('focustrap', FocusTrap);
app.directive('animateonscroll', AnimateOnScroll);

app.component('ConfirmDialog', ConfirmDialog)
app.component('Slider', Slider)
app.component('InputText', InputText)
app.component('FloatLabel', FloatLabel)
app.component('SelectButton', SelectButton)
app.component('Card', Card)
app.component('Dialog', Dialog)
app.component('Badge', Badge)

app.directive('tooltip', Tooltip)

app.mount('#app')

export function notify(msgtype, header, message, life, closable, sticky) {
    let type = msgtype || 'info';
    let lifeSpan = life || 3000;
    let isClosable = closable || false;
    let isSticky = sticky || false;
    app.config.globalProperties.$toast.add({severity:type, summary:header, detail:message, life:lifeSpan, closable:isClosable, sticky:isSticky});
}

export function showDialog(header, message) {
    return new Promise((resolve, reject) => {
      app.config.globalProperties.$confirm.require({
        message: message,
        header: header,
        icon: 'pi pi-exclamation-triangle',
        acceptLabel: "Ja",
        rejectLabel: "Nein",
        accept: () => {
          resolve(true);
        },
        reject: () => {
          resolve(false);
        },
        beforeClose: (event) => {
            console.log(event)
        }
      });
    });
}

window.addEventListener('beforeunload', function (e) {
  // Get the current URL path
  const path = window.location.pathname;

  // Check if the path is '/waitingLobby' or '/gameLobby'
  if (path === '/waitingLobby' || path === '/gameLobby') {
    // Cancel the event
    e.preventDefault();
    // Chrome requires returnValue to be set
    e.returnValue = '';
  }
});


import { io } from "socket.io-client";

let socket = null;

function connect(){
    console.log("connecting...")
    socket = io("https://api.derduemmstefliegt.online");
    socket.on('connect', () => {
        console.log('connected to server');
        socket.emit('message', 'Hello, Server!');
    });
}

setTimeout(connect, 1000);