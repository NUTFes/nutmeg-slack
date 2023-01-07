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
const routeParamChannelId = route.params.channelId;
const channelLog = ref<Message[]>([]);

client.get("/group/channel").then((response) => {
  const slackLogs: Message[][] = response.data;

  channelLog.value = slackLogs.filter((slackLog)=>{
    return slackLog[0].channelId === routeParamChannelId
  }).flat();
});
</script>

<template>
  <div>
    {{ channelLog }}
  </div>
</template>
