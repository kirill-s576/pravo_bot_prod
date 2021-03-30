<template>
  <div style="height: 100%;" class="pa-2">
    <v-text-field label="Search" v-model="search"></v-text-field>
    <v-row dense style="height: 100%;">
      <v-col cols="4" v-for="message in messagesFilter" :key="message.id">
        <v-card v-if="message">
          <v-card-title >
            {{message.title}}
          </v-card-title>
          <v-card-text>
            <v-textarea v-model="message.default_text">

            </v-textarea>
          </v-card-text>
          <v-card-actions>
            <v-btn>
              Save
            </v-btn>
            <v-btn @click="dialogMessageData = message; dialogDrawer=true;">
              Settings
            </v-btn>
          </v-card-actions>
        </v-card>

      </v-col>

      <MessageSettingsDialog
        v-model="dialogDrawer"
        :message-data="dialogMessageData"
        :languagesData="languages"
        @closeDialog="dialogDrawer=false"
      />
    </v-row>
  </div>

</template>

<script>
  import message_settings_dialog from "./message_settings_dialog";
    export default {
      components: {
        MessageSettingsDialog: message_settings_dialog
      },
      data () {
        return {
          search: "",
          dialogDrawer: false,
          dialogMessageData: {
            title: null,
            default_text: null
          }
        }
      },
      computed: {
        languages () {
          return this.$store.getters["components/getLanguages"]
        },
        messages () {
          return this.$store.getters["components/getTexts"]
        },
        messagesFilter () {
          return this.messages.filter(item => item.default_text.indexOf(this.search) > -1)
        }
      },
      beforeCreate() {
        this.$store.dispatch("components/setLanguages")
        this.$store.dispatch("components/setTexts")
      },
    }
</script>

<style scoped>

</style>
