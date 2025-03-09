// src/components/toppic.tsx
import { defineComponent, computed } from 'vue';
import useToppic from '@hooks/useToppic';
import '@style/toppic.scss';

export default defineComponent({
  name: 'Toppic',
  setup() {
    const { toppicInfo } = useToppic();
    const example = computed(() => toppicInfo.value);

    return () => (
      <div class={['toppic', example.value && 'has-toppic'].join(' ')}>
        <div class={['scrollToppic', example.value?.type === 'scroll' ? 'scrollToppic' : ''].join(' ')}>
          <span class="content" style={{ cursor: 'pointer' }} v-html={example.value?.data || ''}></span>
        </div>
      </div>
    );
  },
});
