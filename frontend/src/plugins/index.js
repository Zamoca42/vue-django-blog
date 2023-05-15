import { loadFonts } from './webfontloader'
import vuetify from './vuetify'
import router from './router'

export function registerPlugins (app) {
  loadFonts()
  app.use(router)
  app.use(vuetify)
}
