import './assets/main.css'
// Remove MDB if you want pure Bootstrap 5, or keep if you need specific MDB components
// import 'mdb-vue-ui-kit/css/mdb.min.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
// Removed bootstrap CSS import since using CDN

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
