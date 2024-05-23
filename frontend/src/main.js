import { createApp } from 'vue'
import App from './App.vue'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import router from './router'
import './reset.css'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

import axios from 'axios';

// 获取 CSRF 令牌
const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
// 添加请求拦截器
axios.interceptors.request.use(config => {
  if (config.method === 'post' || config.method === 'put' || config.method === 'delete') {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  return config;
}, error => {
  return Promise.reject(error);
});

const app = createApp(App)

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(ElementPlus)
app.use(router)
app.mount('#app')
