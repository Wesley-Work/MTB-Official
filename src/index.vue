<template>
  <MTBHeader></MTBHeader>
  <router-view class="waitHeader"></router-view>
  <MTBFooter></MTBFooter>
</template>
<script setup lang="tsx">
import MTBHeader from '@components/header.vue';
import MTBFooter from '@components/footer.vue';
</script>

<style lang="scss">
// .waitHeader {
//   margin-top: 78px;
// }
</style>
