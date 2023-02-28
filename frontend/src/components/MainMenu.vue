<template>
  <v-app-bar color="white" density="compact" class="justify-space-between">
    <div class="ma-1 pa-1 me-auto">zamoca.space</div>

    <v-app-bar-nav-icon
      :icon="drawer ? 'mdi-chevron-up' : 'mdi-chevron-down'"
      class="d-flex d-sm-none ma-2 pa-2 me-auto"
      @click="drawer = !drawer"
    >
    </v-app-bar-nav-icon>
    <div class="d-none d-sm-flex me-auto">
      <v-btn
        variant="text"
        v-for="(item, i) in items"
        :key="i"
        :value="item"
        :href="item.href"
      >
        {{ item.text }}
      </v-btn>
    </div>
    <!-- <v-btn variant="text" href="/blog/post_list">Blog</v-btn> -->
    <v-btn href="/"><v-icon>mdi-magnify</v-icon>Tag</v-btn>
  </v-app-bar>

  <v-navigation-drawer
    :elevation="1"
    color="white"
    class="d-flex d-sm-none"
    v-model="drawer"
    location="top"
    rail="true"
    :rail-width="railwidth"
  >
    <v-list density="compact">
      <!-- <v-list-subheader>menu</v-list-subheader> -->
      <v-list-item
        class="justify-center"
        v-for="(item, i) in items"
        :key="i"
        :value="item"
        :href="item.href"
        active-color="primary"
      >
        <template v-slot:prepend>
          <!-- <v-icon :icon="item.icon"></v-icon> -->
        </template>

        <v-list-item-title v-text="item.text"></v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
import axios from "axios";
import { user } from "./globals.js";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default {
  setup() {
    return { user };
  },

  data: () => ({
    drawer: false,
    items: [
      { text: "Info", href: "/" },
      { text: "Blog", href: "/blog/post_list.html" },
    ],
  }),

  computed: {
    railwidth() {
      return 50 * this.items.length;
    },
  },

  created() {
    // console.log("created(MainMenu.vue)...");
    // this.user.getUserInfo();
  },

  mounted() {
    // console.log("mounted()...");
  },

  methods: {},
};
</script>
