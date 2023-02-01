import axios, { AxiosInstance } from 'axios'
import { createStore } from 'vuex'
import { Message } from '@/types'

interface SlackLogState {
  channelName: string
  channelNameList: string[]
  channelIdList: string[]
  channelLog: Message[]
  messageTime: string[]
}

const client: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
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
    messageTime: [],
  },

  getters: {
    channelName: (state: SlackLogState) => state.channelName,
    channelNameList: (state: SlackLogState) => state.channelNameList,
    channelIdList: (state: SlackLogState) => state.channelIdList,
    channelLog: (state: SlackLogState) => state.channelLog,
    messageTime: (state: SlackLogState) => state.messageTime,
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
    setMessageTime(state: SlackLogState, messageTime: string[]) {
      state.messageTime = messageTime
    }
  },

  actions: {
    fetchSlackLog({ commit }: any, { channelId }: { channelId: string }) {
      client.get('/group/channel').then((res) => {
        const slackLogs: Message[][] = res.data
        const channelNameList: string[] = []
        const channelIdList: string[] = []
        const channelLog: Message[][] = []
        const messageTime: string[] = []

        slackLogs.forEach((slackLog: Message[]) => {
          channelNameList.push(slackLog[0].channelName)
          channelIdList.push(slackLog[0].channelId)

          if (slackLog[0].channelId === channelId) {
            const channelName = slackLog[0].channelName
            commit('setChannelName', channelName)
            channelLog.push(slackLog)
            channelLog.flat().reverse()
            commit('setChannelLog', channelLog.flat().reverse())
          }
        })
        channelLog[0].forEach((log) => {
          const date = new Date(parseInt(log.eventTs) * 1000)
          messageTime.push(date.toLocaleString())
        })
        commit('setChannelNameList', channelNameList)
        commit('setChannelIdList', channelIdList)
        commit('setMessageTime', messageTime.reverse())
      })
    },
  },
})
