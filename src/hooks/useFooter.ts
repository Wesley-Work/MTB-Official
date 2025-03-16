// useFooter.ts
import { ref, onMounted } from 'vue';
import { defaultConfig } from '@config/config';
import { useFetch } from '@utils/fetch';

export default function useFooter() {
  const footerList = ref<FooterData>(defaultConfig?.footer);

  // 初始化
  const initList = () => {
    // 请求数据
    useFetch({
      url: '/getFooterList',
      success: (res: any) => {
        const result = JSON.parse(res);
        if (result?.errcode !== 0) {
          console.error({ title: '获Footer失败(Error)', content: `${result?.errcode}:${result?.errmsg}` });
          return;
        }
        const { data } = result;
        // 内容为空时，footer就是默认的
        if (data?.links?.length === 0 || data?.list?.length === 0) {
          const nullData: string[] = [];
          Object.keys(data).forEach((key) => {
            if (data[key]?.length === 0) {
              nullData.push(key);
            }
          });
          console.warn(`footer数据${nullData}内容为空，使用默认配置数据`, result);
          return;
        }
        footerList.value = data;
      },
      error: (desc: string, res: any) => {
        console.error(desc, res);
        console.error({ title: '获Footer失败(Main)', content: `[desc]:${res}` });
      },
    });
  };

  const refreshList = () => {
    return initList();
  };

  onMounted(() => {
    initList();
  });

  return {
    footerList,
    refreshList,
  };
}
