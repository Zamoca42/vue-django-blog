<template>
  <v-app id="inspire">
    <MainMenu/>

    <v-main>
      <PostDetail/>
    </v-main>

    <!-- <MyFooter/> -->
  </v-app>
</template>

<script>
import MainMenu from '@/components/MainMenu.vue';
import PostDetail from '@/components/PostDetail.vue';
// import MyFooter from '@/components/MyFooter.vue';

export default {
  components: { MainMenu, PostDetail},

  data: () => ({}),
  methods: {},
}
</script>
