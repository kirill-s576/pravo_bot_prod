<template>
  <div style="height: 100%;">
    <div>
      <v-toolbar dark class="gradient-lighten" dense>
        <v-tabs v-model="componentTab">
          <v-tabs-slider color="white"></v-tabs-slider>
          <v-tab
            v-for="item in componentCategories"
            :key="item"
          >
            {{ item }}
          </v-tab>
        </v-tabs>
      </v-toolbar>
    </div>
    <div>
      <LangFullEditor v-if="componentTab === 0"/>
      <MessageFullEditor v-if="componentTab === 1"/>
      <ButtonsFullEditor v-if="componentTab === 2"/>
    </div>
  </div>
</template>

<script>

import languages_full_editor from "../components/languages_full_editor";
import message_full_editor from "../components/message_full_editor";
import buttons_full_editor from "../components/buttons_full_editor";

export default {
  components: {
    LangFullEditor: languages_full_editor,
    MessageFullEditor: message_full_editor,
    ButtonsFullEditor: buttons_full_editor
  },
  data () {
    return {
      componentCategories: [
        "Languages", "Messages", "Buttons"
      ],
      componentTab: "Languages"
    }
  }
}
</script>

<style>

</style>
