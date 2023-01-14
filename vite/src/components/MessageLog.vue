<script lang="ts" setup>
  import { computed } from 'vue'
  import { useStore } from 'vuex'

  const store = useStore()
  const channelLog = computed(() => store.getters.channelLog)
  const messageTime = computed(() => store.getters.messageTime)
</script>

<template>
  <v-row align="center" class="mt-5 flex-column">
    <v-card
      v-for="(log, i) in channelLog"
      :key="i"
      outlined
      class="mb-2 card-container pa-4"
    >
      <v-row>
        <div class="mr-5 font-weight-bold">{{ log.user }}</div>
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

  .time-font {
    font-size: 10px;
  }
</style>
