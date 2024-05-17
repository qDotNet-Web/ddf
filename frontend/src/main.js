
import {createApp, provide, inject} from 'vue'
import {createPinia} from 'pinia'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'
import './assets/css/animate.css'
import './assets/css/animate.min.css'
import './assets/css/main.css'
import './assets/css/loading.css'
import './assets/css/primevue.css'

import PrimeVue from 'primevue/config'
import Slider from 'primevue/slider'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import SelectButton from 'primevue/selectbutton'
import ToastService from 'primevue/toastservice';
import ConfirmDialog from 'primevue/confirmdialog';
import ConfirmationService from 'primevue/confirmationservice';

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

app.mount('#app')

export function notify(message, header, msgtype, life, closable, sticky) {
    let type = msgtype || 'info';
    let lifeSpan = life || 3000;
    let isClosable = closable || false;
    let isSticky = sticky || false;
    app.config.globalProperties.$toast.add({severity:type, summary:header, detail:message, life:lifeSpan, closable:isClosable, sticky:isSticky});
}

export function showDialog(message, msgtype) {
    app.config.globalProperties.$confirm.require({
        message: message,
        header: msgtype,
        icon: 'pi pi-exclamation-triangle',
        accept: () => {
            // logic to execute on confirmation
        },
        reject: () => {
            // logic to execute on rejection
        }
    });
}