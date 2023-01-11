interface Message {
  channelId: string
  channelName: string
  text?: string
  user: string
  eventTs: string
  threadTs?: string
}

export default Message
