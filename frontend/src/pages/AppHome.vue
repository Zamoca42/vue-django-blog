<template>
  <v-app id="inspire">
    <MainMenu/>

    <v-main>
      <HelloWorld/>
    </v-main>

    <MyFooter/>
  </v-app>
</template>

<script>
import MainMenu from '@/components/MainMenu.vue';
import HelloWorld from '@/components/HelloWorld.vue';
import MyFooter from '@/components/MyFooter.vue';

export default {
  components: { MainMenu, HelloWorld, MyFooter },

  data: () => ({}),
  methods: {},
}
</script>
