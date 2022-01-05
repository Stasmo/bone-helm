<template>
  <v-app id="inspire">
    <v-navigation-drawer
      v-model="drawer"
      app
    >
      <v-list-item>
        <v-list-item-content>
          <v-list-item-title class="title">
            Boilerplate Application
          </v-list-item-title>
          <v-list-item-subtitle>
            To be named later
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>
      <v-divider></v-divider>

      <v-list
        dense
        nav
      >
        <v-list-item
          v-for="item in items"
          :key="item.title"
          link
          :to="item.route"
        >
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>

          <v-list-item-content>
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" class="white--text">
      <v-app-bar-nav-icon @click="drawer = !drawer" class="white--text"></v-app-bar-nav-icon>

      <v-toolbar-title>Boilerplate Application</v-toolbar-title>
    </v-app-bar>

    <v-main class="lighten-5" :class="'deep-purple'">
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
import { mapActions } from 'vuex'
  export default {
    created() {
      document.addEventListener("deviceready", this.onDeviceReady, false);
    },
    data: () => ({
      drawer: null,
      items: [
        { title: 'Home', icon: 'mdi-view-dashboard', route: '/' },
        { title: 'Devices', icon: 'mdi-bluetooth-connect', route: '/devices' },
        { title: 'Settings', icon: 'mdi-cog-outline', route: '/settings' },
      ],
    }),
    methods: {
      ...mapActions(['onDeviceReady'])
    }
  }
</script>