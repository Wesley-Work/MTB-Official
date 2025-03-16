import type { RouteRecordRaw } from 'vue-router';
import ShareNetdiskComponent from '@pages/shareNetdisk/component.tsx';
import ConfigPage from '@pages/config.tsx';

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
        name: 'shareNetdisk',
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
    name: 'ConfigPage',
    path: '/config',
    component: ConfigPage,
    children: [
      {
        name: 'header',
        path: 'header',
        component: () => import('@components/header.tsx'),
        meta: {
          noHeader: true,
          noFooter: true,
          test: true,
        },
      },
      {
        name: 'banner',
        path: 'banner',
        component: () => import('@pages/index.vue'),
        meta: {
          noHeader: true,
          noFooter: true,
          test: true,
        },
      },
      {
        name: 'footer',
        path: 'footer',
        component: () => import('@components/footer.tsx'),
        meta: {
          noHeader: true,
          noFooter: true,
          test: true,
        },
      },
    ],
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
