import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from './router'
import { store } from './store/slack_log'

import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import KeyCloakService from './keycloak'

const vuetify = createVuetify({
  components,
  directives,
})

const renderApp = ()=>{
  createApp(App).use(router).use(vuetify).use(store).mount('#app')
}

KeyCloakService.CallLogin(renderApp)
