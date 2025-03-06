// useTheme.ts
import { ref, onMounted } from 'vue';

type ToppicInfo = {
  data: string;
  type: string;
};

export default function useToppic() {
  const toppicInfo = ref<ToppicInfo>();

  // 初始化
  const initList = () => {
    // 请求数据
    // ...
    // 下方假数据
    const data = {
      data: '📢示例顶部消息',
      type: 'static',
    };
    setTimeout(() => {
      toppicInfo.value = data;
      return toppicInfo.value;
    }, 5000);
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
