// src/router/index.ts
import { createRouter, createWebHashHistory, type RouteRecordRaw } from 'vue-router';
import { RouterConfigMap } from '@config/routerMaps';
import NProgress from 'nprogress';

const routes: Array<RouteRecordRaw> = RouterConfigMap;

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  console.info(
    `%c Navigating to: %c ${to.path} %c`,
    `background: rgb(49, 74, 197);border:1px solid rgb(49, 74, 197); padding: 1px; border-radius: 4px 0 0 4px; color: #fff;`,
    `border:1px solid rgb(49, 74, 197); padding: 1px; border-radius: 0 4px 4px 0; color: rgb(49, 74, 197);`,
    'background:transparent',
    from,
  );
  // 进度条
  if (typeof NProgress !== 'undefined') {
    // eslint-disable-next-line no-undef
    NProgress.configure({
      speed: 500,
      trickleSpeed: 50,
    });
    NProgress.start();
  }
  next();
});

router.afterEach(() => {
  if (typeof NProgress !== 'undefined') {
    // eslint-disable-next-line no-undef
    NProgress.done();
  }
});

export default router;
