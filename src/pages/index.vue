<template>
  <div class="container">
    <MTBHeader></MTBHeader>
    <div>index.vue</div>
  </div>
</template>

<script setup lang="tsx">
import { onMounted } from 'vue';
import { config } from '@src/config';
import MTBHeader from '@components/header.vue';

onMounted(() => {
  // 招新Console
  if (config.RecruitConsole) {
    console.group(
      '%c恭喜你发现了媒体部技术组招新特别渠道！ (互联网班级、有编程经验 优先[不包括编程猫等软件])',
      'color: #1890ff',
    );
    console.info(
      '%c本站使用 Vite6+Vue3(TypeScript); 后端使用Python开发  本站使用Github作为代码管理 https://github.com/Wesley-0808/MTB-Official',
      'color: #1890ff',
    );
    console.info(
      '%c媒体部技术组长期招新！！！！如果你也对网络、编程有兴趣，想加入媒体部技术组，欢迎到我们部门找部长！！！（部门位置：办公楼一楼德育处 隔壁办公室）',
      'color: #07c160',
    );
    console.info('%c技术组很好玩的~~', 'color: rgb(255,152,0)');
    console.groupEnd();
    console.group('%c【技术组简介】', 'color: rgb(255,152,0)');
    console.info('%c1. 维护部门内网络、服务器正常运行，必要时需排查故障、解决问题。', 'font-weight: bold');
    console.info('%c2. 协调部门内工作，保障其他组正常工作。', 'font-weight: bold');
    console.info(
      '%c3. 校园活动后台，包含：灯光、音响、直播、场控等内容，保障活动正常进行，给予技术支持。',
      'font-weight: bold',
    );
    console.info('%c...', 'font-weight: bold');
    console.groupEnd();
  }
});
</script>

<style lang="scss">
body {
  background: #07c160;
}
</style>
