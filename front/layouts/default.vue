<template>
  <BaseLayout>
    <v-app-bar
      app
      color="#fcb69f"
      dark
      flat
      dense
      style="padding-left: 10px; padding-right: 10px;"
      class="gradient-darken"
    >
      <v-toolbar-title>Pravo Bot</v-toolbar-title>

      <v-spacer />


      <template v-slot:extension>
        <v-tabs>
          <v-tab to="/components">Компоненты</v-tab>
          <v-tab to="/constructor">Конструктор</v-tab>
          <v-tab to="/bot">Бот</v-tab>
        </v-tabs>
        <div v-if="userData">{{userData.email}}</div>
        <v-menu offset-y>
          <template v-slot:activator="{ on, attrs }">
            <v-btn
              icon
              v-bind="attrs"
              v-on="on"
            >
              <v-icon>mdi-account-box</v-icon>
            </v-btn>
          </template>
          <v-list>
            <v-list-item @click="logout">Logout</v-list-item>
          </v-list>
        </v-menu>
      </template>
    </v-app-bar>
    <v-main>
      <v-container fluid style="margin: 0; padding:0; display: block;">
        <nuxt />
      </v-container>
    </v-main>
  </BaseLayout>
</template>

<script>
  import base from "./base";
export default {
  components: {
    BaseLayout: base
  },
  computed: {
    userData () {
      return this.$store.getters["user/userData"]
    }
  },
  data () {
    return {
      drawer: true
    }
  },
  methods: {
    logout () {
      this.$store.dispatch('user/logout')
      this.$nuxt.$router.replace({ path: '/auth' })
    }
  }
}
</script>

<style>

</style>
