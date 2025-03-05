import { resolveConfig, basePlugin } from '../config/vite.base.config';

const paths = resolve(__dirname, '../pages')

// 单元测试相关配置
const testConfig = {
  include: [resolve(paths, '__tests__/*.{test,spec}.{js,mjs,cjs,ts,mts,cts,jsx,tsx}')],
  globals: true,
  environment: 'jsdom',
  testTimeout: 5000,
  setupFiles: '',
  transformMode: {
    web: [/\.[jt]sx$/],
  },
  coverage: {
    reporter: ['text', 'json', 'html'],
    allowExternal: true,
    include: [paths],
  },
};

export default {
  resolve: resolveConfig,
  plugins: basePlugin,
  test: testConfig,
};
