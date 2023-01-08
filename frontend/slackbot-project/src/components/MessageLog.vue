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
const channelName = ref<string>("");

client.get("/group/channel").then((response) => {
  const slackLogs: Message[][] = response.data;

  channelLog.value = slackLogs.filter((slackLog)=>{
    return slackLog[0].channelId === routeParamChannelId
  }).flat().reverse();
  channelName.value = channelLog.value[0].channelName;
});
</script>

<template>
  <v-row
    align="center"
    class="mt-5 flex-column"
  >
    <v-row
      class="text-h4"
    >{{ channelName }}</v-row>
    <v-card v-for="log, i in channelLog" :key="i"
      outlined
      class="mb-2 card-container"
    >
      <v-row>
        <div
          class ="mr-5"
        >{{ log.user }}</div>
        <div>{{ log.eventTs }}</div>
      </v-row>
      <v-row>{{ log.text }}</v-row>
    </v-card>
  </v-row>
</template>

<style>
  .card-container{
    width: 70%;
  }
</style>
