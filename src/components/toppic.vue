<template>
  <div class="toppic" :class="{ 'has-toppic': !!example }">
    <div :class="{ scrollToppic: example?.type === 'scroll' }">
      <span class="content">{{ example?.data }}</span>
    </div>
  </div>
</template>

<script setup lang="tsx">
import { computed, defineComponent, ref } from 'vue';
import useToppic from '@hooks/useToppic';

const { toppicInfo } = useToppic();

const example = computed(() => {
  return toppicInfo.value;
});
</script>

<script lang="tsx">
export default defineComponent({
  name: 'Toppic',
});
</script>

<style lang="scss">
.toppic {
  width: 100%;
  height: 0px;
  padding: 0px;
  box-sizing: border-box;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  background-color: var(--td-brand-color);
  transition: all 0.28s ease-in-out;
  &.has-toppic {
    height: 32px;
    padding: 8px 24px;
  }
  .content {
    cursor: pointer;
    color: rgba(255, 255, 255, 0.9);
    transition: 0.2s;
  }
}
</style>
