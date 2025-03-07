// useFooter.ts
import { ref, onMounted } from 'vue';
import { defaultCondig } from '@config/config';

export default function useFooter() {
  const footerList = ref<FooterData>(defaultCondig?.footer);

  // 初始化
  const initList = () => {
    // 请求数据
    // ...
    // 下方假数据
    const data: FooterData = {
      links: [
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
      ],
      list: [
        {
          label: '问题反馈',
          target: '_blank',
          href: 'https://wj.qq.com/s2/15358157/232e/',
          isRouter: false,
        },
      ],
    };
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
