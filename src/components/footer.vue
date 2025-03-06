<template>
  <div class="toppic">
    <div></div>
  </div>
</template>

<script setup lang="tsx">
import { defineComponent, ref } from 'vue';

const example = ref({
  data: '',
  type: 'static', //| scroll
  title: '',
});
</script>

<script lang="tsx">
export default defineComponent({
  name: 'Toppic',
});
</script>
