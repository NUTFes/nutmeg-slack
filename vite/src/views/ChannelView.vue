<script lang="ts" setup>
  import { useStore } from 'vuex'
  import { useRoute } from 'vue-router'
  import { onMounted } from 'vue'
  import Header from '@/components/Header.vue'
  import MessageLog from '@/components/MessageLog.vue'
  import SideBar from '@/components/SideBar.vue'

  const store = useStore()
  const route = useRoute()

  onMounted(() => {
    store.dispatch('fetchSlackLog', { channelId: route.params.channelId })
  })
</script>

<template>
  <div>
    <Header />
    <SideBar />
    <MessageLog />
  </div>
</template>
