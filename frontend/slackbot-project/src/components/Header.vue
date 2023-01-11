<script lang="ts" setup>
import { computed } from "vue";
import { useStore } from "vuex";

const store = useStore();
const channelName = computed(() => store.getters.channelName);
</script>

<template>
  <div class="header">
    <div class="text-h4">{{ channelName }}</div>
  </div>
</template>

<style>
  .header {
  background-color: white;
  width: 100%;
  height: 50px;
  position: fixed;
  top: 0;
  right: 0;
  border-bottom: 2px solid #a3a0a0;;
  padding-left: 25%;
  z-index: 1;
}
</style>
