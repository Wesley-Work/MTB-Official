import { defineConfig, searchForWorkspaceRoot } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';
import { resolveConfig, basePlugin } from './src/config/vite.base.config';

export default ({ mode }) => {
  return defineConfig({
    base: '/',
    resolve: resolveConfig,
    server: {
      host: '0.0.0.0',
      port: 14560,
      open: '/',
      https: false,
      fs: {
        allow: [searchForWorkspaceRoot(process.cwd())],
      },
    },
    plugins: [...basePlugin, VitePWA()],
  });
};
