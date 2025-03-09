// useFooter.ts
import { ref, onMounted } from 'vue';
import { defaultConfig } from '@config/config';

export default function useFooter() {
  const footerList = ref<FooterData>(defaultConfig?.footer);

  // 初始化
  const initList = () => {
    // 请求数据
    // ...
    // 下方假数据
    const data: FooterData = {
      links: [
        {
          title: '媒体部',
          children: [
            {
              label: '介绍',
              href: 'about',
              isRouter: true,
            },
            {
              label: '加入我们',
              href: 'join-us',
              isRouter: true,
            },
            {
              label: '<广告位招租>',
              href: 'javascript:void(0)',
            },
          ],
        },
        {
          title: '服务与支持',
          children: [
            {
              label: '共享网盘',
              href: 'shareNetdisk',
              isRouter: true,
            },
            {
              label: '速度测试',
              href: 'speedtest',
              isRouter: true,
            },
            {
              label: 'SSO[统一身份认证平台]',
              href: '//10.3.146.13',
            },
            {
              label: 'OA[媒体部办公系统]',
              href: '//10.3.146.12',
            },
          ],
        },
        {
          title: '媒体账号',
          children: [
            {
              label: '微信公众号',
              href: 'https://mp.weixin.qq.com/mp/profile_ext?action=home&amp;__biz=Mzg2MjYwMDE4MA==&amp;scene=124#wechat_redirect',
              target: '_blank',
            },
            {
              label: 'BiliBili',
              href: 'https://space.bilibili.com/257175059',
              target: '_blank',
            },
            {
              label: '全媒体中心公众号',
              href: 'https://mp.weixin.qq.com/mp/profile_ext?action=home&amp;__biz=MzkxNjI4MDk4MQ==&amp;scene=124#wechat_redirect',
              target: '_blank',
            },
          ],
        },
        {
          title: '友情链接',
          children: [
            {
              label: '影视飓风',
              href: 'https://www.ysjf.com/',
              target: '_blank',
            },
            {
              label: '顺德中专门户网站',
              href: 'http://sdzz.net/',
              target: '_blank',
            },
            {
              label: '顺德区教育局',
              href: 'http://sdedu.net/',
              target: '_blank',
            },
            {
              label: '广东省人民政府',
              href: 'https://www.gd.gov.cn/',
              target: '_blank',
            },
          ],
        },
      ],
      list: [
        {
          label: '问题反馈',
          target: '_blank',
          href: 'https://wj.qq.com/s2/15358157/232e/',
        },
        {
          label: '代码仓库',
          target: '_blank',
          href: 'https://github.com/Wesley-0808/MTB-Official',
        },
        {
          label: '更新日志',
          href: 'CHANGELOG',
          isRouter: true,
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
