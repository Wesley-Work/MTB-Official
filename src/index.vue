<template>
  <MTBHeader></MTBHeader>
  <router-view class="waitHeader"></router-view>
  <MTBFooter></MTBFooter>
</template>
<script setup lang="tsx">
import MTBHeader from '@components/header.tsx';
import MTBFooter from '@components/footer.tsx';
</script>

<style lang="scss">
// .waitHeader {
//   margin-top: 78px;
// }
</style>
