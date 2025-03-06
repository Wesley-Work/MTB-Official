<template>
  <MTBHeader></MTBHeader>
  <router-view class="waitHeader"></router-view>
</template>
<script setup lang="tsx">
import MTBHeader from '@components/header.vue';
</script>

<style lang="scss">
.waitHeader {
  margin-top: 78px;
}
</style>
