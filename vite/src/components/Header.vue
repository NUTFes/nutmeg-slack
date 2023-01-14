<script lang="ts" setup>
  import { computed } from 'vue'
  import { useStore } from 'vuex'

  const store = useStore()
  const channelName = computed(() => store.getters.channelName)
</script>

<template>
  <div class="header">
    <div class="text-h4">{{ channelName }}</div>
  </div>
</template>

<style>
  .header {
    position: fixed;
    top: 0;
    right: 0;
    z-index: 1;
    width: 100%;
    height: 50px;
    padding-left: 25%;
    background-color: white;
    border-bottom: 2px solid #a3a0a0;
  }
</style>
