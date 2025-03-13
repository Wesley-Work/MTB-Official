import type { RouteRecordRaw } from 'vue-router';
import ShareNetdiskComponent from '@pages/shareNetdisk/component.tsx';

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
  {
    name: 'shareNetdiskComponent',
    path: '/shareNetdisk',
    component: ShareNetdiskComponent,
    children: [
      {
        name: 'index',
        path: '',
        component: () => import('@pages/shareNetdisk/shareNetdisk.vue'),
        meta: {
          noHeader: true,
          noFooter: true,
          extraClass: ['shareNetdisk--index'],
        },
      },
      {
        name: 'filePreview',
        path: 'filePreview',
        component: () => import('@pages/shareNetdisk/filePreview.vue'),
        meta: {
          noHeader: true,
          noFooter: true,
          extraClass: ['shareNetdisk--filePreview'],
        },
      },
    ],
    meta: {
      noHeader: true,
      noFooter: true,
      extraClass: ['shareNetdisk'],
    },
  },
  {
    path: '/:w+',
    redirect: '/',
  },
];

export const RouterConfig = {
  home: '/',
  maps: RouterConfigMap,
};

export default RouterConfigMap;
