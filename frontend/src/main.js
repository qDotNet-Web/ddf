
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
import ToastService from 'primevue/toastservice';
import ConfirmDialog from 'primevue/confirmdialog';
import ConfirmationService from 'primevue/confirmationservice';
import Tooltip from 'primevue/tooltip';
import Card from 'primevue/card';
import Dialog from 'primevue/dialog';

import 'primevue/resources/themes/aura-light-green/theme.css'

import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(PrimeVue)
app.use(ToastService)
app.use(ConfirmationService);

app.component('ConfirmDialog', ConfirmDialog);
app.component('Slider', Slider)
app.component('InputText', InputText)
app.component('FloatLabel', FloatLabel)
app.component('SelectButton', SelectButton)
app.component('Card', Card)
app.component('Dialog', Dialog)

app.directive('tooltip', Tooltip);

app.mount('#app')

export function notify(msgtype, header, message, life, closable, sticky) {
    let type = msgtype || 'info';
    let lifeSpan = life || 3000;
    let isClosable = closable || false;
    let isSticky = sticky || false;
    app.config.globalProperties.$toast.add({severity:type, summary:header, detail:message, life:lifeSpan, closable:isClosable, sticky:isSticky});
}

export function showDialog(message, msgtype, callbackAccept, callbackReject) {
    app.config.globalProperties.$confirm.require({
        message: message,
        header: msgtype,
        icon: 'pi pi-exclamation-triangle',
        accept: () => {
            if (callbackAccept) {
                callbackAccept();
            }
        },
        reject: () => {
            if (callbackReject) {
                callbackReject();
            }
        }
    });
}