<template>
  <MTBHeader v-if="!showHeader"></MTBHeader>
  <!-- <div class="waitHeader"></div> -->
  <router-view :class="route.meta.extraClass"></router-view>
  <MTBFooter v-if="!showFooter"></MTBFooter>
</template>
<script setup lang="tsx">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import MTBHeader from '@components/header.tsx';
import MTBFooter from '@components/footer.tsx';
const route = useRoute();

const showHeader = computed(() => route.meta.noHeader === true);
const showFooter = computed(() => route.meta.noFooter === true);
</script>

<style lang="scss">
.waitHeader {
  margin-top: 78px;
}
</style>
