<template>
  <v-app id="inspire" style="height: 100%;">
    <slot/>
  </v-app>
</template>

<script>
  export default {
    computed: {
      token () {
        return this.$store.getters["user/token"]
      },
      userData () {
        return this.$store.getters["user/userData"]
      }
    },
    mounted () {
      this.$store.dispatch('user/refreshUserData')
      if (!this.token) {
        this.$nuxt.$router.replace({ path: '/auth' })
      }
    },
    watch: {
      token (newValue, oldValue) {
        if (newValue && !oldValue) {
          this.$nuxt.$router.replace({ path: '/components' })
        }
      }
    }
  }
</script>

<style>
  .gradient-lighten {
    background-color: #5b6467 !important;
    background-image: linear-gradient(315deg, #5b6467 0%, #8b939a 74%) !important;
  }
  .gradient-darken {
    background-color: #485461 !important;
    background-image: linear-gradient(315deg, #485461 0%, #28313b 74%) !important;
  }
</style>
