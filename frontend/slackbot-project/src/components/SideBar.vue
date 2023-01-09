<script lang="ts" setup>
import { ref } from "vue";
import axios, { AxiosInstance } from "axios";
import { Message } from "@/types";

const client: AxiosInstance = axios.create({
  baseURL: "http://localhost:1323",
  headers: {
    "Content-Type": "application/json",
  },
});

const channelName = ref<string[]>([]);
const channelId = ref<string[]>([]);

client.get("/group/channel").then((response) => {
  const slackLogs: Message[][] = response.data;
  slackLogs.forEach((slackLog) => {
    channelName.value.push(slackLog[0].channelName);
    channelId.value.push(slackLog[0].channelId);
  });
});
</script>

<template>
  <div class="sidebar">
    <div class="text-h5 white-text">NUTMEG</div>
    <div class="text-h6 white-text py-2">Channels</div>
    <div v-for="(name, i) in channelName" v-bind:key="i">
      <a
        :href="'/channels/' + channelId[channelName.indexOf(name)]"
        class="white-text text-h6"
      >
        {{ name }}
      </a>
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
  width: 25%;
  height: 100%;
  background-color: #4d2947;
  padding: 20px;
}
</style>
