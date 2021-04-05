<template>
  <div class="pa-4">
    <v-row>
      <v-col cols="6">
        <v-menu
          v-model="menuFrom"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateFrom"
              label="Date from"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateFrom"
            @input="menuFrom = false"
          ></v-date-picker>
        </v-menu>
      </v-col>
      <v-col cols="6">
        <v-menu
          v-model="menuTo"
          :close-on-content-click="false"
          :nudge-right="40"
          transition="scale-transition"
          offset-y
          min-width="auto"
        >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="dateTo"
              label="Date to"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="attrs"
              v-on="on"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="dateTo"
            @input="menuTo = false"
          ></v-date-picker>
        </v-menu>
      </v-col>
      <v-btn @click="refreshStat">Refresh</v-btn>
    </v-row>
    <v-row>
      {{statData}}
    </v-row>
  </div>
</template>

<script>
    export default {
      data () {
        return {
          dateFrom: new Date().toISOString().substr(0, 10),
          dateTo: new Date().toISOString().substr(0, 10),
          menuFrom: false,
          menuTo: false,
          statData: null
        }
      },
      methods: {
        refreshStat () {
          this.$axios.post(
            '/quiz/sessions/get_statistic/',
            {
              date_from: this.dateFrom,
              date_to: this.dateTo
            }
          )
          .then(
            response => {
              this.statData = response.data
            }
          )
        }
      }
    }
</script>

<style scoped>

</style>
