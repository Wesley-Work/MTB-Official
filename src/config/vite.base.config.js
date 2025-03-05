import * as path from 'path';
import vue from '@vitejs/plugin-vue';
import vueJsx from '@vitejs/plugin-vue-jsx';

export const resolveConfig = {
  alias: {
    '@': path.resolve(__dirname, '../../'),
    '@src': path.resolve(__dirname, '../src'),
    '@assets': path.resolve(__dirname, '../assets'),
    '@test': path.resolve(__dirname, '../test'),
    '@pages': path.resolve(__dirname, '../pages'),
    '@config': path.resolve(__dirname, '../config'),
    '@components': path.resolve(__dirname, '../components'),
    '@style': path.resolve(__dirname, '../style'),
    '@utils': path.resolve(__dirname, '../utils'),
    '@hooks': path.resolve(__dirname, '../hooks'),
  },
};
export const basePlugin = [
  [
    vue({
      ssr: false,
    }),
    vueJsx(),
  ],
];
