<template>
  <v-app id="inspire">
    <MainMenu/>

    <v-main>
      <Information/>
    </v-main>

  </v-app>
</template>

<script>
import MainMenu from '@/components/MainMenu.vue';
import Information from '@/components/Information.vue';
// import MyFooter from '@/components/MyFooter.vue';

export default {
  components: { MainMenu, Information},

  data: () => ({}),
  methods: {},
}
</script>
