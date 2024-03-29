<template>
  <v-app>
    <v-app-bar color="white" density="compact" class="justify-space-between">
      <p class="ma-1 pa-1 me-auto text-button d-flex">
        <span>zamoca</span>
        <span class="d-none d-sm-flex">.space</span>
      </p>

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
          :to="$router.resolve(item.href)"
        >
          {{ item.text }}
        </v-btn>
      </div>
      <v-dialog v-model="dialog" scrollable width="460px">
        <template v-slot:activator="{ props }">
          <v-btn v-bind="props" @click="fetchTagCloud()">
            <v-icon>mdi-magnify</v-icon>Tag
          </v-btn>
        </template>
        <v-card>
          <v-card-title>Select Tag</v-card-title>
          <v-divider></v-divider>
          <v-container>
            <v-row>
              <v-col cols="auto">
                <v-chip
                  v-for="(tag, index) in tagCloud"
                  :key="index"
                  @click="serverPage(tag.name)"
                  class="ma-2"
                  :color="tag.chipColor"
                  ttext-color="white"
                >
                  <v-avatar
                    :color="tag.avatarColor"
                    size="x-small"
                    class="me-2"
                    >{{ tag.count }}</v-avatar
                  >
                  {{ tag.name }}
                </v-chip>
              </v-col>
            </v-row>
          </v-container>
          <v-card-text style="height: 300px"> </v-card-text>
          <v-divider></v-divider>
          <v-card-actions>
            <v-btn color="blue-darken-1" variant="text" @click="dialog = false">
              Close
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-app-bar>

    <v-navigation-drawer
      elevation="1"
      color="white"
      class="d-flex d-sm-none"
      v-model="drawer"
      location="top"
      :rail="drawer ? true : false"
      :rail-width="railwidth"
    >
      <v-list density="compact">
        <v-list-item
          class="justify-center"
          v-for="(item, i) in items"
          :key="i"
          :value="item"
          :to="$router.resolve(item.href)"
          active-color="primary"
        >
          <template v-slot:prepend> </template>

          <v-list-item-title v-text="item.text"></v-list-item-title>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
  </v-app>
</template>

<script>
import axios from "../plugins/axios-serverURL.js";

axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFToken";

export default {
  setup() {},

  data: () => ({
    drawer: false,
    dialog: false,
    tagCloud: [],
    items: [
      { text: "Info", href: { name: "Info" } },
      { text: "Blog", href: { name: "Blog" } },
    ],
  }),

  computed: {
    railwidth() {
      return 50 * this.items.length;
    },
  },

  methods: {
    async fetchTagCloud() {
      try {
        const response = await axios.get("/api2/tag/cloud/");
        this.tagCloud = response.data.tagList;

        this.tagCloud.forEach((element) => {
          if (element.weight === 3) {
            element.chipColor = "green-accent-4";
            element.avatarColor = "green-lighten-1";
          } else if (element.weight === 2) {
            element.chipColor = "cyan-accent-4";
            element.avatarColor = "blue-lighten-4";
          } else if (element.weight === 1) {
            element.chipColor = "grey-darken-1";
            element.avatarColor = "grey-lighten-1";
          }
        });
      } catch (err) {
        this.$router.push({ name: "NotFound" });
      }
    },

    serverPage(tagname) {
      this.$router.push({ name: "Blog", query: { tagname } });
      this.dialog = false;
    },
  },
};
</script>
