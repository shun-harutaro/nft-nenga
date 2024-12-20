import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from "pinia";
import App from './App.vue'
import router from "./router"
import axios from 'axios';

axios.defaults.withCredentials = true;
axios.defaults.baseURL = import.meta.env.VITE_API_URL;

const pinia  = createPinia()
createApp(App)
  .use(router)
  .use(pinia)
  .mount("#app")
