<template>
  <div class="mtb-header">
    <div class="wrap">
      <div class="logo">
        <a style="width: 100%; height: 100%" href="/">
          <img alt="风华正少年" src="@assets/fhzsn_red.png" />
          <img alt="风华正少年" src="@assets/fhzsn_white.png" />
        </a>
      </div>
      <div class="nav">
        <ul class="subnav-ul fl">
          <li v-for="(item, index) in defaultNav" :key="index">
            <a :class="item.extraClass" :target="item.target" :href="`javascript:void(${index})`">
              <span>{{ item.label }}</span>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { defineComponent, ref } from 'vue';
import router from '../router';

const defaultNav = ref([
  {
    extraClass: '',
    label: '首页',
    target: '_blank',
    path: '/',
  },
]);

const clickToPath = (path: string) => {
  router.push(path);
};
</script>

<script lang="tsx">
export default defineComponent({
  name: 'MTBHeader',
});
</script>

<style lang="scss">
.mtb-header {
  display: flex;
  flex-direction: row;
  width: 100%;
  height: 78px;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0) 100%);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 1305;
  transition: all 0.3s ease-out;

  &:hover {
    background: var(--td-bg-color-container) !important;
    .wrap {
      .logo {
        img:first-of-type {
          display: block;
        }
        img {
          display: none;
        }
      }
      .nav {
        .subnav-ul a {
          color: #333;
        }
      }
    }
  }
  .wrap {
    width: 1200px;
    margin: 0px auto;
    font-size: 0;

    .logo {
      position: relative;
      display: inline-block;
      vertical-align: middle;
      width: 190px;
      height: 43.5px;
      img {
        position: absolute;
        top: 0;
        width: 100%;
      }
      img:first-of-type {
        display: none;
      }
    }
    .nav {
      display: inline-block;
      vertical-align: middle;
      width: calc(100% - 280px);
      font-size: 0;
      padding-left: 68px;
      .subnav-ul li {
        display: inline-block;
        vertical-align: top;
        font-size: 14px;
      }
      .subnav-ul a {
        // color: #333;
        color: #fff;
        display: block;
        margin: 0px 25px;
        line-height: 78px;
      }
    }
  }
  img {
    object-fit: cover;
  }
}
</style>
