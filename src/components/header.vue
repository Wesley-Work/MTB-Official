<template>
  <div class="mtb-header">
    <div class="wrap">
      <a class="am-logo" href="/"
        ><img alt="" src="@assets/fhzsn_red.png" /><img alt="" src="@assets/fhzsn_white.png"
      /></a>
      <div class="nav">
        <ul class="subnav-ul fl">
          <li>
            <a class="" target="_self" href="/product/hardware"><span>产品系列</span></a>
            <div class="nav-down" hidden="" style="display: none">
              <div class="nav-tab"><a class="active">教学硬件</a><a>教学应用</a><a>管理平台</a></div>
            </div>
          </li>
          <li>
            <a class="" target="_self" href="/home"><span>解决方案</span></a>
          </li>
          <li>
            <a class="" target="_self" href="/support"><span>服务支持</span></a>
          </li>
          <li>
            <a class="" target="_self" href="/home"><span>教师发展</span></a>
          </li>
          <li>
            <a class="" target="_self" href="/home"><span>关于希沃</span></a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script lang="tsx">
import { defineComponent } from 'vue';
export default defineComponent({
  name: 'MTBHeader',
});
</script>

<style lang="scss">
.mtb-header {
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.3) 0%, rgba(0, 0, 0, 0) 100%);
  .wrap {
    width: 1200px;
    margin: 0px auto;

    .am-logo {
      margin-top: 26px;
      float: left;
      width: 180px;
      height: 26px;
      img {
        width: 100%;
      }
    }
    .nav {
      float: right;
      min-width: 70%;
      font-size: 0;
    }
  }
  img {
    object-fit: cover;
  }
}
</style>
