import { createApp } from 'vue';
import './style.scss';
import './style/index.less';
import App from './index.vue';
import router from './router';

createApp(App).use(router).mount('#app');
