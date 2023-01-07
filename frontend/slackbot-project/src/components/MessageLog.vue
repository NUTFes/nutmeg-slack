<template>
  <div>
    <h2>{{ users }}</h2>
    {{ users[$route.params.channelId]}}
    {{ channelLog }}
    <!-- {{ this.$route.params.channelId }} -->
  <!-- <div v-for="slackLog in slackLogs">
    {{slackLog[$route.params.id]]}}
  </div> -->
  </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import axios, { AxiosInstance } from "axios";

const client: AxiosInstance = axios.create({
  baseURL: "http://localhost:1323",
  headers: {
    "Content-Type": "application/json",
  },
});

export default defineComponent({
  name: "ChannelView",
  data() {
    return {
      slackLogs: [
        {
          channelId: "",
          channelName: "",
          text: "",
          user: "",
          eventTs: "",
        },
      ],
      channelLog: [],
    };
  },mounted() {
    var routeParamChannelId = this.$route.params.channelId;
    var channelLog = this.channelLog;

    client.get("/group/channel").then((response) => {
      this.slackLogs = response.data;
      for (let i = 0; i < this.slackLogs.length; i++) {
        this.slackLogs[i].filter(function (value) {
          if (value.channelId === routeParamChannelId) {
            channelLog.push(value);
          }
        });
      }
      console.log(this.channelLog);
    });
  }
});

</script>
