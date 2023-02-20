<template>
  <v-app id="inspire">
    <MainMenu/>

    <v-main>
      <PostList/>
    </v-main>

    <MyFooter/>
  </v-app>
</template>

<script>
import MainMenu from '@/components/MainMenu.vue';
import PostList from '@/components/PostList.vue';
import MyFooter from '@/components/MyFooter.vue';

export default {
  components: { MainMenu, PostList, MyFooter },

  data: () => ({}),
  methods: {},
}
</script>
