// useHeader.ts
import { ref, onMounted } from 'vue';
import { defaultConfig } from '@config/config';
export default function useHeader() {
  const headerList = ref<HeaderData>(defaultConfig.header);

  // 初始化
  const initList = () => {
    // 请求数据
    // ...
    // 下方假数据
    const data: HeaderData = [
      {
        label: '诗词大会讲解视频收集',
        target: '_self',
        href: '/',
      },
      {
        label: '德育资料收集',
        target: '_self',
        href: '/',
      },
      {
        label: '共享网盘',
        target: '_self',
        href: 'shareNetdisk',
        isRouter: true,
      },
      {
        label: '服务',
        type: 'list',
        children: [
          {
            label: '文件搜索（仅内部）',
            href: '//10.3.146.12:81/',
            target: '_self',
          },
          {
            label: '速度测试',
            href: 'speedtest',
            isRouter: true,
          },
        ],
      },
      {
        label: '资源',
        type: 'label',
        children: [
          {
            title: '内部共享',
            children: [
              {
                label: '成片库',
                href: '//10.3.146.11',
              },
              {
                label: '媒体库',
                href: '//10.3.146.11',
              },
              {
                label: '德育处资源库',
                href: '//10.3.146.11',
              },
            ],
          },
          {
            title: '外部资料',
            children: [
              {
                label: '对外共享',
                href: '//10.3.146.11',
              },
            ],
          },
        ],
      },
      {
        label: '系统',
        type: 'list',
        children: [
          {
            label: '媒体部OA',
            href: '//10.3.146.12/',
            target: '_blank',
          },
          {
            label: '统一身份认证平台',
            href: '//10.3.146.13/',
            target: '_blank',
          },
          {
            label: '直播系统',
            href: '//10.3.146.125:12800/',
            target: '_blank',
          },
        ],
      },
      {
        label: '加入我们',
        href: '',
        isRouter: true,
      },
      {
        label: '关于媒体部',
        href: 'about',
        isRouter: true,
      },
    ];
    setTimeout(() => {
      headerList.value = data;
      return headerList.value;
    }, 5000);
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
