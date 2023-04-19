import App from './AppInfo.vue'

import { createApp } from 'vue'

import { registerPlugins } from '@/plugins'

const app = createApp(App)

registerPlugins(app)

app.mount('#app')
