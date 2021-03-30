<template>
  <v-row dense style="height: 100%;">

    <v-col cols="4" class="ma-2">
      <v-card
        color="#385F73"
        dark
      >
        <v-card-title>
          Create new
        </v-card-title>
        <v-card-text style="height: 150px;">
          <v-text-field label="Name" v-model="newLanguageName"></v-text-field>
          <v-combobox
            v-model="newLanguageChoice"
            :items="emptyChoices"
            label="Choose language variant"
            item-text="name"
            item-value="label"
            outlined
            dense
          ></v-combobox>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="createLanguage">
            <v-icon>mdi-plus</v-icon>
            Create
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>

    <v-col cols="2" v-for="language in languages" :key="language.id" class="ma-2">
      <v-card
        color="#385F73"
        dark
      >
        <v-card-title class="headline">
          {{language.name}}
        </v-card-title>

        <v-card-text  style="height: 150px;">
          {{language.label.toUpperCase()}}
        </v-card-text>

        <v-card-actions>
          <v-btn text @click="removingId = language.id; modalDrawer = true;">
            <v-icon>mdi-delete</v-icon>
            Remove
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-col>
    <AreYouSureModal
      v-model="modalDrawer"
      text="Вы уверены? Удалятся все переводы компонентов, которые вы создали для этого языка..."
      title="Подтвердить удаление."
      negative-value="No"
      positive-value="Yes"
      @onPositive="modalDrawer=false; removeLanguage(removingId);"
      @onNegative="modalDrawer=false;"
    />
  </v-row>
</template>

<script>
  import are_you_sure_modal from "./are_you_sure_modal"

    export default {
      components: {
        AreYouSureModal: are_you_sure_modal,
      },
      data () {
        return {
          newLanguageName: null,
          newLanguageChoice: null,
          removingId: null,
          modalDrawer: false
        }
      },
      computed: {
        languages () {
          return this.$store.getters["components/getLanguages"]
        },
        langChoices () {
          return this.$store.getters["components/langChoices"]
        },
        labelsList () {
          return this.languages.map(a => a.label)
        },
        emptyChoices () {
          return this.langChoices.filter(item => this.labelsList.indexOf(item.label.toLowerCase()) < 0)
        }
      },
      mounted() {
        this.$store.dispatch("components/setLanguages")
        this.$store.dispatch("components/setLangChoices")
      },
      methods: {
        createLanguage () {
          this.$axios.post(
            '/quiz/languages/',
            {
              "name": this.newLanguageName,
              "label": this.newLanguageChoice.label
            }
          )
            .then(response => {
              this.$store.dispatch("components/setLanguages")
            })
        },
        removeLanguage (languageId) {
          this.$axios.delete(
            '/quiz/languages/' + languageId
          )
            .then(response => {
              this.$store.dispatch("components/setLanguages")
            })

        }
      }
    }
</script>

<style scoped>

</style>
