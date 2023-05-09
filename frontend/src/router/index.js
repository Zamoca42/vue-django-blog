import { createRouter, createWebHashHistory } from 'vue-router';

const routes = [
  {
    path: '/',
    name: 'Blog',
    component: () => import('@/components/PostList.vue')
  },
  {
    path: '/info',
    name: 'Info',
    component: () => import('@/components/Information.vue')
  },
  {
    path: '/posts/:id',
    name: 'Detail',
    component: () => import('@/components/PostDetail.vue')
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router;