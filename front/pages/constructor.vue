<template>
  <div style="height: 100%;">
    <v-row style="position: relative; top: 12px;">
      <v-col cols="5" style="height: 100%; padding: 0; padding-left: 10px;">
        <v-toolbar dark class="gradient-lighten" dense>
          <v-toolbar-title>Stages</v-toolbar-title>
        </v-toolbar>
        <StagesList
          v-if="stagesTree"
          :stages-tree="[stagesTree]"
          @emptyStageCreated="switchStageTo"/>
      </v-col>

      <v-col cols="7" class="h-100" style="padding: 0;">
        <v-toolbar dark class="gradient-lighten" dense>
          <v-toolbar-title>Stages</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn icon @click="drawer=!drawer">
            <v-icon>mdi-tools</v-icon>
          </v-btn>
        </v-toolbar>
        <StageView :stageData="currentStage" class="pa-4"/>
      </v-col>

      <v-navigation-drawer
        v-model="drawer"
        absolute
        right
        width="400px"
        style="height: 90vh;"
      >
        <v-toolbar dark class="gradient-lighten" dense>
          <v-tabs v-model="componentTab">
            <v-tabs-slider color="white"></v-tabs-slider>
            <v-tab
              v-for="item in componentItems"
              :key="item"
            >
              {{ item }}
            </v-tab>
          </v-tabs>
          <v-btn icon @click="drawer=!drawer">
            <v-icon>mdi-eye-off-outline</v-icon>
          </v-btn>
        </v-toolbar>
        <ButtonsList
          v-if="buttons && componentItems[componentTab] === 'Buttons'"
          :buttons="buttons"
          group="buttons"/>
        <TextsList
          v-if="texts && componentItems[componentTab] === 'Texts'"
          :texts="texts"
          group="texts"/>
      </v-navigation-drawer>
    </v-row>
  </div>
</template>

<script>

import { recursiveSearchById, arraySearchById } from "../lib/methods"
import buttons_list from "../components/buttons_list";
import texts_list from "../components/texts_list";
import stages_list from "../components/stages_list";
import stage_view from "../components/stage_view";

export default {
  components: {
    ButtonsList: buttons_list,
    TextsList: texts_list,
    StagesList: stages_list,
    StageView: stage_view
  },
  data() {
    return {
      drawer: false,
      componentItems: ["Buttons", "Texts"],
      componentTab: "Buttons",
      currentStage: {
        id: 1,
        title: "Some stage",
        button: 1
      },
      newButtons: [
        {
          id: 4,
          default_text: "asdasdas"
        }
      ]
    }
  },
  computed: {
    buttons () {
      return this.$store.getters["components/getButtons"]
    },
    texts () {
      return this.$store.getters["components/getTexts"]
    },
    stagesTree () {
      return this.$store.getters["stages/getStagesTree"]
    },
  },
  created () {
    this.$store.dispatch("components/setButtons")
    this.$store.dispatch("components/setTexts")
    this.$store.dispatch("stages/setStagesTree")
  },
  methods: {
    setCurrentStage (stageId) {
      this.$axios.get(
        '/quiz/stages/' + stageId
      )
        .then(response => {
          this.currentStage = response.data
        })
    },
    switchStageTo( stageId ) {
      this.setCurrentStage( stageId )
    }
  }
}
</script>

<style scoped>

</style>
