import { createWebHistory, createRouter } from 'vue-router'
import Welcome from './components/Welcome'
import ShowDemo from './components/ShowDemo'
import ChooseVideo from './components/ChooseVideo'

const routes = [
   { path: "/", redirect: '/welcome' },
   { path: "/welcome", component: Welcome },
   { path: "/choose_video", component: ChooseVideo },
   { path: "/show_demo", component: ShowDemo },
]

const router = createRouter({
   history: createWebHistory(),
   routes
 })

 export default router