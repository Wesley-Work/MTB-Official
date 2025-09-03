// useHeader.ts
import { ref, onMounted } from 'vue';
import { defaultConfig } from '@config/config';
import useFetch from '@utils/fetch';
import { HeaderData } from '../types';
export default function useHeader() {
  const headerList = ref<HeaderData>(defaultConfig.header);

  // 初始化
  const initList = () => {
    // 请求数据
    useFetch({
      url: '/getHeaderList',
      success: (res: any) => {
        const result = JSON.parse(res);
        if (result?.errcode !== 0) {
          console.error({ title: '获取Header失败(Error)', content: `${result?.errcode}:${result?.errmsg}` });
          return;
        }
        const { data } = result;
        // 内容为空时，header就是默认的
        if (data.length === 0) {
          console.warn('header数据内容为空，使用默认配置数据', result);
          return;
        }
        headerList.value = data;
      },
      error: (desc: string, res: any) => {
        console.error(desc, res);
        console.error({ title: '获Header失败(Main)', content: `[desc]:${res}` });
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
    headerList,
    refreshList,
  };
}
