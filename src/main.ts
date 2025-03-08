import { createApp } from 'vue';
import './style.scss';
import './style/index.less';
import App from './index.vue';
import router from './router';
import Tdesign from 'tdesign-vue-next';
import 'tdesign-vue-next/es/style/index.css';

createApp(App).use(router).use(Tdesign).mount('#app');
