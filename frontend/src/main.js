
import {createApp} from 'vue'
import {createPinia} from 'pinia'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle'
import './assets/css/animate.css'
import './assets/css/animate.min.css'
import './assets/css/main.css'
import './assets/css/loading.css'
import './assets/css/primevue.css'
import VueSweetalert2 from 'vue-sweetalert2'
import 'sweetalert2/dist/sweetalert2.min.css'
import PrimeVue from 'primevue/config'
import Slider from 'primevue/slider'
import InputText from 'primevue/inputtext'
import FloatLabel from 'primevue/floatlabel'
import SelectButton from 'primevue/selectbutton'
import 'primevue/resources/themes/aura-light-green/theme.css'

import App from './App.vue'
import router from './router'


const app = createApp(App)

app.use(createPinia())
app.use(router)
app.use(VueSweetalert2)
app.use(PrimeVue)
app.component('Slider', Slider)
app.component('InputText', InputText)
app.component('FloatLabel', FloatLabel)
app.component('SelectButton', SelectButton)



app.mount('#app')


