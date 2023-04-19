import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'
import '@/assets/main.css';

import { createVuetify } from 'vuetify'
import { VDataTable } from 'vuetify/labs/VDataTable'

export default createVuetify({
  theme: {
    themes: {
      light: {
        colors: {
          primary: '#1867C0',
          secondary: '#5CBBF6',
        },
      },
    },
  },

  components: {
    VDataTable,
  }, 

})
