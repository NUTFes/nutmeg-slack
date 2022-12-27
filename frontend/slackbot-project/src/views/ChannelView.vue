<template>
  <div class="channel">
    <h1>Channel</h1>
    {{ slackLog  }}
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
      slackLog: [],
    };
  },
  mounted() {
    client.get("/documents").then((response) => {
      this.slackLog = response.data;
      console.log(this.slackLog);
    });
  },
};
</script>
