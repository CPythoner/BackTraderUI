import { createRouter, createWebHistory } from 'vue-router'
import Login from "@/components/LoginPage.vue"
import HomePage from '@/views/HomePage.vue';
import ResultPage from '@/views/ResultPage.vue';
import StockData from "@/views/StockData.vue";

const routes = [
    { path: '/', component: HomePage, name: 'home' },
    { path: '/home', component: HomePage, name: 'home' },
    { path: '/login', component: Login },
    {
      path: '/result',
      name: 'result',
      component: ResultPage
    },
    {
      path: '/stock-data',
      name: 'stock-data',
      component: StockData
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

export default router