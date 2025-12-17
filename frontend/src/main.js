import { createApp } from 'vue'
import App from './App.vue'

// Импортируем Tailwind CSS
import './style.css'
import router from './router'

createApp(App).use(router).mount('#app')