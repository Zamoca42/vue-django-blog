<template>
    <div id="app">
      <nav>
        <MainMenu/>
      </nav>
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  import MainMenu from './components/MainMenu.vue';
  import { defineComponent } from 'vue';
  
  export default defineComponent({
    name: 'App',
    components: {
    MainMenu,
  },
  });
  </script>