import axios, { AxiosInstance } from 'axios'
import { createStore } from 'vuex'

import { Message } from '@/types'

interface SlackLogState {
  channelName: string
  channelNameList: string[]
  channelIdList: string[]
  channelLog: Message[]
}

const client: AxiosInstance = axios.create({
  baseURL: 'http://localhost:1323',
  headers: {
    'Content-Type': 'application/json',
  },
})

export const store = createStore({
  state: {
    channelName: '',
    channelNameList: [],
    channelIdList: [],
    channelLog: [],
  },

  getters: {
    channelName: (state: SlackLogState) => state.channelName,
    channelNameList: (state: SlackLogState) => state.channelNameList,
    channelIdList: (state: SlackLogState) => state.channelIdList,
    channelLog: (state: SlackLogState) => state.channelLog,
  },

  mutations: {
    setChannelName(state: SlackLogState, channelName: string) {
      state.channelName = channelName
    },
    setChannelNameList(state: SlackLogState, channelNameList: string[]) {
      state.channelNameList = channelNameList
    },
    setChannelIdList(state: SlackLogState, channelIdList: string[]) {
      state.channelIdList = channelIdList
    },
    setChannelLog(state: SlackLogState, channelLog: Message[]) {
      state.channelLog = channelLog
    },
  },

  actions: {
    fetchSlackLog({ commit }: any, { channelId }: { channelId: string }) {
      client.get('/group/channel').then((res) => {
        const slackLogs: Message[][] = res.data
        const channelNameList: string[] = []
        const channelIdList: string[] = []
        const channelLog: Message[] = []

        slackLogs.forEach((slackLog) => {
          channelNameList.push(slackLog[0].channelName)
          channelIdList.push(slackLog[0].channelId)
          if (slackLog[0].channelId === channelId) {
            const channelName = slackLog[0].channelName
            commit('setChannelName', channelName)
            channelLog.push(slackLog[0])
            channelLog.flat().reverse()
            commit('setChannelLog', channelLog.flat().reverse())
          }
        })
        commit('setChannelNameList', channelNameList)
        commit('setChannelIdList', channelIdList)
      })
      // const channelNameList = res.data.map((channel: any) => channel.name);
      // const channelIdList = res.data.map((channel: any) => channel.id);
      // const channelNameList = ["general", "random", "test", channelId];
      // commit("setChannelNameList", channelNameList);
      //commit("setChannelIdList", channelIdList);
    },
  },
})
