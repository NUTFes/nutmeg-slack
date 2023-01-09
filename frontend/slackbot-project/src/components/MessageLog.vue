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
const messageTime = ref<string[]>([]);
const date = ref<Date>();

client.get("/group/channel").then((response) => {
  const slackLogs: Message[][] = response.data;
  channelLog.value = slackLogs
  .filter((slackLog) => {
    return slackLog[0].channelId === routeParamChannelId;
  })
  .flat()
  .reverse();
  channelLog.value.forEach((log) => {
    date.value = new Date(parseInt(log.eventTs) * 1000);
    messageTime.value.push(date.value.toLocaleString());
  });
  console.log(messageTime)
});
</script>

<template>
  <v-row align="center" class="mt-5 flex-column">
    <v-card
      v-for="(log, i) in channelLog"
      :key="i"
      outlined
      class="mb-2 card-container"
    >
      <v-row>
        <div class="mr-5">{{ log.user }}</div>
        <div class="time-font pt-1">{{ messageTime[i] }}</div>
      </v-row>
      <v-row>{{ log.text }}</v-row>
    </v-card>
  </v-row>
</template>

<style>
.card-container {
  position: fixed;
  top: 50px;
  left: 13%;
  width: 75%;
}

.time-font{
  font-size: 10px;
}
</style>
