import { createRouter, createWebHistory } from 'vue-router';

const routes = [
  { 
    path: '/:pathMatch(.*)*', 
    name: 'NotFound',
    component: () => import('@/components/NotFound.vue')
  },
  {
    path: '/',
    redirect: '/posts',
  },
  {
    path: '/posts',
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
  history: createWebHistory(),
  routes,
})

export default router;