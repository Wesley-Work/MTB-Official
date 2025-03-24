import { defineConfig, searchForWorkspaceRoot } from 'vite';
import { VitePWA } from 'vite-plugin-pwa';
import { resolveConfig, basePlugin } from './src/config/vite.base.config';

export default () => {
  return defineConfig({
    base: '/',
    resolve: resolveConfig,
    server: {
      host: '0.0.0.0',
      port: 14560,
      open: '/',
      fs: {
        allow: [searchForWorkspaceRoot(process.cwd())],
      },
    },
    build: {
      outDir: 'dist',
      assetsDir: 'static',
      rollupOptions: {
        output: {
          assetFileNames: (assetInfo) => {
            const reg = /\.mp4$/gi;
            if (assetInfo.names.some((name) => reg.test(name))) {
              return `static/_upload/[name].[ext]`;
            }
            return `static/[name]-[hash].[ext]`;
          },
        },
      },
    },
    plugins: [...basePlugin, VitePWA()],
  });
};
