// useTheme.ts
import { ref, onMounted, onUnmounted } from 'vue';
import { config } from '@src/config';
type ThemeMode = 'light' | 'dark';

export default function useTheme() {
  const theme = ref<ThemeMode>('light');
  const htmlEl = document.documentElement;

  // 初始化
  const initTheme = () => {
    const savedTheme = localStorage.getItem('theme') as ThemeMode;
    const systemIsDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    theme.value = savedTheme || (systemIsDark ? 'dark' : 'light');
    htmlEl.setAttribute('theme-mode', theme.value);
  };

  // 切换
  const toggleTheme = () => {
    theme.value = theme.value === 'dark' ? 'light' : 'dark';
    config.useViewTransitionToggleTheme ? document.startViewTransition(() => tt()) : tt();
  };

  const tt = () => {
    htmlEl.setAttribute('theme-mode', theme.value);
    localStorage.setItem('theme', theme.value);
  };

  // 监听系统主题变化
  // eslint-disable-next-line no-unused-vars
  const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
  // eslint-disable-next-line no-unused-vars
  const handleSystemThemeChange = (e: MediaQueryListEvent) => {
    if (!localStorage.getItem('theme')) {
      theme.value = e.matches ? 'dark' : 'light';
      htmlEl.setAttribute('theme-mode', theme.value);
    }
  };

  onMounted(() => {
    initTheme();
    // mediaQuery.addEventListener('change', handleSystemThemeChange);
  });

  onUnmounted(() => {
    // mediaQuery.removeEventListener('change', handleSystemThemeChange);
  });

  return {
    theme,
    toggleTheme,
    setTheme: (mode: ThemeMode) => {
      theme.value = mode;
      htmlEl.setAttribute('theme-mode', mode);
      localStorage.setItem('theme', mode);
    },
  };
}
