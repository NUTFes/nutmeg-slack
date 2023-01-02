<template>
  <div class="channel">
    <h1>NUMEG SLACK LOG</h1>
    <v-col v-for="(slackLog, j) in slackLogs" v-bind:key="slackLog.channel">
      <v-card elevation="8">
        <v-card-title>
          <h3>{{ channel[j] }}</h3>
        </v-card-title>
        <li v-for="i in slackLog" :key="i" style="list-style: none">
          <v-card-text>
            <p>{{ i.user }}:{{ i.text }}</p>
          </v-card-text>
        </li>
      </v-card>
    </v-col>
  </div>
</template>

<script lang="ts">
import axios, { AxiosInstance } from "axios";

const client: AxiosInstance = axios.create({
  baseURL: "http://localhost:1323",
  headers: {
    "Content-Type": "application/json",
  },
});

export default {
  name: "ChannelView",
  data() {
    return {
      slackLogs: [
        {
          channel: "",
          text: "",
          thredTs: "",
          user: "",
          eventTs: "",
        },
      ],
      channel: [],
    };
  },
  mounted() {
    client.get("/group/channel").then((response) => {
      this.slackLogs = response.data;
      for (let i = 0; i < this.slackLogs.length; i++) {
        this.channel.push(this.slackLogs[i][0]["channel"]);
      }
    });
  },
};
</script>
