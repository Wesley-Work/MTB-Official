<template>
  <div class="content waitHeader">
    <div
      class="banner mtb-together"
      :style="{ backgroundImage: `url(${MTBTogether})` }"
    >
      <div class="wrap">
        <h2 class="mtb-together-title title">加 入 我 们</h2>
      </div>
    </div>
    <div class="warpper">
      <div class="item">
        <div class="title" style="font-weight: 600">纳新方式</div>
        <div class="text" style="font-weight: 500; padding-left: 20px">
          目前，媒体部招新由团委统一安排，学生会各个部门会一起招新。<strong>但是</strong>如果你<span
            style="text-decoration: underline"
            >技术上有特长或对技术相关内容感兴趣</span
          >（技术内容譬如：音响、灯光、编程、电脑硬/软件等）欢迎随时到媒体部打扰我们！（技术组特招渠道，198-3287-9110或188-2329-1731[微信同号]）
          <br />
          此外，如果你非常有拍摄的基础，同时非常想加入我们，我们也欢迎你~~
        </div>
      </div>
      <div class="item">
        <div class="title" style="font-weight: 600; margin: 16px 0 8px">
          纳新对象
        </div>
        <div class="text" style="font-weight: 500; padding-left: 20px">
          全校非毕业级班级 学生
        </div>
      </div>
      <div class="tt">FAQ</div>
      <div v-for="(item, index) in faqList" :key="index" class="item">
        <div class="title">Q: {{ item.q }}</div>
        <div class="text">A: {{ item.a }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { defineComponent, ref } from "vue";
import MTBTogether from "@assets/MTB-together-wywh.png";
const faqList = ref([
  {
    q: "为什么要加入媒体部？",
    a: "在这里，你能学到摄影技术，增长个人见识，培养兴趣爱好，认识志同道合的人。",
  },
  {
    q: "媒体部内的分组是怎样的？",
    a: "部门内分为：照片组、视频组、海报组、技术组。其对应的工作内容为：照片[无人机]、视频[特效]、海报、技术支持。在此基础上支持跨组作业。",
  },
  {
    q: "媒体部和别的部门有什么不同？",
    a: '媒体部与学生会其他部门的工作大相径庭，不像常规管理部门一样，每天都要"上班"，但在一些特定时期需要参与任务，其次，在遵守部门规则的前提下可以带电脑回校工作。',
  },
  {
    q: "部门待遇？",
    a: "团委学生会是以“引领、奉献、服务、发展”为宗旨，在学生会的工作中，没有待遇的好坏之分。",
  },
  {
    q: "媒体部有/提供哪些设备？",
    a: "部门内现有相机若干、无人机若干、手持拍摄设备以及固定工作电脑等。具体的配置可咨询部门人员。",
  },
]);
</script>

<script lang="tsx">
export default defineComponent({
  name: "JoinUs",
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
      content: "";
      position: absolute;
      width: 100%;
      height: 100%;
      left: 0;
      top: 0;
      z-index: 1;
      -webkit-backdrop-filter: saturate(60%) blur(4px);
      backdrop-filter: saturate(60%) blur(6px);
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
    .tt {
      font-size: 32px;
      line-height: 48px;
      padding: 18px 0;
      font-weight: 600;
      margin-top: 24px;
    }
    .item + .item {
      margin-top: 24px;
      .title {
        margin: 58px auto 14px;
      }
    }
    .item {
      .title {
        font-size: 32px;
        line-height: 48px;
        letter-spacing: 0.8px;
        margin-bottom: 10px;
        color: #333;
      }
      .text {
        font-size: 16px;
        line-height: 28px;
        letter-spacing: 0.4px;
        font-weight: 600;
        color: #383838;
      }
    }
  }
}
</style>
