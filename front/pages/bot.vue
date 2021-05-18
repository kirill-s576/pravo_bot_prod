<template>
  <div style="padding: 12px;">
    <h2>Languages</h2>
    <v-row dense>
      <v-col v-for="language in languages" :key="language.id" cols="2">
        <v-card height="150px">
          <v-card-title>
            {{language.name}}
          </v-card-title>
          <v-card-text>
            <v-checkbox
              label="Active"
              v-model="language.is_active"
              @click="toggleLanguage(language)"
            />
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <h2>Messages</h2>
      <v-row>
        <v-col cols="6">
          <v-select
            v-model="choosedMessage"
            :items="messages"
            label="Choose the message"
            item-text="label"
            return-object
            @change="setTranslate"
          ></v-select>
        </v-col>
        <v-col cols="6">
          <v-select
            v-if="choosedMessage.id !== 0"
            v-model="choosedLanguageId"
            :items="languages"
            label="Choose the language"
            item-value="id"
            item-text="name"
            @change="setTranslate"
          ></v-select>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="6">
          <h5>Default message</h5>
          <v-textarea v-model="choosedMessage.text"/>
          <v-btn >
            Save message
          </v-btn>
        </v-col>
        <v-col cols="6">
          <div v-if="currentTranslate">
            <h5>Translate</h5>
            <v-textarea v-model="currentTranslate.text"/>
            <v-btn @click="updateTranslate(currentTranslate.id, currentTranslate.text)">
              Save
            </v-btn>
          </div>
          <div v-else-if="choosedMessage && choosedMessage.id !== 0">
            <h5>Create new translate</h5>
            <v-textarea v-model="newTranslateText"/>
            <v-btn @click="createTranslate(choosedMessage.id, choosedLanguageId, newTranslateText)">
              Create
            </v-btn>
          </div>
          <div v-else>

          </div>
        </v-col>
      </v-row>
  </div>
</template>

<script>

export default {
  data () {
    return {
      choosedMessage: {
        id: 0,
        label: "",
        text: ""
      },
      choosedLanguageId: null,
      currentTranslate: null,
      newTranslateText: null
    }
  },
  computed: {
    languages () {
      return this.$store.getters["bot/botLanguages"]
    },
    messages () {
      return this.$store.getters["bot/botMessages"]
    },
    langChoices () {
      return this.$store.getters["bot/langChoices"]
    },
  },
  mounted () {
    this.$store.dispatch("bot/refreshBotLanguages")
    this.$store.dispatch("bot/refreshBotMessages")
    this.$store.dispatch("bot/refreshLangChoices")
  },
  methods: {
    updateTranslates (messageId) {
      this.$axios.get(
        '/tg_bot/messages/' + messageId + '/get_translates/'
      )
      .then(
        response => {
          this.currentTranslates = response.data
        }
      )
    },
    toggleLanguage ( language ) {
      this.$axios.put(
        '/tg_bot/languages/' + language.id + '/',
        {
          is_active: language.is_active
        }
      )
      .catch(
       error => {
         language.is_active = !language.is_active
         this.currentTranslate = null
       }
      )
    },
    setTranslate () {
      this.$axios.post(
        '/tg_bot/messages/' + this.choosedMessage.id + '/get_translate_by_language_id/',
        {
          language_id: this.choosedLanguageId
        }
      )
      .then(
        response => {
          this.currentTranslate = response.data
        }
      )
      .catch(
        error => {
          this.currentTranslate = null
        }
      )
    },
    createTranslate (messageId, languageId, text) {
      this.$axios.post(
        '/tg_bot/translates/',
        {
          message_id: messageId,
          language_id: languageId,
          text: text
        }
      )
      .then(
        response => {

        }
      )
    },
    updateTranslate ( translateId, text) {
      this.$axios.put(
        '/tg_bot/translates/' + translateId + '/',
        {
          text: text
        }
      )
      .then(
        response => {

        }
      )
    }
  }
}
</script>

<style>

</style>
