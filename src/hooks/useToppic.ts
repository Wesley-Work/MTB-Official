// useToppic.ts
import { ref, onMounted } from 'vue';
import { useFetch } from '@utils/fetch';

export default function useToppic() {
  const toppicInfo = ref<ToppicInfo>();

  // 初始化
  const initList = () => {
    // 请求数据
    useFetch({
      url: '/getToppic',
      success: (res: any) => {
        const result = JSON.parse(res);
        if (result?.errcode !== 0) {
          console.error({ title: '获Toppic失败(Error)', content: `${result?.errcode}:${result?.errmsg}` });
          return;
        }
        const { data } = result;
        // 内容为空时，toppic就是默认的
        if (Object.keys(data).length === 0) {
          console.warn('toppic数据内容为空，使用默认配置数据', result);
          return;
        }
        toppicInfo.value = data;
      },
      error: (desc: string, res: any) => {
        console.error(desc, res);
        console.error({ title: '获Toppic失败(Main)', content: `[desc]:${res}` });
      },
    });
  };

  const refreshToppic = () => {
    return initList();
  };

  onMounted(() => {
    initList();
  });

  return {
    toppicInfo,
    refreshToppic,
  };
}
