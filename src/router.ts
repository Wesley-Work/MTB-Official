// src/router/index.ts

import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router';
import { RouterConfigMap } from '@config/routerMaps';

const routes: Array<RouteRecordRaw> = RouterConfigMap;

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 在这里添加路由的导航守卫
router.beforeEach((to, from, next) => {
  console.log('Navigating to:', to.path);
  next();
});

export default router;
