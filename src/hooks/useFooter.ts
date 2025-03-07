// useFooter.ts
import { ref, onMounted } from 'vue';

export default function useFooter() {
  const footerList = ref<FooterData>();

  // 初始化
  const initList = () => {
    // 请求数据
    // ...
    // 下方假数据
    const data: FooterData = [
      {
        title: '底部内容1',
        children: [
          {
            label: '底部内容1-1',
            target: '_blank',
            href: 'https://www.baidu.com',
            isRouter: false,
          },
        ],
      },
    ];
    setTimeout(() => {
      footerList.value = data;
      return footerList.value;
    }, 5000);
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
