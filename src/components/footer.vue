<template>
  <div class="footer">
    <div class="wrap">
      <div class="pc" style="justify-content: center">
        <div v-for="(item, index) in footerConfig?.links" :key="index" class="Footer-subfooterdiv">
          <h2>{{ item?.title ?? `项目${index + 1}` }}</h2>
          <div class="Footer-subtag">
            <a
              v-for="(aItem, aIndex) in item.children"
              :key="aIndex"
              :target="!!aItem.isRouter ? '' : aItem.target"
              :href="aItem.href"
              >{{ aItem?.label ?? `项目${aIndex + 1}` }}</a
            >
          </div>
        </div>
        <div class="Footer-subfooterdiv find-us">
          <h2>找到我们</h2>
          <div class="clearfix">
            <h3>办公楼 一楼 德育处主任室 旁</h3>
            <p>工作时间：08:00～21:30</p>
          </div>
        </div>
      </div>
      <div class="mobile" style="justify-content: center">
        <div id="FooterItem--0" class="Footer-subfooterdiv">
          <div class="arrow">
            <h2>媒体部</h2>
            <svg
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              width="24px"
              height="24px"
              viewBox="0,0,300,250"
            >
              <g
                fill="#ffffff"
                fill-rule="nonzero"
                stroke="none"
                stroke-width="1"
                stroke-linecap="butt"
                stroke-linejoin="miter"
                stroke-miterlimit="10"
                stroke-dasharray=""
                stroke-dashoffset="0"
                font-family="none"
                font-weight="none"
                font-size="none"
                text-anchor="none"
                style="mix-blend-mode: normal"
              >
                <g transform="scale(8.53333,8.53333)">
                  <path
                    d="M17,3h2c0.386,0 0.738,0.223 0.904,0.572c0.166,0.349 0.115,0.762 -0.13,1.062l-8.482,10.366l8.482,10.367c0.245,0.299 0.295,0.712 0.13,1.062c-0.165,0.35 -0.518,0.571 -0.904,0.571h-2c-0.3,0 -0.584,-0.135 -0.774,-0.367l-9,-11c-0.301,-0.369 -0.301,-0.898 0,-1.267l9,-11c0.19,-0.231 0.474,-0.366 0.774,-0.366z"
                  ></path>
                </g>
              </g>
            </svg>
          </div>
          <div class="Footer-subtag">
            <a target="_self" href="http://10.3.146.11/about-MTB">介绍</a
            ><a target="_self" href="http://10.3.146.11/join-us">加入我们</a
            ><a target="_self" href="javascript:void(0)">&lt;广告位招租&gt;</a>
          </div>
        </div>
        <div class="Footer-subfooterdiv find-us">
          <div class="arrow">
            <h2>服务与支持</h2>
            <svg
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              width="24px"
              height="24px"
              viewBox="0,0,300,250"
            >
              <g
                fill="#ffffff"
                fill-rule="nonzero"
                stroke="none"
                stroke-width="1"
                stroke-linecap="butt"
                stroke-linejoin="miter"
                stroke-miterlimit="10"
                stroke-dasharray=""
                stroke-dashoffset="0"
                font-family="none"
                font-weight="none"
                font-size="none"
                text-anchor="none"
                style="mix-blend-mode: normal"
              >
                <g transform="scale(8.53333,8.53333)">
                  <path
                    d="M17,3h2c0.386,0 0.738,0.223 0.904,0.572c0.166,0.349 0.115,0.762 -0.13,1.062l-8.482,10.366l8.482,10.367c0.245,0.299 0.295,0.712 0.13,1.062c-0.165,0.35 -0.518,0.571 -0.904,0.571h-2c-0.3,0 -0.584,-0.135 -0.774,-0.367l-9,-11c-0.301,-0.369 -0.301,-0.898 0,-1.267l9,-11c0.19,-0.231 0.474,-0.366 0.774,-0.366z"
                  ></path>
                </g>
              </g>
            </svg>
          </div>
          <div class="clearfix">
            <a target="_self" href="http://10.3.146.11/share-network-disk">共享网盘</a
            ><a target="_self" href="http://10.3.146.13/">统一认证系统</a
            ><a target="_self" href="http://10.3.146.12/">媒体部OA</a>
          </div>
        </div>
        <div id="FooterItem--2" class="Footer-subfooterdiv">
          <div class="arrow">
            <h2>媒体账号</h2>
            <svg
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              width="24px"
              height="24px"
              viewBox="0,0,300,250"
            >
              <g
                fill="#ffffff"
                fill-rule="nonzero"
                stroke="none"
                stroke-width="1"
                stroke-linecap="butt"
                stroke-linejoin="miter"
                stroke-miterlimit="10"
                stroke-dasharray=""
                stroke-dashoffset="0"
                font-family="none"
                font-weight="none"
                font-size="none"
                text-anchor="none"
                style="mix-blend-mode: normal"
              >
                <g transform="scale(8.53333,8.53333)">
                  <path
                    d="M17,3h2c0.386,0 0.738,0.223 0.904,0.572c0.166,0.349 0.115,0.762 -0.13,1.062l-8.482,10.366l8.482,10.367c0.245,0.299 0.295,0.712 0.13,1.062c-0.165,0.35 -0.518,0.571 -0.904,0.571h-2c-0.3,0 -0.584,-0.135 -0.774,-0.367l-9,-11c-0.301,-0.369 -0.301,-0.898 0,-1.267l9,-11c0.19,-0.231 0.474,-0.366 0.774,-0.366z"
                  ></path>
                </g>
              </g>
            </svg>
          </div>
          <div class="Footer-subtag">
            <a
              target="_self"
              href="https://mp.weixin.qq.com/mp/profile_ext?action=home&amp;__biz=Mzg2MjYwMDE4MA==&amp;scene=124#wechat_redirect"
              >微信公众号</a
            ><a target="_self" href="https://space.bilibili.com/257175059">Bilibili</a
            ><a
              target="_self"
              href="https://mp.weixin.qq.com/mp/profile_ext?action=home&amp;__biz=MzkxNjI4MDk4MQ==&amp;scene=124#wechat_redirect"
              >全媒体中心公众号</a
            >
          </div>
        </div>
        <div id="FooterItem--3" class="Footer-subfooterdiv">
          <div class="arrow">
            <h2>友情链接</h2>
            <svg
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              xmlns:xlink="http://www.w3.org/1999/xlink"
              width="24px"
              height="24px"
              viewBox="0,0,300,250"
            >
              <g
                fill="#ffffff"
                fill-rule="nonzero"
                stroke="none"
                stroke-width="1"
                stroke-linecap="butt"
                stroke-linejoin="miter"
                stroke-miterlimit="10"
                stroke-dasharray=""
                stroke-dashoffset="0"
                font-family="none"
                font-weight="none"
                font-size="none"
                text-anchor="none"
                style="mix-blend-mode: normal"
              >
                <g transform="scale(8.53333,8.53333)">
                  <path
                    d="M17,3h2c0.386,0 0.738,0.223 0.904,0.572c0.166,0.349 0.115,0.762 -0.13,1.062l-8.482,10.366l8.482,10.367c0.245,0.299 0.295,0.712 0.13,1.062c-0.165,0.35 -0.518,0.571 -0.904,0.571h-2c-0.3,0 -0.584,-0.135 -0.774,-0.367l-9,-11c-0.301,-0.369 -0.301,-0.898 0,-1.267l9,-11c0.19,-0.231 0.474,-0.366 0.774,-0.366z"
                  ></path>
                </g>
              </g>
            </svg>
          </div>
          <div class="Footer-subtag">
            <a target="_self" href="https://www.ysjf.com/">影视飓风</a
            ><a target="_self" href="http://sdzz.net/">顺德中专门户网站</a
            ><a target="_self" href="http://sdedu.net/">顺德区教育局</a>
          </div>
        </div>
        <div class="Footer-subfooterdiv find-us">
          <h2>找到我们↓</h2>
          <div class="clearfix">
            <h3>办公楼 一楼 德育处主任室 旁</h3>
            <p>工作时间：08:00～21:30</p>
          </div>
        </div>
      </div>
      <div class="Footer-bootom">
        <a href="javascript:void(0)"><img alt="" src="@src/assets/fhzsn_white.png" width="200" /></a>
        <div class="links">
          <a
            v-for="(item, index) in footerConfig?.list"
            :key="index"
            :target="!!item.isRouter ? '' : item.target"
            :href="item.href"
            >{{ item.label }}</a
          >
        </div>
      </div>
      <div class="copyright">
        <div class="items">
          <span style="display: flex; gap: 4px; align-items: center; flex-wrap: nowrap; white-space: nowrap"
            >Copyright © 2025 <img src="@src/assets/source/wesley.svg" style="width: 48px" /> &amp; MTB. All Rights
            Reserved.</span
          >
          <div class="becareful">
            <span>顺德区中等专业学校、顺德区技工学校 团委学生会</span><span>顺德中专影视创作基地：媒体部</span
            ><span>顺德中专 全媒体中心</span>
          </div>
          <span style="text-wrap: nowrap; display: flex; flex-direction: row; gap: 4px">
            城轨222 文俊亮 提供服务与支持
            <span class="PackageVersion">v{{ version }}</span>
          </span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { computed, defineComponent, ref } from 'vue';
