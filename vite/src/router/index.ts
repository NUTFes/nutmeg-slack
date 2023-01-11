import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import ChannelView from '../views/ChannelView.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/about',
    name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () =>
      import(/* webpackChunkName: "about" */ '../views/AboutView.vue'),
  },
  {
    path: '/channels/:channelId',
    name: 'channels',
    component: ChannelView,
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
