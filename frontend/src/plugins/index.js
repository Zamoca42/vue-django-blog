import { loadFonts } from './webfontloader'
import vuetify from './vuetify'
import router from './router'
import VueKatex from '@hsorby/vue3-katex'

export function registerPlugins (app) {
  loadFonts()
  app.use(router)
  app.use(vuetify)
  app.use(VueKatex, {
    globalOptions: {
       //... Define globally applied KaTeX options here
    }
  })
}
