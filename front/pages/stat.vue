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
    </v-row>
    <v-row>
      <v-col cols="4">
        <v-btn @click="refreshStat">Refresh</v-btn>
        <h3 v-if="statData">Всего сессий за период: {{statData.total_sessions_count}}</h3>
        <h4 v-if="statData">Из них завершенных: {{statData.finished_sessions_count}}</h4>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="6">
        <apexcharts width="500" type="donut" :options="pieOptions" :series="byLanguageChartPercents"></apexcharts>
      </v-col>
      <v-col cols="6">
        <apexcharts width="500" type="line" :series="lineChartSeries" :options="lineOptions"/>
      </v-col>
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
          statData: null,
          lineOptions: {
            xaxis: {
              type: 'datetime'
            }
          },
          series: [44, 55, 41, 17, 15]
        }
      },
      computed: {
        languages() {
          return this.$store.getters["components/getLanguages"]
        },
        byLanguageChartPercents () {
          if (!this.statData) {
            return []
          } else {
            return this.statData.sessions_count_by_language.map(item => item.sessions_count_percent)
          }
        },
        byLanguageChartLabels () {
          if (!this.statData) {
            return []
          } else {
            return this.statData.sessions_count_by_language.map(item => this.getLanguageById(
              item.language_id).name + " (" + item.sessions_count + ")"
            )
          }
        },
        pieOptions () {
          return {
            pie: {
              expandOnClick: true
            },
            labels: this.byLanguageChartLabels
          }
        },
        lineChartData () {
          if (!this.statData) {
            return []
          } else {
            return this.statData.sessions_per_day.map(
              item => {
                return {
                  x: new Date(item.date).getTime(),
                  y: item.total
                }
              }
            )
          }
        },
        lineChartSeries () {
          return [
            {
              data: this.lineChartData
            }
          ]
        }
      },
      created () {
        this.$store.dispatch("components/setLanguages")
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
        },
        getLanguageById (id) {

          let langFilter = this.languages.filter(item => item.id === id)[0]
          if (langFilter) {
            console.log(langFilter)
            return langFilter
          } else {
            return {
              label: "Undefined",
              name: "Undefined"
            }
          }
        }
      }
    }
</script>

<style scoped>

</style>
