<script lang="ts" setup>
  import { computed } from 'vue'
  import { useStore } from 'vuex'

  const store = useStore()
  const channelNameList = computed(() => store.getters.channelNameList)
  const channelIdList = computed(() => store.getters.channelIdList)
</script>

<template>
  <div class="sidebar">
    <div class="text-h5 white-text">NUTMEG</div>
    <div class="text-h6 white-text py-2">Channels</div>
    <div
        v-for="(name, i) in channelNameList" v-bind:key="i" class="mb-3"
      >
      <a :href="`/channels/${channelIdList[channelNameList.indexOf(name)]}`"
        class="white-text trext-h6"
        active-class="font-weight-bold"
      >
        {{ name }}
      </a>
      <RouterView name=MessageLog></RouterView>
    </div>
  </div>
</template>

<style>
  .white-text {
    color: white;
  }

  .sidebar {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 1;
    width: 25%;
    height: 100%;
    padding: 20px;
    overflow: scroll;
    background-color: #4d2947;
  }
</style>
