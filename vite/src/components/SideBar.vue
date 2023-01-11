<script lang="ts" setup>
  import { ref, computed } from 'vue'
  import { useStore } from 'vuex'
  import axios, { AxiosInstance } from 'axios'
  import { Message } from '@/types'

  // const client: AxiosInstance = axios.create({
  //   baseURL: "http://localhost:1323",
  //   headers: {
  //     "Content-Type": "application/json",
  //   },
  // });

  // const channelNameList = ref<string[]>([]);
  // const channelIdList = ref<string[]>([]);

  // client.get("/group/channel").then((response) => {
  //   const slackLogs: Message[][] = response.data;
  //   slackLogs.forEach((slackLog) => {
  //     channelNameList.value.push(slackLog[0].channelName);
  //     channelIdList.value.push(slackLog[0].channelId);
  //   });
  // });
  const store = useStore()
  const channelNameList = computed(() => store.getters.channelNameList)
  const channelIdList = computed(() => store.getters.channelIdList)
</script>

<template>
  <div class="sidebar">
    <div class="text-h5 white-text">NUTMEG</div>
    <div class="text-h6 white-text py-2">Channels</div>
    <div v-for="(name, i) in channelNameList" v-bind:key="i" class="mb-3">
      <!-- <a
        :href="'/channels/' + channelId[channelName.indexOf(name)]"
        class="white-text text-h6"
      > -->
      <RouterLink
        :to="'/channels/' + channelIdList[channelNameList.indexOf(name)]"
        class="white-text trext-h6"
        active-class="font-weight-bold"
      >
        {{ name }}
      </RouterLink>
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
