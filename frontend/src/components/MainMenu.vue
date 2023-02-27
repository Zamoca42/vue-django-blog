<template>
    <v-app-bar color="indigo-lighten-5" density="compact" class="justify-space-between">

        <v-app-bar-nav-icon class="d-flex d-sm-none" @click="drawer = !drawer"></v-app-bar-nav-icon>

        <v-toolbar-title>zamoca.space</v-toolbar-title>

        <span class="d-none d-sm-flex">
            <v-btn variant="text" href="/home.html">INFO</v-btn>
            <v-btn variant="text" href="/blog/post_list.html">Blog</v-btn>
        </span>

        <v-spacer></v-spacer>

        <span>
            <v-btn href="/"><v-icon>mdi-magnify</v-icon>Tag</v-btn>
        </span>

    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app clipped>
        <v-list density="compact">
            <v-list-subheader>menu</v-list-subheader>

            <v-list-item v-for="(item, i) in items" :key="i" :value="item" :href="item.href" active-color="primary">
                <template v-slot:prepend>
                    <!-- <v-icon :icon="item.icon"></v-icon> -->
                </template>

                <v-list-item-title v-text="item.text"></v-list-item-title>
            </v-list-item>
        </v-list>
    </v-navigation-drawer>
</template>
  
<script>
import axios from 'axios';
import { user } from './globals.js';

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';

export default {
    setup() {
        return { user }
    },

    data: () => ({
        drawer: null,
        items: [
            { text: 'Information', href: '/home.html' },
            { text: 'Blog', href: '/blog/post_list.html' },
        ],
    }),

    created() {
        // console.log("created(MainMenu.vue)...");
        // this.user.getUserInfo();
    },

    mounted() {
        // console.log("mounted()...");
    },

    methods: {

    },
}
</script>