import { version } from '@/package.json';
import useFooter from '../hooks/useFooter';

const { footerList, refreshList } = useFooter();

const footerConfig = computed(() => footerList.value as FooterData);

const example = ref({
  data: '',
  type: 'static', //| scroll
  title: '',
});
</script>

<script lang="tsx">
export default defineComponent({
  name: 'Footer',
});
</script>

<style>
:root {
  --footer-bg-color-primary: #1c436e;
}
/* #18304b */
:root[theme-mode='dark'] {
  --footer-bg-color-primary: #112f52;
}
.footer {
  position: absolute;
  left: 0;
  font-size: 14px;
  line-height: 36px;
  color: #fff9;
  background-color: var(--footer-bg-color-primary);
  padding-top: 70px;
  padding-bottom: 30px;
  width: 100%;
  z-index: 501;

  .wrap {
    height: 100%;
    width: 78%;
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    text-align: left;
    .pc {
      display: flex;
      .Footer-subfooterdiv {
        float: left;
        width: 16.6%;
        h2 {
          font-size: 16px;
          color: #fff;
          margin-bottom: 15px;
          font-weight: 700;
        }
        a {
          color: #fff9;
          display: block;
          transition: all 0.3s ease-out;
          &:hover {
            color: #1d70f2;
            padding-left: 2px;
          }
        }
      }
    }
    .mobile {
      padding: 0px 3.0313rem;
      display: none;
      flex-direction: column;
    }

    .Footer-bootom {
      border-bottom: 1px solid rgba(248, 248, 248, 0.1);
      font-size: 16px;
      margin-top: 60px;
      padding-bottom: 12px;
      display: flex;
      flex-direction: row;
      a {
        color: #fff9;
        margin-right: 25px;
        transition: all 0.3s ease-out;
        display: flex;
        align-items: center;
        &:hover {
          color: #1d70f2 !important;
        }
      }
      .links {
        display: flex;
        flex-direction: row;
      }
    }
    .copyright {
      margin-top: 6px;
      font-variant-numeric: normal;
      font-variant-east-asian: normal;
      font-variant-alternates: normal;
      font-kerning: auto;
      font-optical-sizing: auto;
      font-feature-settings: normal;
      font-variation-settings: normal;
      font-variant-position: normal;
      font-weight: 400;
      font-stretch: normal;
      font-size: 13px;
      line-height: normal;
      font-family: Helvetica Neue;
      .items {
        color: #adb3bc;
        display: flex;
        gap: 14px;
      }
      .becareful {
        display: flex;
        flex-wrap: wrap;
        gap: 0px 12px;
      }
      .PackageVersion {
        color: #fff9;
        margin-right: 25px;
        display: flex;
        align-items: center;
        font-size: 11px;
      }
    }
  }
}
</style>
