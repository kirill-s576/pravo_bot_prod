<template>
  <v-dialog
    v-model="value"
    persistent
    max-width="290"
  >
    <v-card>
      <v-card-title class="headline">
        {{title}}
      </v-card-title>
      <v-card-text>
        {{text}}
      </v-card-text>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          color="green darken-1"
          text
          @click="$emit('onPositive')"
        >
          {{positiveValue}}
        </v-btn>
        <v-btn
          color="green darken-1"
          text
          @click="$emit('onNegative')"
        >
          {{negativeValue}}
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script>
    export default {
      model: {
        prop: 'value'
      },
      props: {
        title: String,
        text: String,
        positiveValue: String,
        negativeValue: String,
        value: Boolean
      },
      data () {
        return {

        }
      }
    }
</script>

<style scoped>

</style>
