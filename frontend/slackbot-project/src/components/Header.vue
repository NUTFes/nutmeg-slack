<script lang="ts" setup>
import { ref } from "vue";
import axios, { AxiosInstance } from "axios";
import { useRoute } from "vue-router";
import { Message } from "@/types";


const client: AxiosInstance = axios.create({
  baseURL: "http://localhost:1323",
  headers: {
    "Content-Type": "application/json",
  },
});

const route = useRoute();
const channelName = ref<string>("");

client.get("/group/channel").then((response) => {
  const slackLogs: Message[][] = response.data;
  slackLogs.forEach((slackLog) => {
    if (slackLog[0].channelId === route.params.channelId) {
      channelName.value = slackLog[0].channelName;
    }
  });
});
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
  left: 0;
  right: 0;
  border-bottom: 2px solid #a3a0a0;
}
</style>
