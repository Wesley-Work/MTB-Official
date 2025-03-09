// src/router/index.ts

import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router';
import { RouterConfigMap } from '@config/routerMaps';

const routes: Array<RouteRecordRaw> = RouterConfigMap;

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

// 在这里添加路由的导航守卫
router.beforeEach((to, from, next) => {
  console.info('Navigating to:', to.path, from);
  next();
});

export default router;
