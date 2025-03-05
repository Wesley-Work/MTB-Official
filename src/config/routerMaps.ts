import type { RouteRecordRaw } from 'vue-router';

export const RouterConfigMap: RouteRecordRaw[] = [
  {
    name: 'index',
    path: '/',
    component: () => import('@pages/index.vue'),
  },
  {
    name: 'about',
    path: '/about',
    component: () => import('@pages/about.vue'),
  },
];

export const RouterConfig = {
  home: '/',
  maps: RouterConfigMap,
};

export default RouterConfigMap;
