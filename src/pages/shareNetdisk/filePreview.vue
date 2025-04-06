<template>
  <div>
    <div style="height: 78px"></div>
    <!--header-->
    <MTBHeader :fixed="true" :hidden-toppic="true" :use-custom-data="headerConfig" />
    <!---->
    <div class="filePreview"></div>
    <!---->
    <WesleyFooter />
  </div>
</template>

<script setup lang="tsx">
import { defineComponent } from 'vue';

import MTBHeader from '@components/header';
import WesleyFooter from '@components/wesley_footer';
const headerConfig: HeaderData = [
  {
    label: '返回 文件列表',
    href: '/shareNetdisk',
    isRouter: true,
  },
  {
    label: '问题反馈',
    href: 'https://wj.qq.com/s2/14786781/3fb8/',
    target: '_blank',
  },
  // {
  //   label: 'Github Repository',
  //   href: 'https://github.com/Wesley-Work/MTB-Official/',
  //   target: '_blank',
  // },
];
// const supportList = ['png', 'jpg'];
</script>

<script lang="tsx">
export default defineComponent({
  name: 'MTBShareNetdiskFilePreview',
});
</script>
