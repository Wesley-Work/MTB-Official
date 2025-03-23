<template>
  <div class="content waitHeader">
    <div class="banner mtb-together" :style="{ backgroundImage: `url(${MTBTogether})` }">
      <div class="wrap">
        <h2 class="mtb-together-title title">关 于 媒 体 部</h2>
      </div>
    </div>
    <div class="warpper">
      <div class="item">
        <div class="title">简介</div>
        <div class="text">
          媒体部，成立于2021年，隶属于团委学生会，系顺德中专团委学生会旗下的学生组织，受团委和德育处统一管理，日常由学生组织工作，服务于校。同时也是学生发展、培养学生兴趣爱好、锻炼自身技能的优秀平台。
        </div>
      </div>
      <div class="item">
        <div class="title">媒体部的工作是什么？</div>
        <div class="text">
          与学生会其他部门的工作大相径庭，媒体部的主要工作是：负责学校各类大小活动的拍摄及技术支持，学校对内、外宣传等媒体相关工作。
        </div>
      </div>
      <div class="item">
        <div class="title">如何加入媒体部？</div>
        <div class="text">
          请在<a href="/join-us">此处</a
          >查阅相关资料。媒体部非常欢迎热爱摄影、剪辑、编程的同学！如有意加入，请直接联系我们/校团委。
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { defineComponent } from 'vue';
import MTBTogether from '@assets/MTB_together-2024.png';
</script>

<script lang="tsx">
export default defineComponent({
  name: 'AboutUs',
});
</script>

<style lang="scss">
.content {
  .mtb-together {
    display: flex;
    flex-direction: column;
    justify-content: center;
    background-size: cover !important;
    background-repeat: no-repeat !important;
    background-position: 50% 30%;
    min-height: 365px;
    position: relative;
    text-align: center;
    font-size: 16px;
    line-height: 30px;
    color: #333;
    &::after {
      content: '';
      position: absolute;
      width: 100%;
      height: 100%;
      left: 0;
      top: 0;
      z-index: 1;
      -webkit-backdrop-filter: saturate(60%) blur(4px);
      backdrop-filter: saturate(60%) blur(4px);
      filter: brightness(0.85);
    }
    .wrap {
      color: #fff;
      position: relative;
      z-index: 2;
      text-shadow: 0.125rem 0.125rem 2px black;
      padding: 0 32px;
      .title {
        text-shadow: 3px 5px 2px black;
        font-weight: 700;
        font-size: 60px;
        padding: 0;
        color: #fff;
        top: -15px;
        position: absolute;
        left: 0;
        right: 0;
      }
    }
  }
  .warpper {
    background: #fff;
    color: #000000e6;
    padding: 64px;
    .item + .item {
      margin-top: 24px;
      .title {
        margin: 64px auto 24px;
      }
    }
    .item {
      .title {
        font-size: 32px;
        line-height: 48px;
        letter-spacing: 0.8px;
        margin-bottom: 10px;
        color: #333;
        font-weight: 600;
      }
      .text {
        font-size: 16px;
        line-height: 28px;
        letter-spacing: 0.4px;
        font-weight: 600;
        color: #383838;
        a {
          font-weight: 500;
          color: #646cff;
          text-decoration: inherit;
        }
      }
    }
  }
}
</style>
