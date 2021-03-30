<template>
    <v-card width="400" class="auth-form">
      <v-card-title class="gradient-lighten">
        Authentication
      </v-card-title>
      <v-card-text>
        <v-text-field v-model="email" label="E-mail" type="username"></v-text-field>
        <v-text-field v-model="password" label="Password" type="password"></v-text-field>
      </v-card-text>
      <v-card-actions class="justify-end">
        <v-btn @click="login">
          Login
          <v-icon>mdi-login</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>
</template>


<script>

    export default {
      layout: 'empty',
      data () {
        return {
          email: null,
          password: null
        }
      },
      computed: {
        token () {
          return this.$store.getters["user/token"]
        },
        userData () {
          return this.$store.getters["user/userData"]
        }
      },
      methods: {
        async login () {
          await this.$store.dispatch('user/login', {
            email: this.email,
            password: this.password
          })
        }
      }
    }
</script>

<style scoped>
  .auth-form {
    margin: 0 auto;
    top: 30vh;
  }
</style>
