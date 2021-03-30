<template>
  <div style="height: 100%;" class="pa-2">
    <v-text-field label="Search" v-model="search"></v-text-field>
    <v-row dense style="height: 100%;">
      <v-col cols="4" v-for="button in buttonsFilter" :key="button.id">
        <v-card v-if="button">
          <v-card-title>
            <v-text-field v-model="button.default_text"></v-text-field>
          </v-card-title>
          <v-card-actions>
            <v-btn>
              Save
            </v-btn>
            <v-btn @click="dialogButtonData = button; dialogDrawer=true;">
              Settings
            </v-btn>
          </v-card-actions>
        </v-card>

      </v-col>

      <ButtonSettingsDialog
        v-model="dialogDrawer"
        :button-data="dialogButtonData"
        :languagesData="languages"
        @closeDialog="dialogDrawer=false"
      />
    </v-row>
  </div>

</template>

<script>
  import button_settings_dialog from "./button_settings_dialog";
    export default {
      components: {
        ButtonSettingsDialog: button_settings_dialog
      },
      data () {
        return {
          search: "",
          dialogDrawer: false,
          dialogButtonData: {
            id: 0,
            default_text: "Default"
          }
        }
      },
      computed: {
        languages () {
          try {
            return this.$store.getters["components/getLanguages"]
          } catch {
            return []
          }
        },
        buttons () {
          try {
            return this.$store.getters["components/getButtons"]
          } catch {
            return []
          }
        },
        buttonsFilter () {
          return this.buttons.filter(item => item.default_text.indexOf(this.search) > -1)
        }
      },
      beforeCreate () {
        this.$store.dispatch("components/setLanguages")
        this.$store.dispatch("components/setButtons")
      },
    }
</script>

<style scoped>

</style>
