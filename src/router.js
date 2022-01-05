import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home'
import Devices from '@/views/Devices'

Vue.use(VueRouter)

const routes = [
  { path: '/', component: Home, name: "Home" },
  { path: '/devices', component: Devices }
]

const router = new VueRouter({
  routes
})

export default router